# `mev_project_interface.py` Documentation

## Overview

`mev_project_interface.py` serves as the main interface for the MEV Agent project. It integrates various components such as `order`, `venue`, `market`, and `agent` to facilitate the execution of MEV strategies.

## Functions

### `load_data(file_path)`

Loads data from a JSON file.

- **Parameters**:
  - `file_path` (str): The path to the JSON file.

- **Returns**:
  - `data` (dict): The loaded data from the JSON file.

### `create_order(data)`

Creates a list of `Order` instances from the loaded JSON data.

- **Parameters**:
  - `data` (dict): The loaded JSON data.

- **Returns**:
  - `Order` (order instance): An `Order` object containing user intent.

- **Note**:
  - This function processes only one user intent per call.

### `create_venues(data)`

Creates a list of `Venue` instances from the loaded JSON data.

- **Parameters**:
  - `data` (dict): The loaded JSON data.

- **Returns**:
  - `Venues` (list): A list of `Venue` instances.

### `main(file_path, plot_strategy=False, verbose=False)`

The main function of the project. It maximizes the surplus and creates an output JSON file.

- **Parameters**:
  - `file_path` (str): The path to the JSON file.
  - `plot_strategy` (bool, optional): If `True`, plots the strategy graph. Default is `False`.
  - `verbose` (bool, optional): If `True`, prints additional verbose information. Default is `False`.

- **Process**:
  1. Fetches intent content from the specified JSON file.
  2. Creates order and venues objects from the data collected.
  3. Creates the market graph from the venues information.
  4. Creates an agent that reads the order and the market, and creates the directed strategy graph containing all simple paths in the market that fulfill the order intent.
  5. Optimizes the strategy to maximize the surplus under the constraints identified by the user order.
  6. Creates an updated output JSON file.

### `add_venue_to_json(url, token1, token2, json_file, delete_tmp=True)`

Extracts liquidity data for specified tokens from a given URL and updates a JSON file with this information.

- **Parameters**:
  - `url` (str): The URL to fetch data from.
  - `token1` (str): The string of the first token.
  - `token2` (str): The string of the second token.
  - `json_file` (str): The path to the JSON intent file to be updated.
  - `delete_tmp` (bool, optional): Flag indicating whether to delete the temporary HTML file after processing. Defaults to `True`.

- **Process**:
  1. Fetches HTML content from the specified URL.
  2. Parses the HTML to extract liquidity values for the specified tokens.
  3. Updates the JSON file with the extracted liquidity values under a new venue name.
  4. Deletes the temporary HTML file if `delete_tmp` is set to `True`.

- **Note**:
  - The function assumes that the token liquidity values can be found in the HTML content with the format 'pooled {token} is {value}'.
  - The function handles the precision of token values by formatting them to 18 decimal places and replacing '.' with '_'.

## Usage

To run the main function, use the following command:

```sh
python script_name.py --file_path <path_to_json> [--plot_strategy] [--verbose]
