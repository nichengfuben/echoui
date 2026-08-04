import subprocess
result = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\black.exe', 'src/', 'tests/'],
    capture_output=True, text=True
)
print("BLACK:", "OK" if result.returncode == 0 else "FAIL")
print(result.stdout[-500:])

result2 = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\isort.exe', 'src/', 'tests/'],
    capture_output=True, text=True
)
print("ISORT:", "OK" if result2.returncode == 0 else "FAIL")
print(result2.stdout[-500:])
