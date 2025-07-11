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
        self.prebuild_step = ""
        self.postbuild_step = ""
        self.convert_hex = False
        self.convert_bin = False

    def parse(self):
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
        raw_source_paths = []
        for entry in root.findall(".//sourceEntries/entry"):
            if entry.get("kind") == "sourcePath":
                raw_source_paths.append(entry.get("name"))
        self.source_paths = sorted(list(set(raw_source_paths)))

        # Use sets to store unique include paths and defines
        unique_include_paths = set()
        unique_defines = set()

        # Extract include paths and defines from all toolchains
        for tool_chain in root.findall(".//toolChain"):
            for tool in tool_chain.findall("tool"):
                for option in tool.findall("option"):
                    if option.get("name") == "Include paths (-I)":
                        for value in option.findall("listOptionValue"):
                            unique_include_paths.add(value.get("value").replace("../", ""))
                    elif option.get("name") == "Define symbols (-D)":
                        for value in option.findall("listOptionValue"):
                            unique_defines.add(value.get("value"))

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


if __name__ == '__main__':
    parser = EclipseProjectParser("tests/stm32_project")
    parser.parse()
    print(f"Project Name: {parser.project_name}")
    print(f"Source Paths: {parser.source_paths}")
    print(f"Include Paths: {parser.include_paths}")
    print(f"Defines: {parser.defines}")
    print(f"Linker Script: {parser.linker_script}")
