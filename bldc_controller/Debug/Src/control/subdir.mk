################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/control/angle_ramp.c \
../Src/control/commutator.c \
../Src/control/svpwm.c \
../Src/control/transforms.c 

OBJS += \
./Src/control/angle_ramp.o \
./Src/control/commutator.o \
./Src/control/svpwm.o \
./Src/control/transforms.o 

C_DEPS += \
./Src/control/angle_ramp.d \
./Src/control/commutator.d \
./Src/control/svpwm.d \
./Src/control/transforms.d 


# Each subdirectory must supply rules for building sources it contributes
Src/control/%.o Src/control/%.su Src/control/%.cyclo: ../Src/control/%.c Src/control/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DSTM32 -DSTM32G4 -DNUCLEO_G474RE -DSTM32G474RETx -DSTM32G474xx -c -I../Inc -I../Drivers/CMSIS/Device/ST/STM32G4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-control

clean-Src-2f-control:
	-$(RM) ./Src/control/angle_ramp.cyclo ./Src/control/angle_ramp.d ./Src/control/angle_ramp.o ./Src/control/angle_ramp.su ./Src/control/commutator.cyclo ./Src/control/commutator.d ./Src/control/commutator.o ./Src/control/commutator.su ./Src/control/svpwm.cyclo ./Src/control/svpwm.d ./Src/control/svpwm.o ./Src/control/svpwm.su ./Src/control/transforms.cyclo ./Src/control/transforms.d ./Src/control/transforms.o ./Src/control/transforms.su

.PHONY: clean-Src-2f-control

