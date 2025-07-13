
import sys
import json
from typing import Any


class Config:
    def __init__(self, config_dict: dict[str, Any]):
        self.project_name = config_dict.get("project_name")
        self.source_paths = config_dict.get("source_paths", [])
        self.include_paths = config_dict.get("include_paths", [])
        self.defines = config_dict.get("defines", [])
        self.linker_script = config_dict.get("linker_script")
        self.prebuild_step = config_dict.get("prebuild_step", "")
        self.postbuild_step = config_dict.get("postbuild_step", "")
        self.convert_hex = config_dict.get("convert_hex", False)
        self.convert_bin = config_dict.get("convert_bin", False)
        self.optimization_level = config_dict.get("optimization_level")
        float_abi = config_dict.get("float_abi", None)
        self.cpu_arch = config_dict.get("cpu_arch")

        if float_abi is not None:
            self.float_abi = float_abi
        else:
            self.float_abi = "soft"  # must apply a default if missing

    def verify(self):
        """Verifies that the essential configuration values are present."""
        required_keys = [
            "project_name",
            "source_paths",
            "include_paths",
            "defines",
            "linker_script",
            "prebuild_step",
            "postbuild_step",
            "convert_hex",
            "convert_bin",
            "optimization_level",
            "float_abi",
            "cpu_arch",
        ]
        missing = [key for key in required_keys if getattr(self, key) is None]
        if missing:
            print(f"Config verification failed. Missing keys: {missing}")
            sys.exit(1)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
