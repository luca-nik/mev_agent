# `venue` Class

The `venue` class is designed to represent a liquidity pool with token reserves. It encapsulates the details about the trading venue and its reserves.

## Attributes

- `name` (str): The name of the trading venue.
- `reserves` (dict): A dictionary containing the token reserves in the venue.

## Methods

### `__init__(self, name, reserves)`
Constructs all the necessary attributes for the venue object.

**Parameters:**
- `name` (str): The name of the trading venue.
- `reserves` (dict): A dictionary containing the token reserves in the venue.

### `from_json(name, data)`
Creates a venue instance from JSON data.

**Parameters:**
- `name` (str): The name of the trading venue.
- `data` (dict): The JSON data containing the venue's reserves.

**Returns:**
- `venue`: An instance of the `venue` class.

### `print_info(self)`
Prints the venue information in a JSON-like formatted string.

## Example Usage

```python
import json
import numpy as np

# Creating a venue instance using the constructor
venue1 = venue(
    name="Uniswap",
    reserves={
        "ETH": 100.0,
        "USDT": 50000.0
    }
)

# Creating a venue instance from JSON data
venue_data = {
    "ETH": "100_0",
    "USDT": "50000_0"
}
venue2 = venue.from_json("SushiSwap", venue_data)

# Printing venue information
venue1.print_info()
venue2.print_info()
