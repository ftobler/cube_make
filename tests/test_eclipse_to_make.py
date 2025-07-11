import os
import pytest
import subprocess
import textwrap
from unittest.mock import patch, mock_open

from eclipse_to_make.parser import EclipseProjectParser
from eclipse_to_make.generator import MakefileGenerator
from pathlib import Path

# --- Fixtures for test data ---


@pytest.fixture
def stm32_project_path(tmp_path):
    # Create a dummy project structure for testing
    project_dir = tmp_path / "stm32_project"
    project_dir.mkdir()

    files_repository_dir = Path() / "tests" / "minimal_files"

    # Simulate .cproject content
    # Ensure no leading whitespace or newlines before <?xml
    with open(files_repository_dir / "stm32_cproject_fixture.xml", "r") as f:
        (project_dir / ".cproject").write_text(f.read())

    # Create dummy source files
    (project_dir / "Core").mkdir()
    (project_dir / "Core" / "Src").mkdir()
    (project_dir / "Core" / "Src" / "main.c").write_text("int main() { return 0; }")
    (project_dir / "Core" / "Src" / "stm32_it.c").write_text("void IT_Handler() {}")
    (project_dir / "Core" / "Inc").mkdir()
    (project_dir / "Core" / "Inc" / "main.h").write_text("#define MAIN_H")
    (project_dir / "Core" / "Startup").mkdir()
    with open(files_repository_dir / "startup_stm32g030xx.s", "r") as f:
        (project_dir / "Core" / "Startup" / "startup_stm32g030xx.s").write_text(f.read())
    with open(files_repository_dir / "system_stm32g0xx.c", "r") as f:
        (project_dir / "Core" / "Src" / "system_stm32g0xx.c").write_text(f.read())
    with open(files_repository_dir / "syscalls.c", "r") as f:
        (project_dir / "Core" / "Src" / "syscalls.c").write_text(f.read())

    (project_dir / "Drivers").mkdir()
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver").mkdir()
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver" / "Src").mkdir()
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver" / "Src" / "stm32g0xx_hal.c").write_text("void HAL_Init() {}")
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver" / "Inc").mkdir()
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver" / "Inc" / "stm32g0xx_hal.h").write_text("#define HAL_Hxx")
    (project_dir / "Drivers" / "STM32G0xx_HAL_Driver" / "Inc" / "stm32g0xx.h").write_text("#define HAL_H")

    (project_dir / "application").mkdir()
    (project_dir / "application" / "app.c").write_text("void app_init() {}")
    (project_dir / "application" / "test.cpp").write_text("void test_cpp() {}")

    # (project_dir / "STM32G030K8TX_FLASH.ld").write_text("MEMORY { FLASH (rx) : ORIGIN = 0x8000000, LENGTH = 64K }")
    with open(files_repository_dir / "STM32G030K8TX_FLASH.ld", "r") as f:
        (project_dir / "STM32G030K8TX_FLASH.ld").write_text(f.read())

    return project_dir

# --- Tests for EclipseProjectParser ---


def test_fixture(stm32_project_path):
    assert stm32_project_path is not None


def test_make_is_available():
    try:
        subprocess.run(["make", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("Make is not available or not in PATH")


def test_arm_none_eabi_gcc_is_available():
    try:
        subprocess.run(["arm-none-eabi-gcc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("arm-none-eabi-gcc is not available or not in PATH")


def test_parser_extracts_project_name(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    assert parser.project_name == "stm32_project"


def test_parser_extracts_source_paths(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    expected_paths = ["Core", "Drivers", "Application"]
    assert sorted(parser.source_paths) == sorted(expected_paths)


def test_parser_extracts_include_paths(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    expected_includes = [
        "Core/Inc",
        "Drivers/STM32G0xx_HAL_Driver/Inc",
        "Drivers/STM32G0xx_HAL_Driver/Inc/Legacy",
        "Drivers/CMSIS/Device/ST/STM32G0xx/Include",
        "Drivers/CMSIS/Include",
        "application"
    ]
    assert sorted(parser.include_paths) == sorted(expected_includes)


def test_parser_extracts_defines(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    expected_defines = ["DEBUG", "USE_HAL_DRIVER", "STM32G030xx", "NDEBUG"]
    assert sorted(parser.defines) == sorted(expected_defines)


def test_parser_extracts_linker_script(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    assert parser.linker_script == "STM32G030K8TX_FLASH.ld"

# --- Tests for MakefileGenerator ---


def test_generator_produces_valid_makefile(stm32_project_path):
    parser = EclipseProjectParser(str(stm32_project_path))
    parser.parse()
    generator = MakefileGenerator(
        str(stm32_project_path),
        parser.project_name,
        parser.source_paths,
        parser.include_paths,
        parser.defines,
        parser.linker_script
    )
    makefile_content = generator.generate()

    # Basic sanity checks for Makefile content
    assert f"PROJECT_NAME = {parser.project_name}" in makefile_content
    assert "C_SOURCES =" in makefile_content
    assert "CPP_SOURCES =" in makefile_content
    assert "S_SOURCES =" in makefile_content
    assert "C_INCLUDES =" in makefile_content
    assert "C_DEFINES =" in makefile_content
    assert f"LD_SCRIPT = {parser.linker_script}" in makefile_content
    assert "all: $(BUILD_DIR)/$(PROJECT_NAME).elf" in makefile_content
    assert "\t@mkdir -p $(@D)" in makefile_content  # Check for tab indentation

    # Write the Makefile to a temporary location and try to parse it with make -n
    makefile_path = stm32_project_path / "makefile"
    makefile_path.write_text(makefile_content)

    try:
        # Use make -n to dry-run and check for syntax errors
        result = subprocess.run(
            ["make", "-n", str(makefile_path)],
            capture_output=True,
            text=True,
            check=True
        )
        assert result.returncode == 0
        assert "***" not in result.stderr # Check for common Makefile errors
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Generated Makefile has syntax errors or other issues: {e.stderr}")


def test_compile_makefile(stm32_project_path):
    # TODO: Implement a test that compiles using the generated Makefile
    pass