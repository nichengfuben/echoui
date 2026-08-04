import sys
import os
os.chdir(r'X:\Project\echoui')
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from pytest import main
sys.exit(main(['tests/', '--tb=short', '-q']))
