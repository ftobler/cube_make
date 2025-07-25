# cube_to_make

[![Build and Test](https://github.com/ftobler/cube_make/actions/workflows/main.yml/badge.svg)](https://github.com/ftobler/cube_make/actions/workflows/main.yml) [![Test cube_make Action](https://github.com/ftobler/cube_make/actions/workflows/as_action.yml/badge.svg)](https://github.com/ftobler/cube_make/actions/workflows/as_action.yml)


Create a makefile from a STM32 cube project. It mimics what Eclipse CDT pipelines would do in combination with ST specific behaviour.

## Usage

Install the python package:
```
pip install git+https://github.com/ftobler/cube_make.git
```


This made the `cube_make` command available. Use it like:
```
cube_make <path_to_project>
```


This will generate a `makefile` in the project folder. You can execute `make`, it will put results in `build`.

```bash
make clean
make -j 16
```

## Project

The project is written in python. It has a lot of C code in the tests, so 99% of all code is just used as a compile test.
