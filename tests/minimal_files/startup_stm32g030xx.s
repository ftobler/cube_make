.syntax unified
.cpu cortex-m0plus
.thumb

.global g_pfnVectors
.global Default_Handler

/* start address for the stack */
.word _estack

.section .isr_vector
.align 2
g_pfnVectors:
  .word _estack
  .word Reset_Handler
  .word NMI_Handler
  .word HardFault_Handler
  .word SVC_Handler
  .word PendSV_Handler
  .word SysTick_Handler

/* External Interrupts */
  .word WWDG_IRQHandler
  .word PVD_IRQHandler
  .word RTC_TAMP_IRQHandler
  .word FLASH_IRQHandler
  .word RCC_IRQHandler
  .word EXTI0_1_IRQHandler
  .word EXTI2_3_IRQHandler
  .word EXTI4_15_IRQHandler
  .word DMA1_Channel1_IRQHandler
  .word DMA1_Channel2_3_IRQHandler
  .word DMA1_Channel4_5_6_7_IRQHandler
  .word ADC1_IRQHandler
  .word TIM1_BRK_UP_TRG_COMP_IRQHandler
  .word TIM1_CC_IRQHandler
  .word TIM2_IRQHandler
  .word TIM3_IRQHandler
  .word TIM6_DAC_LPTIM1_IRQHandler
  .word TIM7_LPTIM2_IRQHandler
  .word TIM14_IRQHandler
  .word TIM15_IRQHandler
  .word TIM16_IRQHandler
  .word TIM17_IRQHandler
  .word I2C1_IRQHandler
  .word I2C2_IRQHandler
  .word SPI1_IRQHandler
  .word SPI2_IRQHandler
  .word USART1_IRQHandler
  .word USART2_IRQHandler
  .word USART3_4_IRQHandler
  .word CEC_IRQHandler
  .word AES_RNG_IRQHandler
  .word USB_IRQHandler

.thumb_func
.weak Reset_Handler
.type Reset_Handler, %function
Reset_Handler:

/* Copy the data segment initializers from flash to SRAM */
  ldr r0, =_sdata
  ldr r1, =_edata
  ldr r2, =_sidata
  movs r3, #0
  b LoopCopyDataInit

CopyDataInit:
  ldr r4, [r2, r3]
  str r4, [r0, r3]
  adds r3, r3, #4

LoopCopyDataInit:
  cmp r3, r1
  blt CopyDataInit

/* Zero fill the .bss segment. */
  ldr r2, =__bss_start__
  ldr r4, =__bss_end__
  movs r3, #0
  b LoopFillZerobss

FillZerobss:
  str r3, [r2]
  adds r2, r2, #4

LoopFillZerobss:
  cmp r2, r4
  blt FillZerobss

/* Call the system clock initialization function */
  bl SystemInit

/* Call the application's entry point.*/
  bl main
  bx lr

.align 4

.thumb_func
.weak Default_Handler
.type Default_Handler, %function
Default_Handler:
  b .

.macro IRQ handler
  .weak \handler
  .set \handler, Default_Handler
.endm

IRQ NMI_Handler
IRQ HardFault_Handler
IRQ SVC_Handler
IRQ PendSV_Handler
IRQ SysTick_Handler

IRQ WWDG_IRQHandler
IRQ PVD_IRQHandler
IRQ RTC_TAMP_IRQHandler
IRQ FLASH_IRQHandler
IRQ RCC_IRQHandler
IRQ EXTI0_1_IRQHandler
IRQ EXTI2_3_IRQHandler
IRQ EXTI4_15_IRQHandler
IRQ DMA1_Channel1_IRQHandler
IRQ DMA1_Channel2_3_IRQHandler
IRQ DMA1_Channel4_5_6_7_IRQHandler
IRQ ADC1_IRQHandler
IRQ TIM1_BRK_UP_TRG_COMP_IRQHandler
IRQ TIM1_CC_IRQHandler
IRQ TIM2_IRQHandler
IRQ TIM3_IRQHandler
IRQ TIM6_DAC_LPTIM1_IRQHandler
IRQ TIM7_LPTIM2_IRQHandler
IRQ TIM14_IRQHandler
IRQ TIM15_IRQHandler
IRQ TIM16_IRQHandler
IRQ TIM17_IRQHandler
IRQ I2C1_IRQHandler
IRQ I2C2_IRQHandler
IRQ SPI1_IRQHandler
IRQ SPI2_IRQHandler
IRQ USART1_IRQHandler
IRQ USART2_IRQHandler
IRQ USART3_4_IRQHandler
IRQ CEC_IRQHandler
IRQ AES_RNG_IRQHandler
IRQ USB_IRQHandler
