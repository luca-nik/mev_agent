# `mev_project_interface.py` Documentation

## Overview

`mev_project_interface.py` serves as the main interface for the MEV Agent project. It integrates various components such as `order`, `venue`, `market`, and `agent` to facilitate the execution of MEV strategies.

## Functions

### `load_data(file_path)`

Load data from a JSON file.

**Parameters:**
- `file_path` (str): The path to the JSON file.

**Returns:**
- `dict`: The loaded data from the JSON file.

**Raises:**
- `FileNotFoundError`: If the specified file is not found.
- `json.JSONDecodeError`: If there is an error decoding the JSON data.

### `create_order(data)`

Create an `order` instance from the loaded JSON data.

**Parameters:**
- `data` (dict): The loaded JSON data.

**Returns:**
- `order`: An `order` instance.

### `create_venues(data)`

Create a list of `venue` instances from the loaded JSON data.

**Parameters:**
- `data` (dict): The loaded JSON data.

**Returns:**
- `list`: A list of `venue` instances.

### `main(file_path)`

Main function to optimize the surplus given the orders and the venues in the json file

**Parameters:**
- `file_path` (str): The path to the JSON file.

## Example Usage

```python
import sys
import os
import argparse
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from classes import order, venue, market, agent
import mev_project_interface as interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a JSON file path.')
    parser.add_argument('file_path', type=str, nargs='?', default=None, help='Path to the JSON file')
    args = parser.parse_args()

    if args.file_path is None:
        print("Error: No file path provided. Please provide the path to the JSON file.")
        sys.exit(1)

    interface.main(args.file_path)
