import networkx as nx
from matplotlib import pyplot as plt
import sys
from scipy.optimize import minimize, Bounds

#def c_prod_amm(sell_amount, liquidity_sell_token, liquidity_buy_token):
#    """
#    Calculates the price function for a constant product amm
#
#    Parameters:
#    -----------
#    sell_amount : int
#        The amount of the sell token.
#    liquidity_sell_token : int
#        The liquidity of the sell token in the venue.
#    liquidity_buy_token : int
#        The liquidity of the buy token in the venue.
#
#    Returns:
#    --------
#    float
#        The calculated buy amount.
#    """
#    buy_amount = liquidity_buy_token * (1 - liquidity_sell_token / (liquidity_sell_token + sell_amount))
#    print(" ")
#    print(sell_amount)
#    print(liquidity_sell_token)
#    print(liquidity_buy_token)
#    print(buy_amount)
#    #sys.exit()
#    return buy_amount


class agent:
    """
    A class to represent an agent that reads and stores a single user intent.
    
    Attributes:
    -----------
    order : dict
        A dicotionary to store the current order information.
    strategy : nx.DiGraph
        A directed graph to store the strategy paths from sell_token to buy_token.
    paths : list
        A list of the paths from sell_token to buy_token
    
    Methods:
    --------
    read_intent(order):
        Reads an order object and stores the associated information.
    print_intent():
        Prints the current order information.
    read_market(market):
        Evaluates paths in the market connecting sell_token with buy_token of the current order.
    make_strategy(path, market):
        Evaluates a given path and identifies the venues to visit and the sell and buy tokens for each venue.
    plot_strategy():
        Plots the strategy graph using matplotlib.
    propagate_along(path, initial_value):
        Calculates the transfer function along a path.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the agent object.
        """
        self.order = None
        self.strategy = None
        self.paths = None

    def read_intent(self, order):
        """
        Reads an order object and stores the associated information.
        
        Parameters:
        -----------
        order : order
            The order object containing the user intent.
        """
        self.order = {
            "order_number": order.order_number,
            "sell_token": order.sell_token,
            "buy_token": order.buy_token,
            "limit_sell_amount": order.limit_sell_amount,
            "limit_buy_amount": order.limit_buy_amount,
            "partial_fill": order.partial_fill
        }

    def print_order(self):
        """
        Prints the current order information.
        """
        if self.order:
            print("Current order:")
            print(self.order)
        else:
            print("No order found.")

    def read_market(self, market):
        """
        Evaluates paths in the market connecting sell_token with buy_token of the current order.
        Identifies the venues to visit and the sell and buy tokens for each venue.
        
        Parameters:
        -----------
        market : Market
            The market object containing the graph of tokens and venues.
        """
        if not self.order:
            print("No order to evaluate.")
            return

        sell_token = self.order["sell_token"]
        buy_token = self.order["buy_token"]
        try:
            paths = list(nx.all_simple_paths(market.graph, source=sell_token, target=buy_token))
            if paths:

                # Construct the strategy graph
                self.strategy = nx.DiGraph()
                self.paths = []
                #print(f"Paths from {sell_token} to {buy_token} for order {self.order['order_number']}:")
                for path in paths:
                    #print(" -> ".join(path))

                    self.make_strategy(path, market)
                    
                    # Construct the paths where I propagate, with correct price information
                    edges = [self.strategy.edges[path[i], path[i+1]] for i in range(len(path)-1)]
                    self.paths.append(edges)

            else:
                print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")
        except nx.NetworkXNoPath:
            print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")

    def make_strategy(self, path, market):
        """
        Evaluates a given path and identifies the venues to visit and the sell and buy tokens for each venue.
        
        Parameters:
        -----------
        path : list
            The list of tokens representing the path.
        market : Market
            The market object containing the graph of tokens and venues.
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
                    #print(f"Venue: {venue}, Sell Token: {token1}, Buy Token: {token2}, Liquidity: {liquidity_sell_token} {token1}, {liquidity_buy_token} {token2}")
                    self.strategy.add_edge(token1, token2, venue=venue, price_function=market.c_prod_amm,
                                           liquidity_sell_token=liquidity_sell_token, 
                                           liquidity_buy_token=liquidity_buy_token)

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


    def propagate_along(self, path, initial_value):
        """
        Calculates the transfer function of currencies along a path.

        Parameters:
        -----------
        path : list
            The list of nodes representing the path.
        initial_value : float
            The initial value to propagate along the path.

        Returns:
        --------
        float
            The final value after propagation (i.e. the amount bought along that path)
        """
        current_value = initial_value
        for edge_data in path:
            current_value = edge_data['price_function'](current_value, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'])
        return current_value

    def optimize_strategy(self):
        """
        Optimizes the strategy to maximize the total buy amount minus the weighted total sell amount.
        
        Returns:
        --------
        tuple
            The optimal sell amounts and the resulting buy amounts.
        """
        
        # Compute the worst exchange rate acceptable
        exch_rate = self.order["limit_sell_amount"]/self.order["limit_buy_amount"]

        # Define the objective function to maximize
        def objective(x):
            total_b = 0
            for i, path in enumerate(self.paths):
                total_b += self.propagate_along(path, x[i])
            a = sum(x)
            return -(total_b - a / exch_rate)

        # Define the constraints
        def constraint_sum(x):
            return (self.order["limit_sell_amount"] - sum(x))*10**18

        def constraint_b(x):
            total_b = 0
            for i, path in enumerate(self.paths):
                total_b += self.propagate_along(path, x[i])
            return (total_b - self.order["limit_buy_amount"])*10**18

        # Constraints dictionary
        if self.order["partial_fill"]:
            constraints = [{'type': 'ineq', 'fun': constraint_sum},  # sum(x) <= s_lim
                           {'type': 'ineq', 'fun': constraint_b}]    # total_b >= b_lim
        else: #Fly-or-kill
            constraints = [{'type': 'eq', 'fun': constraint_sum},    # sum(x)  = s_lim
                           {'type': 'ineq', 'fun': constraint_b}]    # total_b >= b_lim

        # Initial guesses for all variables
        initial_guess = [0.0] * len(self.paths)

        # Bounds for all variables
        bounds = Bounds([0.0] * len(self.paths), [self.order["limit_sell_amount"]] * len(self.paths))

        # Perform the optimization
        result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

        # Extract the optimal values
        optimal_values = result.x

        # Compute the resulting values along the paths
        optimal_b_values = [self.propagate_along(self.paths[i], optimal_values[i]) for i in range(len(self.paths))]
        optimal_b_sum = sum(optimal_b_values)

        print("The resulting total value sold (via all paths) is: {:.18f}".format(sum(optimal_values)))
        print("The resulting total value at B (via all paths) is: {:.18f}".format(optimal_b_sum))
        print("The resulting gamma is: {:.18f}".format(optimal_b_sum - sum(optimal_values)/exch_rate))


        return optimal_values, optimal_b_values, optimal_b_sum 






