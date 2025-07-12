import sys
import os
from cube_make.parser import EclipseProjectParser
from cube_make.generator import MakefileGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: cube_make <path_to_stm32_cube_eclipse_project>")
        sys.exit(1)
    project_path = sys.argv[1]
    print(f"Generating Makefile for project at: {project_path}")

    parser = EclipseProjectParser(project_path)
    parser.parse()

    print(f"project_name: {parser.project_name}")
    print(f"source_paths: {parser.source_paths}")
    print(f"include_paths: {parser.include_paths}")
    print(f"defines: {parser.defines}")
    print(f"linker_script: {parser.linker_script}")
    print(f"prebuild_step: {parser.prebuild_step}")
    print(f"postbuild_step: {parser.postbuild_step}")
    print(f"convert_hex: {parser.convert_hex}")
    print(f"convert_bin: {parser.convert_bin}")
    print(f"optimization_level: {parser.optimization_level}")
    print(f"float_abi: {parser.float_abi}")
    print(f"cpu_arch: {parser.cpu_arch}")

    generator = MakefileGenerator(
        project_path,
        parser.project_name,
        parser.source_paths,
        parser.include_paths,
        parser.defines,
        parser.linker_script,
        parser.prebuild_step,
        parser.postbuild_step,
        parser.convert_hex,
        parser.convert_bin,
        parser.optimization_level,
        parser.float_abi,
        parser.cpu_arch
    )
    makefile_content = generator.generate()

    output_path = os.path.join(project_path, "makefile")
    with open(output_path, "w") as f:
        f.write(makefile_content)
    print(f"Makefile generated at: {output_path}")


def main_console():
    """Main entry point for console script."""
    main()


if __name__ == "__main__":
    main()
