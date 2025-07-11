import xml.etree.ElementTree as ET
import os

class EclipseProjectParser:
    def __init__(self, project_path):
        self.project_path = project_path
        self.cproject_path = os.path.join(project_path, ".cproject")
        self.project_name = ""
        self.source_paths = []
        self.include_paths = []
        self.defines = []
        self.linker_script = ""

    def parse(self):
        tree = ET.parse(self.cproject_path)
        root = tree.getroot()

        # Extract project name
        project_element = root.find(".//project")
        if project_element is not None:
            self.project_name = project_element.get("name", "")

        # Extract source paths (deduplicate them)
        raw_source_paths = []
        for entry in root.findall(".//sourceEntries/entry"):
            if entry.get("kind") == "sourcePath":
                raw_source_paths.append(entry.get("name"))
        self.source_paths = list(set(raw_source_paths))

        # Extract include paths and defines from the C compiler tool
        c_compiler_tool = root.find(".//tool[@superClass='com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.c.compiler']")
        if c_compiler_tool is not None:
            for option in c_compiler_tool.findall("option"):
                if option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.c.compiler.option.includepaths":
                    for value in option.findall("listOptionValue"):
                        self.include_paths.append(value.get("value").replace("../", "")) # Remove ../ for relative paths
                elif option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.c.compiler.option.definedsymbols":
                    for value in option.findall("listOptionValue"):
                        self.defines.append(value.get("value"))

        # Extract linker script from the C++ linker tool (assuming C and C++ linkers use the same script)
        cpp_linker_tool = root.find(".//tool[@superClass='com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.cpp.linker']")
        if cpp_linker_tool is not None:
            for option in cpp_linker_tool.findall("option"):
                if option.get("superClass") == "com.st.stm32cube.ide.mcu.gnu.managedbuild.tool.cpp.linker.option.script":
                    linker_script_raw = option.get("value", "")
                    # Resolve ${workspace_loc:/${ProjName}/...} to a relative path
                    if linker_script_raw.startswith("${workspace_loc:/"):
                        # Find the end of the project name part
                        start_index = len("${workspace_loc:/") + len(self.project_name) + 1 # +1 for the '/' after project name
                        # Remove the prefix and the trailing '}'
                        self.linker_script = linker_script_raw[start_index:-1]
                    else:
                        self.linker_script = linker_script_raw


if __name__ == '__main__':
    parser = EclipseProjectParser("tests/stm32_project")
    parser.parse()
    print(f"Project Name: {parser.project_name}")
    print(f"Source Paths: {parser.source_paths}")
    print(f"Include Paths: {parser.include_paths}")
    print(f"Defines: {parser.defines}")
    print(f"Linker Script: {parser.linker_script}")
