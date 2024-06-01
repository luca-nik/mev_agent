import sys
import os
import argparse
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from classes import order, venue, market, agent


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def main(file_path):
    # Load data from JSON file
    data = load_data(file_path)

    # Create the Orders list and instance them from the JSON data
    Orders = []
    for index in data['orders'].keys():
        Order = []
        Order = order.from_json(str(index), data['orders'][str(index)])
        Orders.append(Order)
        #Order.print_info()

    # Create the Venues list and instance them from the JSON data
    venues_data = data['venues']
    Venues = []
    for venue_name, venue_info in venues_data.items():
        Venue = []
        Venue = venue.from_json(venue_name, venue_info['reserves'])
        #Venue.print_info()
        Venues.append(Venue)

    # Initialize the market graph from the list of venues
    Market = market(Venues)
    #Market.print_graph_info()
    #Market.plot_graph()
    
    # 
    Agent = agent()
    Agent.read_order(Orders[0])

    # Print stored intents
    #Agent.print_order()
    Agent.read_market(Market)
    #Agent.plot_strategy()
    optimal_values, optimal_b_values, optimal_b_sum = Agent.optimize_strategy()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a JSON file path.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    args = parser.parse_args()
    main(args.file_path)

