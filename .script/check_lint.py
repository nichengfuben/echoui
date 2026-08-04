import subprocess
result = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\pylint.exe', 'src/echoui/', '--disable=C0114,C0115,C0116,R0903'],
    capture_output=True, text=True
)
print("PYLINT:")
lines = result.stdout.strip().split('\n')
# Print last 15 lines
for line in lines[-15:]:
    print(line)
print("EXIT:", result.returncode)

result2 = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\Scripts\flake8.exe', 'src/', 'tests/'],
    capture_output=True, text=True
)
print("\nFLAKE8:")
if result2.stdout.strip():
    lines2 = result2.stdout.strip().split('\n')
    for line in lines2[-20:]:
        print(line)
else:
    print("PASS")
print("EXIT:", result2.returncode)
