import sys
import os
import argparse
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

import mev_project_interface as interface

if __name__ == "__main__":
    
    # Get the json file
    parser = argparse.ArgumentParser(description='Process a JSON file path.')
    parser.add_argument('file_path', type=str, nargs='?', default=None, help='Path to the JSON file')
    args = parser.parse_args()
    
    if args.file_path is None:
        print("Error: No file path provided. Please provide the path to the JSON file.")
        sys.exit(1)
    
    # Perform MEV optimization
    interface.main(args.file_path)


