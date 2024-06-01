# MEV_agent
This project involves developing a Maximal Extractable Value (MEV) agent designed to optimize order execution by matching a set of order intents with various potential liquidity sources. The goal is to maximize the order's surplus through optimal execution strategies.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Venue Class](#venue-class)
  - [Market Class](#market-class)
  - [Agent Class](#agent-class)
- [API Reference](#api-reference)
  - [Venue](#venue)
  - [Market](#market)
  - [Agent](#agent)
  - [Order](#order)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is designed to simulate a market with multiple trading venues, each with its own liquidity pools. The main components are:
- `Venue`: Represents a trading venue with token reserves.
- `Market`: Represents a market of trading venues and generates a graph of token pairs.
- `Agent`: Represents a market agent that formulates and optimizes trading strategies.
- `Order`: Represents an order with user intent for trading.

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
