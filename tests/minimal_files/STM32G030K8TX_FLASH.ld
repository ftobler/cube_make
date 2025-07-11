/* Entry Point */
ENTRY(Reset_Handler)

/* Memories definition */
MEMORY
{
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 64K
  RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 8K
}

/* Sections */
SECTIONS
{
  .text :
  {
    KEEP(*(.isr_vector))
    *(.text*)
    *(.rodata*)
    . = ALIGN(4);
  } > FLASH

  .data :
  {
    . = ALIGN(4);
    _sdata = .;
    *(.data)
    _edata = .;
    . = ALIGN(4);
  } > RAM AT> FLASH

  _sidata = LOADADDR(.data);

  .bss :
  {
    . = ALIGN(4);
    __bss_start__ = .;
    *(.bss)
    __bss_end__ = .;
    . = ALIGN(4);
  } > RAM

  .heap :
  {
    . = ALIGN(4);
    end = .;
    _end = .;
    *(.heap*)
    . = ALIGN(4);
  } > RAM

  .stack :
  {
    . = ALIGN(4);
    _estack = .;
  } > RAM
}
