import sys
import os
import argparse
import json
from matplotlib import pyplot as plt
import re
import requests
from bs4 import BeautifulSoup
import numpy as np

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
    -------
    data: dict
        The loaded data from the JSON file.
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
    --------
    Order: order instance
        Order object containing user intent 


    Note:
        - The function allow to gather only one user intent per time. 
    """


    for index in data['orders']:
        Order = order.from_json(index, data['orders'][index])
        break #We allow for simplicity only one order

    return Order

def create_venues(data):
    """
    Create a list of Venue instances from the loaded JSON data.

    Parameters:
    -----------
    data: dict
        The loaded JSON data.

    Returns:
    --------
    Venues: list
        A list of Venue instances.
    """
    Venues = []
    # Read venues from the file and gather data
    for venue_name, venue_info in data['venues'].items():
        Venue = venue.from_json(venue_name, venue_info['reserves'])
        Venues.append(Venue)

    return Venues

def main(file_path, plot_strategy=False, verbose=False):
    """
    Main function of the project. 
    It takes the input json file after having maximized the surpuls it creates an output json

    Parameters:
    -----------
    file_path : str
        The path to the JSON file.
    plot_strategy : bool, optional
        Plots the strategy graph
    verbose : bool, optional
        Prints additional verbose information

    The function performs the following steps:
    1. Fetches intent content from the specified json-file_path.
    2. Creates order and venues objects from the data collected
    3. Creates the market graph from the venues information
    4. Creates an agent that reads the order and the market and creates the directed strategy 
        graph containing all simple paths in the market that fulfill the order intent.
    5. The agent optimizes the strategy to maximize the surplus under the constraint
        identified by the user order. 
        In this case the agent will output the optimal sold and bought amounts via
        each path in the strategy graph.
    6. Creates an updated output json file.
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
    sold_amount, bought_amount = Agent.optimize_strategy()

    # Output results in JSON file
    Agent.print_results(file=file_path.split('.json')[0]+'-results.json')

def add_venue_to_json(url, token1, token2, json_file, delete_tmp=True):
    """
    Extracts liquidity data for specified tokens from a given URL and updates a JSON file with this information.

    Parameters:
    -----------
    url : str
        The URL to fetch data from.
    token1 : str
        The string of the first token.
    token2 : str
        The string of the second token.
    json_file : str
        The path to the JSON intent file to be updated.
    delete_tmp: bool, optional
        Flag indicating whether to delete the temporary HTML file after processing. Defaults to True.

    The function performs the following steps:
    1. Fetches HTML content from the specified URL.
    2. Parses the HTML to extract liquidity values for the specified tokens.
    3. Updates the JSON file with the extracted liquidity values under a new venue name.
    4. Deletes the temporary HTML file if delete_tmp is set to True.

    Note:
        - The function assumes that the token liquidity values can be found in the HTML content with the format 'pooled {token} is {value}'.
        - The function handles the precision of token values by formatting them to 18 decimal places and replacing '.' with '_'.
    """
    print('Loading data from ' + url)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the parsed HTML to a file
        with open('pool_data.html', 'w') as f:
            f.write(str(soup))

        # Read the file and process the content
        with open('pool_data.html', 'r') as file_:
            lines = file_.readlines()

        # Initialize values for token1 and token2
        token1_value = None
        token2_value = None

        # Iterate through each line to find the target value
        for line in lines:
            if f'pooled {token1}' in line:
                # Use regular expressions to find the values after 'pooled <token1>' and 'pooled <token2>'
                token1_match = re.search(rf'pooled {token1} is ([\d,\.]+)', line)
                token2_match = re.search(rf'pooled {token2} is ([\d,\.]+)', line)

                if token1_match and token2_match:
                    token1_value = np.float64(token1_match.group(1).replace(',', ''))
                    token2_value = np.float64(token2_match.group(1).replace(',', ''))

                    print(" ")
                    print(f"Extracted {token1} liquidity: {token1_value}")
                    print(f"Extracted {token2} liquidity: {token2_value}")
                    print(" ")
                else:
                    print("Values not found in the line")

        # Delete the file after processing
        if delete_tmp:
            os.remove('pool_data.html')
            print("Temporary 'pool_data.html' file storing pool information has been deleted.")

    # Load the existing JSON data
    json_file = 'data.json'
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Construct the venue name
    venue_name = f"METEORA_{token1}_{token2}"

    # Add the new section to the 'venues' key
    if token1_value is not None and token2_value is not None:
        data['venues'][venue_name] = {
            'reserves': {
                token1: f"{token1_value:.18f}".replace('.','_'),
                token2: f"{token2_value:.18f}".replace('.','_')
            }
        }

        # Save the updated JSON back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print("New venue " + venue_name + " added to the JSON file " + json_file)
    else:
        print("No valid token values were extracted.")

