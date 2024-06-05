import sys
import os
import argparse
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from classes import order, venue, market, agent

def load_data(file_path):
    """
    Load data from a JSON file.

    Parameters:
    -----------
    file_path : str 
        The path to the JSON file.

    Returns:
    dict: The loaded data from the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_path}.")
        sys.exit(1)

def create_order(data):
    """
    Create a list of Order instances from the loaded JSON data.

    Parameters:
    -----------
    data: dict 
        The loaded JSON data.

    Returns:
    order: a order instance
    """
    for index in data['orders']:
        Order = order.from_json(index, data['orders'][index])
        break
    return Order

def create_venues(data):
    """
    Create a list of Venue instances from the loaded JSON data.

    Parameters:
    -----------
    data: dict
        The loaded JSON data.

    Returns:
    list: A list of Venue instances.
    """
    Venues = []
    for venue_name, venue_info in data['venues'].items():
        Venue = venue.from_json(venue_name, venue_info['reserves'])
        Venues.append(Venue)
    return Venues

def main(file_path, plot_strategy=False, verbose=False):
    """
    Main function to process the JSON file and create the market graph.

    Parameters:
    -----------
    file_path : str
        The path to the JSON file.
    plot_strategy : bool, optional
        Plots the strategy graph
    verbose : bool, optional
        Prints additional verbose information
    """
    # Load data from JSON file
    data = load_data(file_path)

    # Create Orders and Venues from JSON data
    Order = create_order(data)
    Venues = create_venues(data)

    # Initialize the market graph from the list of venues
    Market = market(Venues)

    # Initialize Agent and read the first order
    Agent = agent()
    Agent.read_order(Order)

    # Read market data and create strategy graph
    Agent.read_market(Market, verbose = verbose)
    if plot_strategy:
        Agent.plot_strategy()

    # Optimize the strategy
    optimal_values, optimal_b_values, optimal_b_sum = Agent.optimize_strategy()

    # Output results in JSON file
    Agent.print_results(file=file_path.split('.json')[0]+'-results.json')
