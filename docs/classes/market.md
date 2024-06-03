# `market` Class

The `market` class represents a market of trading venues as a non-directed graph. It encapsulates the details about the trading venues and provides methods to generate and plot the graph, as well as calculate token prices based on different Automated Market Maker (AMM) mechanisms.

## Attributes

- `venues` (list): A list containing venue instances.
- `graph` (networkx.Graph): A graph where each unique coin is a node and each reserve acts as an edge.

## Methods

### `__init__(self, venues)`
Constructs all the necessary attributes for the market object.

**Parameters:**
- `venues` (list): A list containing venue instances.

### `generate_graph(self)`
Generates a graph from the venues.

### `plot_graph(self, file=None, verbose=False)`
Plots the graph using matplotlib. If a file path is provided, the plot is saved to the file.

**Parameters:**
- `file` (str, optional): The path to save the plot image. If `None`, the plot is displayed.
- `verbose` (bool, optional): If `True`, prints details about the graph nodes and edges. Default is `False`.

### `price_function(coin_amount, liquidity_sell_token, liquidity_buy_token, market_type='constant_product', what_='buy')`
Calculate the amount of tokens bought in a specific liquidity pool given the sell amount, the type of Automated Market Maker (AMM) of the pool, and the initial liquidities of the buy and sell tokens.

**Parameters:**
- `coin_amount` (int): The amount of the token either bought or sold by the AMM.
- `liquidity_sell_token` (int): The current liquidity of the sell token in the liquidity pool.
- `liquidity_buy_token` (int): The current liquidity of the buy token in the liquidity pool.
- `market_type` (str, optional): The type of AMM mechanism used by the liquidity pool. Default is `'constant_product'`. Supported values:
  - `'constant_product'`: Uses the constant product formula (`x * y = k`) for price calculation.
- `what_` (str, optional): The type of operation performed by the AMM. Supported values:
  - `'buy'`, `'sell'` if AMM either is buying or selling.

**Returns:**
- `float`: The calculated amount of buy tokens received for the given sell amount.

**Raises:**
- `ValueError`: If an unsupported market type is provided.

## Example Usage

```python
import networkx as nx
from .venue import venue
from matplotlib import pyplot as plt

# Creating a market instance with venues
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

market_instance = market([venue1, venue2])

# Generating and plotting the market graph
market_instance.plot_graph(verbose=True)

# Calculating the price using the price function
buy_amount = market_instance.price_function(coin_amount=10, liquidity_sell_token=100, liquidity_buy_token=200, market_type='constant_product', what_='buy')
print(f"Buy amount: {buy_amount}")

sell_amount = market_instance.price_function(coin_amount=10, liquidity_sell_token=100, liquidity_buy_token=200, market_type='constant_product', what_='sell')
print(f"Sell amount: {sell_amount}")
