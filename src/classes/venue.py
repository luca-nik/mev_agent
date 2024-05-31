# venue.py
import json
import numpy as np

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
    format_with_underscore(value):
        Formats the atoms amount adding '_' after division 10**18
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

    def format_with_underscore(self, value): #TODO
        """
        Formats the atoms amount adding '_' after division 10**18

        Parameters:
        -----------
        value : str
            The amount of atoms in string format

        Returns:
        --------
        str
            The formatted string of atoms.
        """
        value_str = str(value)
        if len(value_str) > 18:
            pos = len(value_str) - 18
            formatted_value = value_str[:pos] + '_' + value_str[pos:]
        else:
            formatted_value = value_str()
        return formatted_value

    def print_info(self):
        """
        Prints the venue information in a JSON-like formatted string.
        """
        formatted_reserves = {token: self.format_with_underscore(amount) for token, amount in self.reserves.items()}
        venue_data = {
            self.name: {
                "reserves": formatted_reserves
            }
        }
        print(json.dumps(venue_data, indent=4))
