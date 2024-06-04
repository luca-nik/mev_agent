# MEV_agent
This project involves developing a Maximal Extractable Value (MEV) agent designed to optimize order execution by matching a set of order intents with various potential liquidity sources. The goal is to maximize the order's surplus through optimal execution strategies.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)

## Overview

This project is designed to simulate a market with multiple trading venues, each with its own liquidity pool. The main components are:
- `Order`: Represents an order with user intent for trading.
- `Venue`: Represents a trading venue with token reserves.
- `Market`: Represents a market of trading venues, it is a graph with tokens at the vertices and venues at the edges.
- `Agent`: Represents a market agent that formulates and optimizes trading strategies.

The idea is that given a user `Order` containing the intent of buying `token2` selling `token1`, with the worst acceptable exchange rate, `Agent` will read `Market` and construct a `strategy` to exchange such tokens.

`strategy` is a directed graph connecting the nodes of the different tokens by means of edges, which are the venues where the tokens at the corresponding nodes can be exchanged. 
The graph direction is from `token1` to `token2`.

<div align="center">
  <img src="docs/images/example_strategy.png" alt="Diagram">
  <p style="margin-top: 10px;">Example of a strategy graph.</p>
</div>


Knowing the user intent, and the possible paths in the market connecting the desired user tokens, `Agent` can now search for the optimal coin exchange among the directed paths to maximize the user surplus. 

![Equation](docs/images/surplus_maximization_equation.png)

With `N` being the number of simple paths connecting `token1` with `token2` in the strategy graph. 

<div align="center">
  <img src="docs/images/example_strategy-paths.png" alt="Diagram">
  <p style="margin-top: 10px;">Example of a strategy graph where the coins sold and bought along the different channels are highlighted.</p>
</div>

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
To use the code we need first to add to the system path `path-to-src`, i.e. the path to the `src` folder containing the python codes.
Then we only need to import [`mev_project_interface`](docs/mev_project_interface.md) and run its procedure `main` specifying the JSON-file containing user orders and market venues.

### Example Usage

```python
import sys
import os
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'path-to-src')))
import mev_project_interface as mev_interface

# The JSON-file containing user orders and market venues
json_path = 'path-to-json/file.json'

# Run MEV agent optimization on the JSON containing user orders and venues.
mev_interface.main(json_path)

```


## Documentation

For detailed class documentation, please refer to [DOCUMENTATION](docs/DOCUMENTATION.md).

