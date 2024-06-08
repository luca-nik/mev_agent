import json
import numpy as np
import copy

class order:
    """
    A class to represent a user order in a trading system.

    Attributes:
    -----------
    order_number : str
        The unique identifier for the order.
    sell_token : str
        The token being sold in the order.
    buy_token : str
        The token being bought in the order.
    limit_sell_amount : str
        The maximum amount of the sell_token to sell.
    limit_buy_amount : str
        The minimum amount of the buy_token to buy.
    partial_fill : bool
        Whether partial filling of the order is allowed.

    Methods:
    --------
    from_json(order_number, data):
        Creates an order instance from JSON data.
    print_info():
        Prints the order information in a JSON-like formatted string.
    """
    def __init__(self, order_number=None, sell_token=None, buy_token=None, limit_sell_amount='0_0', 
                 limit_buy_amount='0_0', partial_fill=False, ex_sell_amount='0_0', ex_buy_amount='0_0'):
        self.order_number = order_number
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.limit_sell_amount = np.float64(limit_sell_amount.replace("_", "."))
        self.limit_buy_amount =  np.float64(limit_buy_amount.replace("_", "."))
        self.partial_fill = partial_fill
        self.ex_sell_amount = ex_sell_amount
        self.ex_buy_amount = ex_buy_amount

    @staticmethod
    def from_json(order_number, data):
        """
        Constructs all the necessary attributes for the order object.

        Parameters:
        -----------
        order_number : str
            The unique identifier for the order.
        data : dict
            The JSON data containing the order details.

        Returns:
        --------
        Order
            An instance of the Order class.
        """

        Order = order()
        Order.order_number = order_number

        if 'sell_token' in data:
            Order.sell_token = data['sell_token']
        else:
            Order.sell_token = None

        if 'buy_token' in data:
            Order.buy_token = data['buy_token']
        else:
            Order.buy_token = None

        if 'limit_sell_amount' in data:
            Order.limit_sell_amount = np.float64(data['limit_sell_amount'].replace("_", "."))
        else:
            Order.limit_sell_amount = 0.0

        if 'limit_buy_amount' in data:
            Order.limit_buy_amount = np.float64(data['limit_buy_amount'].replace("_", "."))
        else:
            Order.limit_buy_amount = 0.0

        if 'partial_fill' in data:
            Order.partial_fill = data['partial_fill']
        else:
            Order.partial_fill = False

        if 'sell_amount' in data:
            Order.limit_sell_amount = np.float64(data['sell_amount'].replace("_","."))

        if 'buy_amount' in data:
            Order.limit_buy_amount = np.float64(data['buy_amount'].replace("_","."))

        if 'ex_sell_amount' in data:
            Order.ex_sell_amount = np.float64(data['ex_sell_amount'].replace("_","."))
        else:
            Order.ex_sell_amount = 0.0

        if 'ex_buy_amount' in data:
            Order.ex_buy_amount = np.float64(data['ex_buy_amount'].replace("_","."))
        else:
            Order.ex_buy_amount = 0.0

        return Order

    def print_info(self,file=None):
        """
        Prints the order information in a JSON-like formatted string.
        If a file path is provided, writes the output to the file.

        Parameters:
        -----------
        file : str, optional
            The file path where the output should be written. If None, prints to console.
        """
        if self.ex_sell_amount == 0.0:
            order_data = {
                self.order_number: {
                    "sell_token": self.sell_token,
                    "buy_token": self.buy_token,
                    "limit_sell_amount": f"{self.limit_sell_amount:.18f}".replace(".", "_"),
                    "limit_buy_amount": f"{self.limit_buy_amount:.18f}".replace(".","_"),
                    "partial_fill": self.partial_fill
                }
            }
        else:
            order_data = {
                self.order_number: {
                    "sell_token": self.sell_token,
                    "buy_token": self.buy_token,
                    "limit_sell_amount": f"{self.limit_sell_amount:.18f}".replace(".", "_"),
                    "limit_buy_amount": f"{self.limit_buy_amount:.18f}".replace(".","_"),
                    "partial_fill": self.partial_fill,
                    "ex_sell_amount": f"{self.ex_sell_amount:.18f}".replace(".","_"),
                    "ex_buy_amount":  f"{self.ex_buy_amount:.18f}".replace(".","_")
                }
            }

        output = json.dumps(order_data, indent=4)

        # If requested write a file, otherwise print to screen the information
        if file:
            with open(file, 'w') as f:
                f.write(output)
        else:
            print(output)
