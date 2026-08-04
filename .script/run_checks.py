import subprocess
import sys

PY = r'E:\ProgramData\anaconda3\envs\py313\python.exe'
PIP = r'E:\ProgramData\anaconda3\envs\py313\Scripts'

def run(cmd, desc):
    print(f"=== {desc} ===")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

ret = 0

# Black
ret += run([f"{PIP}\\black.exe", "--check", "src/", "tests/"], "Black check")

# isort
ret += run([f"{PIP}\\isort.exe", "--check-only", "src/", "tests/"], "isort check")

# mypy
ret += run([PY, "-m", "mypy", "src/", "--strict"], "mypy strict")

# pylint
ret += run([f"{PIP}\\pylint.exe", "src/echoui/"], "pylint")

# flake8
ret += run([f"{PIP}\\flake8.exe", "src/", "tests/"], "flake8")

print(f"\nTotal issues: {ret}")
