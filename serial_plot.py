"""
serial_plot.py — Live telemetry plotter for BLDC open-loop spin test

Binary frame (big-endian, 20 bytes):
  [0xAA][0x55] [Ia:i16] [Ib:i16] [Ic:i16] [Vbus:u16] [theta:u16]
  [omega:i16] [AmbT:i16] [PhT:i16] [fault:u8] [0x55]

  Scales: currents /100 -> A,  Vbus /100 -> V,  theta /10000 -> rad,
          omega /10 -> rad/s,  temps /10 -> °C

Usage:
    pip install pyserial pyqtgraph PyQt5
    python serial_plot.py
    python serial_plot.py --port COM12 --baud 921600
"""

import argparse
import collections
import struct
import threading
import sys

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

# ── Protocol ────────────────────────────────────────────────────────────────

SYNC       = bytes([0xAA, 0x55])
FRAME_FMT  = ">hhhHHhhhB"    # Ia Ib Ic Vbus theta omega AmbT PhT fault
FRAME_LEN  = 2 + struct.calcsize(FRAME_FMT) + 1   # sync + payload + tail (20)

# ── Shared state ─────────────────────────────────────────────────────────────

MAX_PTS    = 2000
POLE_PAIRS = 2       # change to match your motor

_keys = ["ia", "ib", "ic", "vbus", "theta", "omega", "amb_temp", "ph_temp"]
bufs  = {k: collections.deque([0.0] * MAX_PTS, maxlen=MAX_PTS) for k in _keys}
fault_val  = [0]
data_lock  = threading.Lock()
new_data   = threading.Event()

# ── Serial reader ─────────────────────────────────────────────────────────────

def serial_thread(port, baud):
    import serial
    try:
        ser = serial.Serial(port, baud, timeout=0.02)
    except Exception as e:
        print(f"Serial error: {e}")
        new_data.set()
        return

    raw = bytearray()
    while True:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            raw.extend(chunk)

        while len(raw) >= FRAME_LEN:
            idx = raw.find(SYNC)
            if idx == -1:
                raw = raw[-1:]
                break
            if idx + FRAME_LEN > len(raw):
                raw = raw[idx:]
                break

            frame = raw[idx : idx + FRAME_LEN]
            raw   = raw[idx + FRAME_LEN:]

            # validate tail byte
            if frame[-1] != 0x55:
                continue

            ia, ib, ic, vbus, theta, omega, amb, pht, fault = \
                struct.unpack_from(FRAME_FMT, frame, 2)

            vals = [
                ia    / 100.0,
                ib    / 100.0,
                ic    / 100.0,
                vbus  / 100.0,
                theta / 10000.0,
                (omega / 10.0) * 60.0 / (2 * 3.14159265 * POLE_PAIRS),  # rad/s elec -> RPM mech
                amb   / 10.0,
                pht   / 10.0,
            ]
            with data_lock:
                for k, v in zip(_keys, vals):
                    bufs[k].append(v)
                fault_val[0] = fault
            new_data.set()

# ── UI helpers ────────────────────────────────────────────────────────────────

pg.setConfigOptions(background="w", foreground="k", antialias=True)

COLORS = {
    "ia":       "#e63946",
    "ib":       "#2a9d8f",
    "ic":       "#457b9d",
    "vbus":     "#e76f51",
    "theta":    "#6a4c93",
    "omega":    "#f4a261",
    "amb_temp": "#e63946",
    "ph_temp":  "#2a9d8f",
}

MONO = QtGui.QFont("Consolas", 9)
BOLD = QtGui.QFont("Consolas", 9, 75)  # 75 = Bold weight


def make_plot(title, ylabel, series, window):
    """Returns (widget, {key: curve}, state_dict)."""
    pw = pg.PlotWidget(background="w")
    pw.setTitle(title, color="#333", size="9pt")
    pw.setLabel("left", ylabel, **{"font-size": "9pt", "color": "#555"})
    pw.showGrid(x=True, y=True, alpha=0.35)
    pw.addLegend(offset=(5, 5), labelTextColor="#333").setLabelTextSize("8pt")
    pw.getViewBox().setMouseEnabled(x=True, y=False)
    for ax in (pw.getAxis("left"), pw.getAxis("bottom")):
        ax.setPen(pg.mkPen("#bbb", width=1))
        ax.setTextPen(pg.mkPen("#666"))

    curves = {
        k: pw.plot(pen=pg.mkPen(COLORS[k], width=1.5), name=label,
                   downsampleMethod="peak", autoDownsample=True, clipToView=True)
        for k, label in series
    }
    state = {"window": window, "auto_y": True}
    return pw, curves, state


def autoscale(pw, arrays, pad=0.5):
    if not arrays:
        return
    mn = min(a.min() for a in arrays)
    mx = max(a.max() for a in arrays)
    pad = max((mx - mn) * 0.15, pad)
    pw.setYRange(mn - pad, mx + pad, padding=0)

# ── Main window ───────────────────────────────────────────────────────────────

