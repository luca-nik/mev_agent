# `agent` Class Documentation

## Overview

The `agent` class represents a market agent that reads user intent, evaluates the market, and formulates the optimal MEV strategy. This class manages orders, venues, and strategies to optimize trades within a given market.

## Attributes

- **order**: `order`  
  An `order` object to store the current order information.

- **venues**: `list`  
  A list containing venue instances.

- **strategy**: `nx.DiGraph`  
  A directed graph to store the paths from `sell_token` to `buy_token`, called the strategy.

- **paths**: `list`  
  A list of the paths from `sell_token` to `buy_token`.

## Methods

### `__init__()`

Constructs all the necessary attributes for the agent object.

### `read_order(Order)`

Reads an order object and stores the associated information.

- **Parameters**:  
  - `Order`: The order object containing the user intent.

### `print_order()`

Prints the current order information.

### `read_market(market, verbose=True)`

Evaluates paths in the market connecting `sell_token` with `buy_token` of the current order. Identifies the venues to visit and the sell and buy tokens for each venue. Calls `make_strategy()` to create the strategy graph and the paths the agent needs to follow.

- **Parameters**:  
  - `market`: The market object containing the graph of tokens and venues.
  - `verbose`: (Optional) Print additional information. Default is `True`.
 
- **Process**:
  1. Initializes a split variable to handle multigraphs.
  2. Iterates over each pair of consecutive tokens in the path.
  3. Checks if there is an edge between the token pair in the market graph.
  4. Gathers edge data from the market graph, including venues and liquidity information, and defines the price function.
  5. Constructs or updates the strategy graph:
     - Gathers relevant information for each venue in the edge.
     - Prints information if `verbose` is `True`.
     - Updates the strategy graph, handling multigraphs by appending new variables if an edge already exists.
  6. Checks if the multigraph is too complex and exits if it is.
  7. Stores paths in `self.paths`. These are the edges, i.e., venues, that are visited along a specific coin path (A -> C -> B).

- **Note**:
  - Each edge of the strategy graph will be associated with a `sell_token` and a `buy_token` uniquely defined from the directionality of the graph. This allows assigning to each edge the proper `price_function`

### `make_strategy(path, market, verbose=False)`

Given a path in the market, identifies the venues to visit and the sell and buy tokens for each venue. Constructs the strategy graph (tokens as nodes and venues as edges) and creates the `self.paths` list.

- **Parameters**:  
  - `path`: The list of tokens representing the path.
  - `market`: The market object containing the graph of tokens and venues.
  - `verbose`: (Optional) Prints additional information. Default is `False`.
 
- **Process**:
  1. Calculates the worst acceptable exchange rate based on the order's limit sell and buy amounts.
  2. Defines a surplus function to be maximized:
     - The surplus is a function of the coins sold and bought through each path.
     - Along each path, the amount of coins bought is obtained with the `propagate_along()` function.
  3. Defines constraints:
     - Ensures the total sell amount does not exceed the limit sell amount and the total buy amount meets or exceeds the limit buy amount.
     - If the order allows partial fills, sets an inequality constraint for the sell amount; otherwise, sets an equality constraint for a fill-or-kill order.
  4. Runs optimization:
     - Uses the SLSQP method to minimize the negative surplus (maximize surplus) within the specified bounds and constraints.
  5. Extracts and computes results:
     - Extracts the optimal sell amounts and computes the resulting buy amounts.
     - Computes the coin conservation error to check for discrepancies.
     - Prints optimization results and detailed information for each path.
  6. Updates order and venues information:
     - Updates the order with the executed sell and buy amounts.
     - Updates the venues with the optimal sell amounts.


### `plot_strategy()`

Plots the strategy graph using matplotlib.

### `propagate_along(path, initial_sell_coin_amount)`

Propagates an initial amount of coins sold through the chain of venues stored in `path`, outputting the amount of coins bought at the end of the path.

- **Parameters**:  
  - `path`: The list of edges of the strategy graph representing the path along which we propagate.
  - `initial_sell_coin_amount`: The initial amount of coins to sell at the beginning of the path.

- **Returns**:  
  - `float`: The final value after propagation (i.e., the amount of buy_coin of the order bought along that path).

### `optimize_strategy()`

Optimizes the strategy to maximize the order surplus by defining a surplus function to be maximized, setting constraints, and using the SLSQP method to find the optimal solution.

- **Returns**:  
  - `tuple`: The optimal sell amounts and the resulting buy amounts.

- **Process**:
  1. Calculates the worst acceptable exchange rate based on the order's limit sell and buy amounts.
  2. Defines a surplus function to be maximized:
     - The surplus is a function of the coins sold and bought through each path.
     - Along each path, the amount of coins bought is obtained with the `propagate_along()` function.
  3. Defines constraints:
     - Ensures the total sell amount does not exceed the limit sell amount and the total buy amount meets or exceeds the limit buy amount.
     - If the order allows partial fills, sets an inequality constraint for the sell amount; otherwise, sets an equality constraint for a fill-or-kill order.
  4. Runs optimization:
     - Uses the SLSQP method to minimize the negative surplus (maximize surplus) within the specified bounds and constraints.
  5. Extracts and computes results:
     - Extracts the optimal sell amounts and computes the resulting buy amounts.
     - Computes the coin conservation error to check for discrepancies.
     - Prints optimization results and detailed information for each path.
  6. Updates order and venues information:
     - Updates the order with the executed sell and buy amounts.
     - Updates the venues with the optimal sell amounts.


### `update_venues(optimal_coins_sell)`

Updates the venues' reserves based on the optimal coins to sell along each path.

- **Parameters**:  
  - `optimal_coins_sell`: A list of amounts of initial coins to sell along each path. The length of this list should be equal to the number of paths of the strategy.

### `print_results(file=None)`

Prints the result of the surplus maximization, either to the console or to a specified file.

- **Parameters**:  
  - `file`: (Optional) The file path where the output should be written. If `None`, the output is printed to the console.

---

