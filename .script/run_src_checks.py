import subprocess
import sys

PY = r'E:\ProgramData\anaconda3\envs\py313\python.exe'
PIP = r'E:\ProgramData\anaconda3\envs\py313\Scripts'

def run(cmd, desc):
    print(f"=== {desc} ===")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout[-3000:])  # Last 3000 chars
    if result.stderr:
        print(result.stderr[-2000:])
    return result.returncode

# mypy on src only
ret = run([PY, "-m", "mypy", "src/", "--strict"], "mypy strict")

# pylint on src
ret2 = run([f"{PIP}\\pylint.exe", "src/echoui/", "--disable=C0114,C0115,C0116,R0903"], "pylint")

print(f"\nmypy exit: {ret}, pylint exit: {ret2}")
