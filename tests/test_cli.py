import subprocess
import sys

CLI = [sys.executable, "-m", "ai_cli.cli"]

def run_cli(*args):
    return subprocess.run(
        CLI + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
    )

def test_help_top_level():
    res = run_cli("--help")
    assert res.returncode == 0
    assert "Usage:" in res.stdout
    assert "list" in res.stdout and "run" in res.stdout

def test_run_help():
    res = run_cli("run", "--help")
    assert res.returncode == 0
    assert "Usage:" in res.stdout
    assert "model" in res.stdout