def build_ui(port, baud):
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    win = QtWidgets.QWidget()
    win.setWindowTitle(f"BLDC Telemetry  [{port}  {baud}]")
    win.resize(1100, 900)
    win.setStyleSheet("QWidget{background:#f5f5f5;}")

    root = QtWidgets.QVBoxLayout(win)
    root.setContentsMargins(8, 8, 8, 8)
    root.setSpacing(4)

    # title bar
    hdr = QtWidgets.QHBoxLayout()
    lbl = QtWidgets.QLabel("BLDC OPEN-LOOP TELEMETRY")
    lbl.setFont(QtGui.QFont("Consolas", 11, 75))
    lbl.setStyleSheet("color:#1a1a1a;letter-spacing:2px;")
    status_lbl = QtWidgets.QLabel("OK")
    status_lbl.setFont(BOLD)
    status_lbl.setFixedWidth(160)
    status_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    status_lbl.setStyleSheet("background:#2dc653;color:#fff;border-radius:3px;padding:2px 6px;")
    btn_reset_zoom = QtWidgets.QPushButton("RESET ZOOM")
    btn_reset_zoom.setFont(BOLD)
    btn_reset_zoom.setFixedSize(100, 26)
    btn_reset_zoom.setStyleSheet(
        "QPushButton{background:#457b9d;color:#fff;border:none;border-radius:4px;}"
        "QPushButton:hover{background:#5a9cbd;}")

    hdr.addWidget(lbl); hdr.addStretch()
    hdr.addWidget(btn_reset_zoom)
    hdr.addSpacing(8)
    hdr.addWidget(status_lbl)
    root.addLayout(hdr)

    WINDOW = 500   # samples to display (~10 s at 50 Hz)

    pw_i, c_i, st_i = make_plot(
        "Phase Currents", "A",
        [("ia", "Ia"), ("ib", "Ib"), ("ic", "Ic")],
        WINDOW)

    pw_v, c_v, st_v = make_plot(
        "DC Bus Voltage", "V",
        [("vbus", "Vbus")],
        WINDOW)

    pw_ang, c_ang, st_ang = make_plot(
        "Electrical Angle", "rad",
        [("theta", "θ")],
        WINDOW)

    pw_spd, c_spd, st_spd = make_plot(
        "Speed", "RPM",
        [("omega", "RPM")],
        WINDOW)

    pw_tmp, c_tmp, st_tmp = make_plot(
        "Temperature", "°C",
        [("amb_temp", "Ambient"), ("ph_temp", "Phase")],
        WINDOW)

    splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
    for pw in (pw_i, pw_v, pw_ang, pw_spd, pw_tmp):
        splitter.addWidget(pw)
    splitter.setSizes([220, 110, 110, 110, 110])
    splitter.setStyleSheet("QSplitter::handle{background:#ddd;height:3px;}")
    root.addWidget(splitter, stretch=1)

    # groups: (plot_widget, state, {key: curve}, [keys], y_pad)
    plot_groups = [
        (pw_i,   st_i,   c_i,   ["ia", "ib", "ic"],         0.5),
        (pw_v,   st_v,   c_v,   ["vbus"],                    1.0),
        (pw_ang, st_ang, c_ang, ["theta"],                   0.3),
        (pw_spd, st_spd, c_spd, ["omega"],                   5.0),
        (pw_tmp, st_tmp, c_tmp, ["amb_temp", "ph_temp"],     1.0),
    ]

    def reset_zoom():
        for pw, *_ in plot_groups:
            pw.getViewBox().enableAutoRange()

    btn_reset_zoom.clicked.connect(reset_zoom)

    def update():
        if not new_data.is_set():
            return
        new_data.clear()

        with data_lock:
            snapshot = {k: np.array(list(bufs[k])) for k in _keys}
            fault = fault_val[0]

        for pw, st, curves, keys, pad in plot_groups:
            w = min(st["window"], MAX_PTS)
            slices = [snapshot[k][-w:] for k in keys]
            for k, sl in zip(keys, slices):
                curves[k].setData(sl)

            # autoscale Y to whatever is visible in the current x range
            vb = pw.getViewBox()
            x_min, x_max = vb.viewRange()[0]
            visible = [sl[max(0, int(x_min)) : min(len(sl), int(x_max) + 1)] for sl in slices]
            visible = [v for v in visible if len(v) > 0]
            if visible:
                autoscale(pw, visible, pad)
            elif slices:
                autoscale(pw, slices, pad)

        if fault == 0:
            status_lbl.setText("OK")
            status_lbl.setStyleSheet("background:#2dc653;color:#fff;border-radius:3px;padding:2px 6px;")
        else:
            parts = []
            if fault & 0x01: parts.append("nFAULT")
            if fault & 0x02: parts.append("SPI FAULT")
            status_lbl.setText(" | ".join(parts) if parts else f"FAULT {fault:#04x}")
            status_lbl.setStyleSheet("background:#e63946;color:#fff;border-radius:3px;padding:2px 6px;")

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(20)   # 50 Hz UI refresh
    win._timer = timer

    return app, win


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",  default="COM6")
    parser.add_argument("--baud",  type=int, default=921600)
    args = parser.parse_args()

    threading.Thread(target=serial_thread, args=(args.port, args.baud), daemon=True).start()

    app, win = build_ui(args.port, args.baud)
    win.show()
    sys.exit(app.exec())
