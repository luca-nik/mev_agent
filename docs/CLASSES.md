This file contains detailed documentation about the classes employed in this project

## Table of Contents
  - [order Class](#order-class)
  - [venue Class](#venue-class)
  - [market Class](#market-class)
  - [agent Class](#agent-class)

## `order` Class

The `order` class is designed to represent a user order in a trading system. It encapsulates all necessary details about the order, including the tokens being traded, the amounts, and whether partial fills are allowed.

### Attributes

- `order_number` (str): The unique identifier for the order.
- `sell_token` (str): The token being sold in the order.
- `buy_token` (str): The token being bought in the order.
- `limit_sell_amount` (float): The maximum amount of the `sell_token` to sell.
- `limit_buy_amount` (float): The minimum amount of the `buy_token` to buy.
- `partial_fill` (bool): Whether partial filling of the order is allowed.
- `ex_sell_amount` (float): The executed amount of the `sell_token` sold.
- `ex_buy_amount` (float): The executed amount of the `buy_token` bought.

### Methods

#### `__init__(self, order_number=None, sell_token=None, buy_token=None, limit_sell_amount='0_0', limit_buy_amount='0_0', partial_fill=False, ex_sell_amount='0_0', ex_buy_amount='0_0')`
  - Initializes a new instance of the `order` class.
  - **Parameters:**
    - `order_number` (str, optional): The unique identifier for the order.
    - `sell_token` (str, optional): The token being sold in the order.
    - `buy_token` (str, optional): The token being bought in the order.
    - `limit_sell_amount` (str, optional): The maximum amount of the `sell_token` to sell.
    - `limit_buy_amount` (str, optional): The minimum amount of the `buy_token` to buy.
    - `partial_fill` (bool, optional): Whether partial filling of the order is allowed.
    - `ex_sell_amount` (str, optional): The executed amount of the `sell_token` sold.
    - `ex_buy_amount` (str, optional): The executed amount of the `buy_token` bought.

#### `from_json(order_number, data)`
  - Creates an `order` instance from JSON data.
  - **Parameters:**
    - `order_number` (str): The unique identifier for the order.
    - `data` (dict): The JSON data containing the order details.
  - **Returns:** An instance of the `order` class.

#### `print_info(self, file=None)`
  - Prints the order information in a JSON-like formatted string. If a file path is provided, writes the output to the file.
  - **Parameters:**
    - `file` (str, optional): The file path where the output should be written. If `None`, prints to console.

### Example Usage

```python
import json

# Creating an order instance using the constructor
order1 = order(
    order_number="12345",
    sell_token="BTC",
    buy_token="ETH",
    limit_sell_amount="1_0",
    limit_buy_amount="30_0",
    partial_fill=True
)

# Creating an order instance from JSON data
order_data = {
    "sell_token": "BTC",
    "buy_token": "ETH",
    "limit_sell_amount": "1_0",
    "limit_buy_amount": "30_0",
    "partial_fill": True
}
order2 = order.from_json("12346", order_data)

# Printing order information
order1.print_info()
order2.print_info(file="order_info.json")
```
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


