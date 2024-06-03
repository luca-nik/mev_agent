import networkx as nx
from matplotlib import pyplot as plt
import sys
from scipy.optimize import minimize, Bounds
import copy
import numpy as np
import json

class agent:
    """
    A class to represent a market agent that reads the user intent, reads the market
    and formulates the optimal MEV strategy.
    
    Attributes:
    -----------
    order : order
        A order object to store the current order information.
    venues : list
        A list containing venue instances.
    strategy : nx.DiGraph
        A directed graph to store the paths from sell_token to buy_token, we call it strategy
    paths : list
        A list of the paths from sell_token to buy_token
    
    Methods:
    --------
    read_order(order):
        Reads an order object and stores the associated information.
    print_order():
        Prints the current order information.
    read_market(market, verbose):
        Reads the market graph and given the user order, it calls make_strategy to identify the correct paths
    make_strategy(path, market, verbose):
        Construct the directed graph called strategy, storing all path information and connected price_functions
    plot_strategy():
        Plots the strategy graph using matplotlib.
    propagate_along(path, initial_sell_coin_amount):
        Propagates initial_sell_coin_amount through path outputting the resulting amount of coins bought
        
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the agent object.
        """
        self.order = None
        self.venues = None
        self.strategy = None
        self.paths = None

    def read_order(self, Order):
        """
        Reads an order object and stores the associated information.
        
        Parameters:
        -----------
        order : order
            The order object containing the user intent.
        """
        self.order = copy.copy(Order)

    def print_order(self):
        """
        Prints the current order information.
        """
        if self.order:
            print("Current order:")
            print(self.order)
        else:
            print("No order found.")

    def read_market(self, market, verbose = False):
        """
        Evaluates paths in the market connecting sell_token with buy_token of the current order.
        Identifies the venues to visit and the sell and buy tokens for each venue.
        
        Parameters:
        -----------
        market : Market
            The market object containing the graph of tokens and venues.
        verbose: bool
            Print additional information
        """
        if not self.order:
            print("No order to evaluate.")
            return

        sell_token = self.order.sell_token
        buy_token =  self.order.buy_token
        self.venues = copy.copy(market.venues)
        try:
            # Gett all simple paths from initial sell_token to final buy_token
            paths = list(nx.all_simple_paths(market.graph, source=sell_token, target=buy_token))
            if paths:
                # Initialize the strategy graph
                self.strategy = nx.DiGraph()
                self.paths = []
                if verbose:
                    print(f"Paths from {sell_token} to {buy_token} for order {self.order['order_number']}:")
                for path in paths:
                    if verbose:
                        print(" -> ".join(path))
                    
                    # Make the strategy graph and store the strategy information
                    self.make_strategy(path, market, verbose = verbose)
            else:
                print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")
        except nx.NetworkXNoPath:
            print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")

    def make_strategy(self, path, market, verbose = False):
        """
        Given a market path, it identifies the venues to visit and the sell and buy tokens for each venue.
        It constructs the strategy graph. It stores the edges of the graphs for future propagation

        NOTE:
          Each edge of the strategy graph will be associated to a sell_token and to a buy_token uniquely defined 
          from the directionality of the graph. This allows to assign to each edge the proper price_function.
        
        Parameters:
        -----------
        path : list
            The list of tokens representing the path.
        market : Market
            The market object containing the graph of tokens and venues.
        verbose: bool
            Prints additional information
        """
        for i in range(len(path) - 1):
            token1 = path[i]
            token2 = path[i + 1]
            if market.graph.has_edge(token1, token2):
                edge_data = market.graph[token1][token2]
                venues = edge_data['venues']
                for venue in venues:
                    liquidity_sell_token = edge_data['liquidity_token1']
                    liquidity_buy_token = edge_data['liquidity_token2']
                    if verbose:
                        print(f"Venue: {venue}, Sell Token: {token1}, Buy Token: {token2}, Liquidity: {liquidity_sell_token} {token1}, {liquidity_buy_token} {token2}")

                    # Construct strategy graph, assign the price_function to the edge (constant product AMM)
                    self.strategy.add_edge(token1, token2, sell_token=token1, buy_token=token2, venue=venue, price_function=market.price_function,
                                           liquidity_sell_token=liquidity_sell_token, 
                                           liquidity_buy_token=liquidity_buy_token)

        # Store the paths where the agent will have to propagate
        edges = [self.strategy.edges[path[i], path[i+1]] for i in range(len(path)-1)]
        self.paths.append(edges)

    def plot_strategy(self):
        """
        Plots the strategy graph using matplotlib.
        """
        if self.strategy is None or self.strategy.number_of_nodes() == 0:
            print("No strategy to plot.")
            return

        pos = nx.spring_layout(self.strategy)  # positions for all nodes
        plt.figure(figsize=(10, 8))

        # Draw nodes
        nx.draw(self.strategy, pos, with_labels=True, node_size=7000, node_color='lightblue', font_size=12, font_family='sans-serif', arrows=True)

        # Draw edge labels
        edge_labels = {(u, v): f"{data['venue']}" for u, v, data in self.strategy.edges(data=True)}
        nx.draw_networkx_edge_labels(self.strategy, pos, edge_labels=edge_labels, font_size=10, font_family='sans-serif')

        plt.title("Strategy Graph")
        plt.show()


    def propagate_along(self, path, initial_sell_coin_amount):
        """
        Propagates initial_sell_coin_amount through path outputting the resulting amount of coins bought

        Parameters:
        -----------
        path : list
            The list of nodes representing the path.
        initial_sell_coin_amount : float
            The initial amount of coins to sell at the beginning of the path

        Returns:
        --------
        float
            The final value after propagation (i.e. the amount of buy_coin of the order bought along that path)
        """
        current_value = initial_sell_coin_amount
        for edge_data in path:
            current_value = edge_data['price_function'](current_value, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'])
            current_value = current_value

        return current_value

    def optimize_strategy(self):
        """
        Optimizes the strategy to maximize the order surplus
        
        Returns:
        --------
        tuple
            The optimal sell amounts and the resulting buy amounts.
        """
        
        # Compute the worst exchange rate acceptable
        exch_rate = self.order.limit_sell_amount/self.order.limit_buy_amount

        # Define the surplus function to be maximized
        def surplus(x):
            total_b = [0.0]*len(self.paths)
            for i, path in enumerate(self.paths):
                total_b[i] += self.propagate_along(path, x[i])
            a = sum(x)
            b = sum(total_b)
            return -(b - a / exch_rate) # Minimize -surplus

        # Constrain on the amount sold
        def constraint_sell(x):
                
            return (self.order.limit_sell_amount - sum(x))

        # Constrain on the amount bought
        def constraint_buy(x):
            total_b = 0
            for i, path in enumerate(self.paths):
                total_b += self.propagate_along(path, x[i])
            return (total_b - self.order.limit_buy_amount)
        
        # Set the constraint dictionary according to the order
        if self.order.partial_fill:
            constraints = [{'type': 'ineq', 'fun': constraint_sell},  # total_sold <= s_lim
                           {'type': 'ineq', 'fun': constraint_buy}]    # total_bought >= b_lim
        else: #Fly-or-kill
            constraints = [{'type': 'eq', 'fun': constraint_sell},    # total_sold  = s_lim
                           {'type': 'ineq', 'fun': constraint_buy}]    # total_bought >= b_lim

        options = {
            'ftol': 1e-12,  # Convergence tolerance for the objective function
            'maxiter': 1000  # Maximum number of iterations
        }


        # Initial guesses for sell amount through each path
        initial_guess = [0.0] * len(self.paths)

        # Bounds for the sell amount through each path
        bounds = Bounds([0.0] * len(self.paths), [self.order.limit_sell_amount] * len(self.paths))

        print(" ")
        print("MEV Agent reporting for duty, ready to maximize the surplus .. or at least trying :)")
        # Perform the optimization
        result = minimize(surplus, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints, options=options)

        # Extract the optimal values
        optimal_coins_sell = result.x

        # Compute the resulting values along the paths
        optimal_coins_buy = [self.propagate_along(self.paths[i], optimal_coins_sell[i]) for i in range(len(self.paths))]
        total_sell = sum(optimal_coins_sell)
        total_buy = sum(optimal_coins_buy)

        # Print global information
        print(" ")
        print("The resulting total value sold   (via all paths) is: {:.18f}".format(total_sell))
        print("The resulting total value bought (via all paths) is: {:.18f}".format(total_buy))
        print("The resulting gamma is: {:.18f}".format(total_buy - total_sell/exch_rate))

        print(" ")

        # Print path specific information
        for i, val in enumerate(optimal_coins_sell):
            path = self.paths[i]
            vertices = [path[0]['sell_token']]
            for edge in path:
                vertices.append(edge['buy_token'])
            path_str = " -> ".join(vertices)
            string_sell = f"The resulting total value sold via   {path_str} is: {val:.18f}"
            string_buy  = f"The resulting total value bought via {path_str} is: {optimal_coins_buy[i]:.18f}"
            print(string_sell)
            print(string_buy)
            print(" ")

        # Update order information
        self.order.ex_sell_amount = total_sell
        self.order.ex_buy_amount = total_buy

        # Update venues information
        self.update_venues(optimal_coins_sell)

        return optimal_coins_sell, optimal_coins_buy, total_buy 
        
    def update_venues(self, optimal_coins_sell):
        """
        Updates the venues' reserves based on the optimal coins to sell along each path.

        This method iterates through each path and updates the reserves of the venues involved 
        in the transactions. It calculates the new reserves after selling a specified amount of 
        coins and propagates the outcome of each transaction through the path.

        Parameters:
        -----------
        optimal_coins_sell : list
            A list of amounts of initial coins to sell along each path. The length of this list 
            should be equal to the number of paths of the strategy.

        Updates:
        --------
        - The `reserves` attribute of each `venue` object in `self.venues` is updated with 
          the new reserves after the transactions.
        - Adds 'ex_sell_amount' and 'ex_buy_amount' keys to the `reserves` dictionary of the 
          respective venues to reflect the external sell and buy amounts for each transaction.
        """
        for i,path in enumerate(self.paths):
            current_value = optimal_coins_sell[i]
            for edge_data in path:

                # Get and update the correct venue information
                venue_name = edge_data['venue']
                for v,venue in enumerate(self.venues):
                    if venue.name == venue_name:
                        break

                venue.reserves[edge_data['sell_token']] += current_value
                venue.reserves['ex_buy_amount'] = current_value

                # Propagate and get outcome of transaction
                current_value = edge_data['price_function'](current_value, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'])

                venue.reserves[edge_data['buy_token']] -= current_value
                venue.reserves['ex_sell_amount'] = current_value
                venue.reserves['sell_token'] = edge_data['buy_token']
                venue.reserves['buy_token'] = edge_data['sell_token']

    def print_results(self, file=None):
        """
        Prints the result of the surplus maximization

        This method collects the data from the venues and orders, formats it into a JSON-like
        structure, and then either prints it to the console or writes it to a specified file.

        Parameters:
        -----------
        file : str, optional
            The file path where the output should be written. If None, the output is printed to the console.

        """
        venues_data = {}
        for venue in self.venues:
            venues_data[venue.name] = {
                "sell_token": venue.reserves['sell_token'],
                "buy_token": venue.reserves['buy_token'],
                "ex_buy_amount":  f"{venue.reserves['ex_buy_amount']:.18f}".replace(".","_"),
                "ex_sell_amount": f"{venue.reserves['ex_sell_amount']:.18f}".replace(".","_"),
            }

        order_data = {
            self.order.order_number: {
                "partial_fill": self.order.partial_fill,
                "buy_amount": f"{self.order.limit_buy_amount:.18f}".replace(".","_"),
                "sell_amount": f"{self.order.limit_sell_amount:.18f}".replace(".", "_"),
                "buy_token": self.order.buy_token,
                "sell_token": self.order.sell_token,
                "ex_buy_amount":  f"{self.order.ex_buy_amount:.18f}".replace(".","_"),
                "ex_sell_amount": f"{self.order.ex_sell_amount:.18f}".replace(".","_")
            }
        }

        output_data = {
            "venues": venues_data,
            "orders": order_data
        }

        output = json.dumps(output_data, indent=4)
      
        if file:
            with open(file, 'w') as f:
                f.write(output)
        else:
            print(output)
               

              


