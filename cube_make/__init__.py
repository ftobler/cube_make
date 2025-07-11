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

    print(f"Project Name: {parser.project_name}")
    print(f"Source Paths: {parser.source_paths}")
    print(f"Include Paths: {parser.include_paths}")
    print(f"Defines: {parser.defines}")
    print(f"Linker Script: {parser.linker_script}")

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
        parser.float_abi
    )
    makefile_content = generator.generate()

    output_path = os.path.join(project_path, "makefile")
    with open(output_path, "w") as f:
        f.write(makefile_content)
    print(f"Makefile generated at: {output_path}")


if __name__ == "__main__":
    main()
