import subprocess
result = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\black.exe', '--check', 'src/', 'tests/'],
    capture_output=True, text=True
)
print("BLACK:", "PASS" if result.returncode == 0 else "FAIL")
if result.returncode != 0:
    print(result.stdout[-1000:])
    print(result.stderr[-1000:])

result2 = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\isort.exe', '--check-only', 'src/', 'tests/'],
    capture_output=True, text=True
)
print("ISORT:", "PASS" if result2.returncode == 0 else "FAIL")
if result2.returncode != 0:
    print(result2.stdout[-1000:])
    print(result2.stderr[-1000:])
