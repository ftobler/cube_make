# eclipse_to_make

This project aims to generate a Makefile for an existing Eclipse CDT project, particularly useful for STM32 microcontroller projects.

## Usage

To generate the Makefile for an Eclipse CDT project, run the `eclipse_to_make` command followed by the path to your Eclipse project directory:

```bash
eclipse_to_make /path/to/your/eclipse_project
```

For example, to generate the Makefile for the provided example project:

```bash
eclipse_to_make ./tests/stm32_project
```

After the Makefile is generated, you can build your project using `make`:

```bash
make
```
