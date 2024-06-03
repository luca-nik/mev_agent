# venue.py
import json
import numpy as np
import copy
import sys

class venue:
    """
    A class to represent a liquidity pool with token reserves.
    
    Attributes:
    -----------
    name : str
        The name of the trading venue.
    reserves : dict
        A dictionary containing the token reserves in the venue.
    
    Methods:
    --------
    from_json(name, data):
        Creates a venue instance from JSON data.
    print_info():
        Prints the venue information in a JSON-like formatted string.
    """
    
    def __init__(self, name, reserves):
        """
        Constructs all the necessary attributes for the venue object.
        
        Parameters:
        -----------
        name : str
            The name of the trading venue.
        reserves : dict
            A dictionary containing the token reserves in the venue.
        """
        self.name = name
        self.reserves = reserves

    @staticmethod
    def from_json(name, data):
        """
        Creates a venue instance from JSON data.
        
        Parameters:
        -----------
        name : str
            The name of the trading venue.
        data : dict
            The JSON data containing the venue's reserves.
        
        Returns:
        --------
        venue
            An instance of the venue class.
        """
        reserves = {token: np.float64(data[token].replace("_", ".")) for token in data}
        return venue(name, reserves)


    def print_info(self):
        """
        Prints the venue information in a JSON-like formatted string.
        """
        formatted_reserves = {token: f"{amount:.18f}".replace(".","_") for token, amount in self.reserves.items()}
        venue_data = {
            self.name: {
                "reserves": formatted_reserves
            }
        }
        print(json.dumps(venue_data, indent=4))
