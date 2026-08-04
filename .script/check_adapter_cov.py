import sys
import os
os.chdir(r'X:\Project\echoui')
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from pytest import main
# Check adapter coverage
sys.exit(main([
    'tests/integration/',
    '--cov=src/echoui/adapters',
    '--cov-report=term-missing',
    '--cov-fail-under=80',
    '-q'
]))
