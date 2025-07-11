import pytest
import subprocess
from pathlib import Path

from eclipse_to_make.parser import EclipseProjectParser
from eclipse_to_make.generator import MakefileGenerator

# List of example project paths
EXAMPLE_PROJECT_PATHS = [
    pytest.param(Path("tests/stm32_project_g030"), id="stm32_project_g030"),
    pytest.param(Path("tests/stm32_project_l412"), id="stm32_project_l412"),
]


@pytest.mark.parametrize("project_path", EXAMPLE_PROJECT_PATHS)
def test_compile_example_project(project_path):
    # Ensure make and arm-none-eabi-gcc are available
    try:
        subprocess.run(["make", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("Make is not available or not in PATH")

    try:
        subprocess.run(["arm-none-eabi-gcc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("arm-none-eabi-gcc is not available or not in PATH")

    # Parse the Eclipse project
    parser = EclipseProjectParser(str(project_path))
    parser.parse()

    # Generate the Makefile
    generator = MakefileGenerator(
        str(project_path),
        parser.project_name,
        parser.source_paths,
        parser.include_paths,
        parser.defines,
        parser.linker_script
    )
    makefile_content = generator.generate()

    # Write the Makefile to the project directory
    makefile_path = project_path / "makefile"
    makefile_path.write_text(makefile_content)

    print(f"--- Generated Makefile for {project_path} ---")
    print(makefile_content)
    print("--- End of Generated Makefile ---")

    try:
        # Clean the project first
        print(f"Cleaning project: {project_path}")
        clean_result = subprocess.run(
            ["make", "clean", "-C", str(project_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Clean stdout:\n{clean_result.stdout}")
        print(f"Clean stderr:\n{clean_result.stderr}")

        # Run make in the project directory
        print(f"Attempting to compile project: {project_path}")
        result = subprocess.run(
            ["make", "-C", str(project_path)],
            capture_output=True,
            text=True
        )
        print(f"Compilation stdout:\n{result.stdout}")
        print(f"Compilation stderr:\n{result.stderr}")
        result.check_returncode()

        # Check if the ELF file was created
        elf_file = project_path / "build" / f"{parser.project_name}.elf"
        assert elf_file.exists(), f"ELF file not found for {project_path}: {elf_file}"

    except subprocess.CalledProcessError as e:
        pytest.fail(f"Makefile compilation failed: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("Make command not found. Ensure 'make' is installed and in your PATH.")
