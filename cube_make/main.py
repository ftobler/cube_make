import sys
import os
import json
from typing import Dict, Any
from cube_make.parser import EclipseProjectParser
from cube_make.generator import MakefileGenerator
from cube_make.config import Config


CONFIG_FILENAME = "cube_make.json"


def extract_project_path() -> str:
    if len(sys.argv) < 2:
        print("Usage: cube_make <path_to_stm32_cube_eclipse_project>")
        sys.exit(1)
    return sys.argv[1]


def load_config(path: str) -> Dict[str, Any]:
    config_path = os.path.join(path, CONFIG_FILENAME)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def print_config(config: Config) -> None:
    print(config)


def main() -> None:
    project_path = extract_project_path()
    print(f"Generating Makefile for project at: {project_path}")

    global_config = load_config(".")

    local_config = load_config(project_path)

    parser = EclipseProjectParser(project_path)
    parser.parse()
    parsed_config = parser.get_config()

    merged_config_dict = parsed_config | global_config | local_config   # last one wins
    config = Config(merged_config_dict)

    config.verify()
    print_config(config)

    generator = MakefileGenerator(
        project_path,
        config
    )
    makefile_content = generator.generate()

    output_path = os.path.join(project_path, "Makefile")
    with open(output_path, "w") as f:
        f.write(makefile_content)
    print(f"Makefile generated at: {output_path}")


def main_console() -> None:
    """Main entry point for console script."""
    main()


if __name__ == "__main__":
    main()
