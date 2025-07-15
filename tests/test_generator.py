import pytest
from cube_make.generator import MakefileGenerator
from cube_make.config import Config


backslash = "\\"
tab = "\t"


class TestMakefileGenerator:
    @pytest.fixture
    def config(self):
        return Config({
            'project_name': 'test_project',
            'source_paths': ['Core/Src', 'application'],
            'include_paths': ['Core/Inc', 'application'],
            'defines': ['DEBUG', 'STM32G030xx'],
            'linker_script': 'STM32G030K8TX_FLASH.ld',
            'cpu_arch': 'cortex-m0plus',
            'fpu': None,
            'float_abi': 'soft',
            'optimization_level': 'o2',
            'convert_hex': True,
            'convert_bin': False,
            'prebuild_step': '',
            'postbuild_step': ''
        })

    @pytest.fixture
    def generator(self, config):
        return MakefileGenerator('/path/to/project', config)

    def test_format_file_list_empty(self, generator):
        assert generator.format_file_list("C_SOURCES", []) == "# C_SOURCES = <list is empty>"

    def test_format_file_list_simple(self, generator):
        files = ["main.c", "system.c"]
        expected = f"""C_SOURCES = {backslash}
{tab}main.c {backslash}
{tab}system.c"""
        assert generator.format_file_list("C_SOURCES", files) == expected

    def test_format_file_list_with_prefix(self, generator):
        includes = ["Core/Inc", "Drivers/Inc"]
        expected = f"""C_INCLUDES = {backslash}
{tab}-ICore/Inc {backslash}
{tab}-IDrivers/Inc"""
        assert generator.format_file_list("C_INCLUDES", includes, prefix="-I") == expected

    def test_format_file_list_with_spaces(self, generator):
        files = ["my file.c", "another file.c"]
        expected = f"""C_SOURCES = {backslash}
{tab}'my file.c' {backslash}
{tab}'another file.c'"""
        assert generator.format_file_list("C_SOURCES", files) == expected

    def test_format_file_list_with_special_chars(self, generator):
        files = ["path/(file).c", "path/file$.c"]
        expected = f"""C_SOURCES = {backslash}
{tab}'path/(file).c' {backslash}
{tab}'path/file$.c'"""
        assert generator.format_file_list("C_SOURCES", files) == expected

    def test_format_file_list_mixed(self, generator):
        files = ["main.c", "my file.c", "path/(file).c"]
        expected = f"""C_SOURCES = {backslash}
{tab}main.c {backslash}
{tab}'my file.c' {backslash}
{tab}'path/(file).c'"""
        assert generator.format_file_list("C_SOURCES", files) == expected

    def test_format_file_list_empty_string_in_list(self, generator):
        files = ["main.c", "", "system.c"]
        expected = f"""C_SOURCES = {backslash}
{tab}main.c {backslash}
{tab}system.c"""
        assert generator.format_file_list("C_SOURCES", files) == expected
