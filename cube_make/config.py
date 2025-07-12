
import sys


class Config:
    def __init__(self, config_dict: dict):
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
        self.float_abi = config_dict.get("float_abi", "")
        self.cpu_arch = config_dict.get("cpu_arch")

    def verify(self):
        """Verifies that the essential configuration values are present."""
        required_keys = [
            "project_name",
            "source_paths",
            "include_paths",
            "defines",
            "linker_script",
            "optimization_level",
            "cpu_arch",
        ]
        missing = [key for key in required_keys if getattr(self, key) is None]
        if missing:
            print(f"Config verification failed. Missing keys: {missing}")
            sys.exit(1)
