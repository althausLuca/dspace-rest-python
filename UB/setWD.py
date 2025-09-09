import os
import sys

# set wd to folder above
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# Change current working directory
os.chdir(parent_dir)

# Ensure parent directory is on sys.path for imports
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print(f"Working directory set to: {os.getcwd()}")
