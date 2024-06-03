# MEV_agent
This project involves developing a Maximal Extractable Value (MEV) agent designed to optimize order execution by matching a set of order intents with various potential liquidity sources. The goal is to maximize the order's surplus through optimal execution strategies.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is designed to simulate a market with multiple trading venues, each with its own liquidity pools. The main components are:
- `Order`: Represents an order with user intent for trading.
- `Venue`: Represents a trading venue with token reserves.
- `Market`: Represents a market of trading venues, it is a graph with tokens at the vertices and venues at the edges.
- `Agent`: Represents a market agent that formulates and optimizes trading strategies.

The idea is that given a user `Order` containing the intent of buying `token1` selling `token2`, with the worst acceptable exchange rate, `Agent` will read `Market` and construct a `strategy` to exchange such tokens.
`strategy` is a directed graph connecting the nodes of the different tokens by means of edges, which are the venues where the tokens at the corresponding nodes can be exchanged. 
The graph direction is from `token1` to `token2`.

Knowing the user intent, and the possible paths in the market connecting the desired user tokens, `Agent` can now search for the optimal coin exchange among the directed paths to maximize the user surplus. 


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/mev_agent.git
    cd mev_agent
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

## Documentation

For detailed class documentation, please refer to [CLASSES.md](docs/CLASSES.md).

### `order` Class

The `order` class is designed to represent a user order in a trading system. It encapsulates all necessary details about the order, including the tokens being traded, the amounts, and whether partial fills are allowed.

#### Attributes

- `order_number` (str): The unique identifier for the order.
- `sell_token` (str): The token being sold in the order.
- `buy_token` (str): The token being bought in the order.
- `limit_sell_amount` (float): The maximum amount of the `sell_token` to sell.
- `limit_buy_amount` (float): The minimum amount of the `buy_token` to buy.
- `partial_fill` (bool): Whether partial filling of the order is allowed.
- `ex_sell_amount` (float): The exact amount of the `sell_token` sold (if available).
- `ex_buy_amount` (float): The exact amount of the `buy_token` bought (if available).

#### Methods

- `__init__(self, order_number=None, sell_token=None, buy_token=None, limit_sell_amount='0_0', limit_buy_amount='0_0', partial_fill=False, ex_sell_amount='0_0', ex_buy_amount='0_0')`
  - Initializes a new instance of the `order` class.
  - **Parameters:**
    - `order_number` (str, optional): The unique identifier for the order.
    - `sell_token` (str, optional): The token being sold in the order.
    - `buy_token` (str, optional): The token being bought in the order.
    - `limit_sell_amount` (str, optional): The maximum amount of the `sell_token` to sell.
    - `limit_buy_amount` (str, optional): The minimum amount of the `buy_token` to buy.
    - `partial_fill` (bool, optional): Whether partial filling of the order is allowed.
    - `ex_sell_amount` (str, optional): The exact amount of the `sell_token` sold.
    - `ex_buy_amount` (str, optional): The exact amount of the `buy_token` bought.

- `from_json(order_number, data)`
  - Creates an `order` instance from JSON data.
  - **Parameters:**
    - `order_number` (str): The unique identifier for the order.
    - `data` (dict): The JSON data containing the order details.
  - **Returns:** An instance of the `order` class.

- `print_info(self, file=None)`
  - Prints the order information in a JSON-like formatted string. If a file path is provided, writes the output to the file.
  - **Parameters:**
    - `file` (str, optional): The file path where the output should be written. If `None`, prints to console.

#### Example Usage

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


### Venue Class

```python
from src.classes.venue import venue

# Sample JSON data
json_data = {
    "ETH": "1000_123456789012345678",
    "DAI": "5000_987654321098765432"
}

# Create a venue instance
my_venue = venue.from_json("MyTradingVenue", json_data)

# Print venue information
my_venue.print_info()
```
### Market Class
```python
from src.classes.market import market
from src.classes.venue import venue

# Sample JSON data
json_data_1 = {
    "ETH": "1000_123456789012345678",
    "DAI": "5000_987654321098765432"
}

json_data_2 = {
    "BTC": "2000_987654321012345678",
    "USDT": "8000_123456789098765432"
}

# Create venue instances
venue1 = venue.from_json("Venue1", json_data_1)
venue2 = venue.from_json("Venue2", json_data_2)

# Create a market instance
my_market = market([venue1, venue2])

# Print graph information
my_market.print_graph_info()

# Plot the market graph
my_market.plot_graph()

```
