import subprocess
import sys
result = subprocess.run(
    [r'E:\ProgramData\anaconda3\envs\py313\python.exe', '-m', 'mypy', 'src/', '--strict'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout[-3000:])
print("STDERR:", result.stderr[-2000:])
print("EXIT:", result.returncode)
