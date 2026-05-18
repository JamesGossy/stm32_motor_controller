################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.c 

OBJS += \
./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.o 

C_DEPS += \
./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/CMSIS/Device/ST/STM32G4xx/Source/%.o Drivers/CMSIS/Device/ST/STM32G4xx/Source/%.su Drivers/CMSIS/Device/ST/STM32G4xx/Source/%.cyclo: ../Drivers/CMSIS/Device/ST/STM32G4xx/Source/%.c Drivers/CMSIS/Device/ST/STM32G4xx/Source/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DSTM32 -DSTM32G4 -DNUCLEO_G474RE -DSTM32G474RETx -DSTM32G474xx -c -I../Inc -I../Drivers/CMSIS/Device/ST/STM32G4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32G4xx-2f-Source

clean-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32G4xx-2f-Source:
	-$(RM) ./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.cyclo ./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.d ./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.o ./Drivers/CMSIS/Device/ST/STM32G4xx/Source/system_stm32g4xx.su

.PHONY: clean-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32G4xx-2f-Source

