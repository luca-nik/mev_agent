# `agent` Class

The `agent` class represents a market agent that reads user intent, analyzes the market, and formulates the optimal Maximal Extractable Value (MEV) strategy.

## Attributes

- `order` (order): An `order` object to store the current order information.
- `venues` (list): A list containing venue instances.
- `strategy` (nx.DiGraph): A directed graph of token (vertices) and venues (edges) from `sell_token` to `buy_token`.
- `paths` (list): A list of the paths from `sell_token` to `buy_token`.

## Methods

### `__init__(self)`
Constructs all the necessary attributes for the agent object.

### `read_order(self, Order)`
Reads an order object and stores the associated information.

**Parameters:**
- `order` (order): The order object containing the user intent.

### `print_order(self)`
Prints the current order information.

### `read_market(self, market, verbose=False)`
Evaluates paths in the market connecting `sell_token` with `buy_token` of the current order. Identifies the venues to visit and the sell and buy tokens for each venue.

**Parameters:**
- `market` (Market): The market object containing the graph of tokens and venues.
- `verbose` (bool, optional): Prints additional information. Default is `False`.

### `make_strategy(self, path, market, verbose=False)`
Given a market path, identifies the venues to visit and the sell and buy tokens for each venue. Constructs the strategy graph and stores the edges for future propagation.

**Parameters:**
- `path` (list): The list of tokens representing the path.
- `market` (Market): The market object containing the graph of tokens and venues.
- `verbose` (bool, optional): Prints additional information. Default is `False`.

### `plot_strategy(self)`
Plots the strategy graph using matplotlib.

### `propagate_along(self, path, initial_sell_coin_amount)`
Propagates `initial_sell_coin_amount` through the path, outputting the resulting amount of coins bought.

**Parameters:**
- `path` (list): The list of nodes representing the path.
- `initial_sell_coin_amount` (float): The initial amount of coins to sell at the beginning of the path.

**Returns:**
- `float`: The final value after propagation (i.e., the amount of `buy_coin` of the order bought along that path).

### `optimize_strategy(self)`
Optimizes the strategy to maximize the order surplus.

**Returns:**
- `tuple`: The optimal sell amounts and the resulting buy amounts.

### `update_venues(self, optimal_coins_sell)`
Updates the venues' reserves based on the optimal coins to sell along each path.

**Parameters:**
- `optimal_coins_sell` (list): A list of amounts of initial coins to sell along each path.

### `print_results(self, file=None)`
Prints the result of the surplus maximization.

**Parameters:**
- `file` (str, optional): The file path where the output should be written. If `None`, the output is printed to the console.

## Example Usage

```python
import networkx as nx
from matplotlib import pyplot as plt
from .venue import venue
from .order import order
from .market import market
from .agent import agent

# Create some venue instances
venue1 = venue(
    name="Uniswap",
    reserves={
        "ETH": 100.0,
        "USDT": 50000.0
    }
)

venue2 = venue(
    name="SushiSwap",
    reserves={
        "ETH": 150.0,
        "DAI": 60000.0
    }
)

# Create an order instance
order_instance = order(
    order_number="12345",
    sell_token="ETH",
    buy_token="USDT",
    limit_sell_amount="1.0",
    limit_buy_amount="3000.0",
    partial_fill=True
)

# Create a market instance
market_instance = market([venue1, venue2])

# Create an agent instance
agent_instance = agent()

# Read the order
agent_instance.read_order(order_instance)

# Read the market and generate strategy
agent_instance.read_market(market_instance, verbose=True)

# Plot the strategy
agent_instance.plot_strategy()

# Optimize the strategy
optimal_sell, optimal_buy, total_buy = agent_instance.optimize_strategy()

# Print the results
agent_instance.print_results()
