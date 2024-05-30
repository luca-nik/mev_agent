import json

class order:
    """
    A class to represent an order in a trading system.

    Attributes:
    -----------
    order_number : str
        The unique identifier for the order.
    sell_token : str
        The token being sold in the order.
    buy_token : str
        The token being bought in the order.
    limit_sell_amount : str
        The maximum amount of the sell token to sell.
    limit_buy_amount : str
        The minimum amount of the buy token to buy.
    partial_fill : bool
        Whether partial filling of the order is allowed.

    Methods:
    --------
    from_json(order_number, data):
        Creates an order instance from JSON data.
    format_with_underscore(value):
        Formats the atoms amount adding '_' after division 10**18
    print_info():
        Prints the order information in a JSON-like formatted string.
    """
    def __init__(self, order_number, sell_token, buy_token, limit_sell_amount, limit_buy_amount, partial_fill):
        self.order_number = order_number
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.limit_sell_amount = int(limit_sell_amount.replace("_", ""))
        self.limit_buy_amount = int(limit_buy_amount.replace("_", ""))
        self.partial_fill = partial_fill

    @staticmethod
    def from_json(order_number, data):
        """
        Constructs all the necessary attributes for the order object.

        Parameters:
        -----------
        order_number : str
            The unique identifier for the order.
        sell_token : str
            The token being sold in the order.
        buy_token : str
            The token being bought in the order.
        limit_sell_amount : str
            The maximum amount of the sell token to sell.
        limit_buy_amount : str
            The minimum amount of the buy token to buy.
        partial_fill : bool
            Whether partial filling of the order is allowed.
        """
        return order(
            order_number,
            data['sell_token'],
            data['buy_token'],
            data['limit_sell_amount'],
            data['limit_buy_amount'],
            data['partial_fill']
        )

    def format_with_underscore(self, value):
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
        Prints the order information in a JSON-like formatted string.
        """
        order_data = {
            self.order_number: {
                "sell_token": self.sell_token,
                "buy_token": self.buy_token,
                "limit_sell_amount": self.format_with_underscore(self.limit_sell_amount),
                "limit_buy_amount": self.format_with_underscore(self.limit_buy_amount),
                "partial_fill": self.partial_fill
            }

        }
        print(json.dumps(order_data, indent=4))
