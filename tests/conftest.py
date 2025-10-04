'''Conftest file used for external modules (backend/main.py)
This allows for test_main.py to import functions from main.py from a separate directory'''

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))) # append absolute path to backend