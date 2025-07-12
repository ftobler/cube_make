import sys
import os
import json
from cube_make.parser import EclipseProjectParser
from cube_make.generator import MakefileGenerator


CONFIG_FILENAME = "cube_make.json"


def extract_project_path() -> str:
    if len(sys.argv) < 2:
        print("Usage: cube_make <path_to_stm32_cube_eclipse_project>")
        sys.exit(1)
    return sys.argv[1]


def load_config(path: str) -> dict:
    config_path = os.path.join(path, CONFIG_FILENAME)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def verify_config(config: dict):
    required_keys = [
        "project_name", "source_paths", "include_paths", "defines",
        "linker_script", "optimization_level", "cpu_arch"
    ]
    missing = [key for key in required_keys if key not in config or config[key] is None]
    if missing:
        print(f"Config verification failed. Missing keys: {missing}")
        sys.exit(1)
    print("Config verification passed.")


def print_config(config: dict):
    print(f"project_name: {config.get('project_name')}")
    print(f"source_paths: {config.get('source_paths')}")
    print(f"include_paths: {config.get('include_paths')}")
    print(f"defines: {config.get('defines')}")
    print(f"linker_script: {config.get('linker_script')}")
    print(f"prebuild_step: {config.get('prebuild_step')}")
    print(f"postbuild_step: {config.get('postbuild_step')}")
    print(f"convert_hex: {config.get('convert_hex')}")
    print(f"convert_bin: {config.get('convert_bin')}")
    print(f"optimization_level: {config.get('optimization_level')}")
    print(f"float_abi: {config.get('float_abi')}")
    print(f"cpu_arch: {config.get('cpu_arch')}")


def main():
    project_path = extract_project_path()
    print(f"Generating Makefile for project at: {project_path}")

    global_config = load_config(".")

    local_config = load_config(project_path)

    parser = EclipseProjectParser(project_path)
    parser.parse()
    parsed_config = parser.get_config()

    config = parsed_config | global_config | local_config   # last one wins

    verify_config(config)
    print_config(config)

    generator = MakefileGenerator(
        project_path,
        config
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
