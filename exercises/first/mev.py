import sys
import os
import argparse
import json

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from classes import order, venue


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def main(file_path):
    # Load data from JSON file
    data = load_data(file_path)

    # Create the order list and instance them from the JSON data
    #Orders = []
    #for index in data['orders'].keys():
    #    Order = []
    #    Order = order.from_json(str(index), data['orders'][str(index)])
    #    Orders.append(Order)
    #    Order.print_info()  # This will use the custom print_info method

    # Create the venu list and instance them from the JSON data
    #print(data['venues']['AMM_RHO_KAPPA'])
    venues_data = data['venues']

    for venue_name, venue_info in venues_data.items():
        Venue = venue.from_json(venue_name, venue_info['reserves'])
        Venue.print_info()
    #Venues = []
    #for index in data['venues'].keys():
    #    Order = []
    #    Order = order.from_json(str(index), data['venues'][str(index)])
    #    Orders.append(Order)
    #    Order.print_info()  # This will use the custom print_info method

    #venue = Venue.from_json(data['venues']['AMM_RHO_KAPPA'])

    #print(f"Venue Reserves: {venue.reserves}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a JSON file path.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    args = parser.parse_args()
    main(args.file_path)
