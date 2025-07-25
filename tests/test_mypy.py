import subprocess
import pytest


def test_mypy_passes():
    try:
        subprocess.run(["mypy", "cube_make/", "tests/"], capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"""mypy failed: {e.stdout}\n{e.stderr}""")
