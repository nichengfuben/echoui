import subprocess
result = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\flake8.exe', 'src/'],
    capture_output=True, text=True
)
if result.stdout.strip():
    print("SRC FLAKE8 ISSUES:")
    print(result.stdout)
else:
    print("SRC FLAKE8: PASS")
print("EXIT:", result.returncode)
