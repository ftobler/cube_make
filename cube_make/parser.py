import xml.etree.ElementTree as ET
import os
import re
from typing import List, Dict, Any


class EclipseProjectParser:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.cproject_path = os.path.join(project_path, ".cproject")
        self.project_name: str = ""
        self.source_paths: List[str] = []
        self.include_paths: List[str] = []
        self.defines: List[str] = []
        self.linker_script: str = ""
        self.prebuild_step: str = ""
        self.postbuild_step: str = ""
        self.convert_hex: bool = False
        self.convert_bin: bool = False
        self.optimization_level: str | None = None
        self.float_abi: str | None = None
        self.cpu_arch: str = ""
        self.use_function_sections: bool = False
        self.use_data_sections: bool = False
        self.use_gc_sections: bool = False
        self.specs_nano: bool = False
        self.specs_nosys: bool = False

    def _find_cpu_arch(self) -> None:
        """Finds the CPU architecture from the startup file."""
        for source_path in self.source_paths:
            full_path = os.path.join(self.project_path, source_path)
            for root, _, files in os.walk(full_path):
                for file in files:
                    if file.endswith(".s"):
                        startup_file_path = os.path.join(root, file)
                        try:
                            with open(startup_file_path, "r", encoding='utf-8') as f:
                                content = f.read()
                                # Use regex to find .cpu directive
                                match = re.search(r"^\s*\.cpu\s+([a-zA-Z0-9\.\-+]+)", content, re.MULTILINE)
                                if match:
                                    self.cpu_arch = match.group(1)
                                    return  # Exit after finding the first one
                        except (IOError, UnicodeDecodeError):
                            # Ignore files that can't be read
                            pass
        assert self.cpu_arch != "", "No CPU architecture found in startup files. Create a *.s file with the line '.cpu cortex-m0plus'."

    def parse(self) -> None:
        tree = ET.parse(self.cproject_path)
        root = tree.getroot()

        # Extract project name
        project_element = root.find(".//project")
        if project_element is not None:
            self.project_name = project_element.get("name", "")

        # Extract pre and post build steps
        configuration_element = root.find(".//configuration")
        if configuration_element is not None:
            self.prebuild_step = configuration_element.get("prebuildStep", "")
            self.postbuild_step = configuration_element.get("postbuildStep", "")

        # Extract hex and bin conversion flags
        for option in root.findall(".//option"):
            if option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.option.converthex":
                self.convert_hex = (option.get("value") == "true")
            elif option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.option.convertbinary":
                self.convert_bin = (option.get("value") == "true")

        # Extract source paths (deduplicate them)
        raw_source_paths: List[str] = []
        for entry in root.findall(".//sourceEntries/entry"):
            if entry.get("kind") == "sourcePath":
                name = entry.get("name")
                if name is not None:
                    raw_source_paths.append(name)
        self.source_paths = sorted(list(set(raw_source_paths)))

        self._find_cpu_arch()

        # Use sets to store unique include paths and defines
        unique_include_paths: set[str] = set()
        unique_defines: set[str] = set()

        # Extract include paths, defines and optimization level from all toolchains
        for tool_chain in root.findall(".//toolChain"):
            for tool in tool_chain.findall("tool"):
                for option in tool.findall("option"):
                    if option.get("name") == "Include paths (-I)":
                        for value in option.findall("listOptionValue"):
                            val = value.get("value")
                            print(f"Found include path: {val}")
                            if val is not None:
                                unique_include_paths.add(val.replace("../", ""))
                    elif option.get("name") == "Define symbols (-D)":
                        for value in option.findall("listOptionValue"):
                            val = value.get("value")
                            print(f"Found define: {val}")
                            if val is not None:
                                unique_defines.add(val)
                    elif option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.c.compiler.option.optimization.level":
                        print("Found optimization level option")
                        optimization_level = option.get("value")
                        if optimization_level:
                            self.optimization_level = optimization_level.replace(
                                "com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.c.compiler.option.optimization.level.value.", ""
                            )
                        else:
                            self.optimization_level = None
            for option in tool_chain.findall("option"):
                print(option.get("superClass"))
                if option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.option.floatabi":
                    print("Found float ABI option")
                    float_abi = option.get("value")
                    if float_abi:
                        self.float_abi = float_abi.replace("com.st.stm32cube.ide.mcu.gnu.managedbuild.option.floatabi.value.", "")
                    else:
                        self.float_abi = None

        self.include_paths = sorted(list(unique_include_paths))
        self.defines = sorted(list(unique_defines))

        # Extract linker script from any linker tool
        linker_tool = None
        for tool in root.findall(".//tool"):
            if "Linker" in tool.get("name", ""):
                for option in tool.findall("option"):
                    if option.get("name") == "Linker Script (-T)":
                        linker_tool = tool
                        break
                if linker_tool is not None:
                    break
        if linker_tool is not None:
            for option in linker_tool.findall("option"):
                if option.get("name") == "Linker Script (-T)":
                    linker_script_raw = option.get("value", "")
                    # Resolve ${workspace_loc:/${ProjName}/...} to a relative path
                    if linker_script_raw.startswith("${workspace_loc:/"):
                        # Extract the filename after the last '/' and remove the trailing '}'
                        self.linker_script = linker_script_raw.split('/')[-1][:-1]
                    else:
                        self.linker_script = linker_script_raw

    def get_config(self) -> Dict[str, Any]:
        config = {
            "project_name": self.project_name,
            "source_paths": self.source_paths,
            "include_paths": self.include_paths,
            "defines": self.defines,
            "linker_script": self.linker_script,
            "prebuild_step": self.prebuild_step,
            "postbuild_step": self.postbuild_step,
            "convert_hex": self.convert_hex,
            "convert_bin": self.convert_bin,
            "cpu_arch": self.cpu_arch
        }
        if self.optimization_level is not None:
            config["optimization_level"] = self.optimization_level
        if self.float_abi is not None:
            config["float_abi"] = self.float_abi
        return config


if __name__ == '__main__':
    import json
    parser = EclipseProjectParser("tests/stm32_project_g030")
    parser.parse()
    config = parser.get_config()
    print(json.dumps(config, indent=4))
