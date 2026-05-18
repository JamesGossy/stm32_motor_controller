################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/hal/hal_adc.c \
../Src/hal/hal_init.c \
../Src/hal/hal_pwm.c \
../Src/hal/hal_spi.c \
../Src/hal/hal_uart.c 

OBJS += \
./Src/hal/hal_adc.o \
./Src/hal/hal_init.o \
./Src/hal/hal_pwm.o \
./Src/hal/hal_spi.o \
./Src/hal/hal_uart.o 

C_DEPS += \
./Src/hal/hal_adc.d \
./Src/hal/hal_init.d \
./Src/hal/hal_pwm.d \
./Src/hal/hal_spi.d \
./Src/hal/hal_uart.d 


# Each subdirectory must supply rules for building sources it contributes
Src/hal/%.o Src/hal/%.su Src/hal/%.cyclo: ../Src/hal/%.c Src/hal/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DSTM32 -DSTM32G4 -DNUCLEO_G474RE -DSTM32G474RETx -DSTM32G474xx -c -I../Inc -I../Drivers/CMSIS/Device/ST/STM32G4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-hal

clean-Src-2f-hal:
	-$(RM) ./Src/hal/hal_adc.cyclo ./Src/hal/hal_adc.d ./Src/hal/hal_adc.o ./Src/hal/hal_adc.su ./Src/hal/hal_init.cyclo ./Src/hal/hal_init.d ./Src/hal/hal_init.o ./Src/hal/hal_init.su ./Src/hal/hal_pwm.cyclo ./Src/hal/hal_pwm.d ./Src/hal/hal_pwm.o ./Src/hal/hal_pwm.su ./Src/hal/hal_spi.cyclo ./Src/hal/hal_spi.d ./Src/hal/hal_spi.o ./Src/hal/hal_spi.su ./Src/hal/hal_uart.cyclo ./Src/hal/hal_uart.d ./Src/hal/hal_uart.o ./Src/hal/hal_uart.su

.PHONY: clean-Src-2f-hal

