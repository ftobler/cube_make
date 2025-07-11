
# consider other compiler arguments
like but not exclusive:
* mthumb
* Wl,--start-group
* lc
* lm
* static
* gc-sections
* ffunction-sections
* fdata-sections
see below example arguments

# call examples

## assembler flag example:
-mcpu=cortex-m0plus -g3 -DDEBUG -c -x assembler-with-cpp --specs=nano.specs -mfloat-abi=soft -mthumb
## gcc flag example:
-mcpu=cortex-m0plus -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G030xx -c -I../Core/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32G0xx/Include -I../Drivers/CMSIS/Include -I../application -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity --specs=nano.specs -mfloat-abi=soft -mthumb
## g++ flag example:
-mcpu=cortex-m0plus -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G030xx -c -I../Core/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32G0xx/Include -I../Drivers/CMSIS/Include -I../application -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity --specs=nano.specs -mfloat-abi=soft -mthumb
## linker flag example:
-mcpu=cortex-m0plus -T"/home/ftobler/git/eclipse_to_make/tests/stm32_project_g030/STM32G030K8TX_FLASH.ld" --specs=nosys.specs -Wl,-Map="${BuildArtifactFileBaseName}.map" -Wl,--gc-sections -static --specs=nano.specs -mfloat-abi=soft -mthumb -Wl,--start-group -lc -lm -lstdc++ -lsupc++ -Wl,--end-group


