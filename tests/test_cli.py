import subprocess
import sys


def test_cli_demo_runs():
    result = subprocess.run([sys.executable, "main.py", "demo"], capture_output=True, text=True, check=True)
    assert "[L1]" in result.stdout
    assert "[L2]" in result.stdout
    assert "[L3]" in result.stdout
