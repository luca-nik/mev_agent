import networkx as nx
from matplotlib import pyplot as plt
import sys
from scipy.optimize import minimize, Bounds, differential_evolution, NonlinearConstraint
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

    def read_market(self, market, verbose = True):
        """
        Evaluates paths in the market connecting sell_token with buy_token of the current order.
        Identifies the venues to visit and the sell and buy tokens for each venue.
        Calling agent.make_strategy() this method also creates the strategy graph and the 
        paths the agent needs to follow.

        This method performs the following steps:
        1. Checks if there is an existing order. If not, prints a message and returns.
        2. Initializes `sell_token` and `buy_token` from the current order.
        3. Copies the market venues to the agent's venues.
        4. Attempts to find all simple paths from `sell_token` to `buy_token` in the market graph:
           - If paths are found:
             a. Initializes the strategy graph (`self.strategy`) as a directed graph.
             b. Initializes `self.paths` as an empty list.
             c. Prints the paths if `verbose` is `True`.
             d. Iterates over each path, printing the path and calling `self.make_strategy` to create and store strategy information.
           - If no paths are found, prints a message indicating so.
        5. Catches `nx.NetworkXNoPath` exception and prints a message if no paths are found.

        Note:
            - Paths connecting token A to B are a list of token names e.g. [A, C, D, B]
        
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
                    print(f"Paths from {sell_token} to {buy_token} for order {self.order.order_number}:")
                for path in paths:
                    if verbose:
                        print(" -> ".join(path))
                    
                    # Make the strategy graph and store the strategy information
                    self.make_strategy(path, market, verbose = verbose)
            else:
                print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")
        except nx.NetworkXNoPath:
            print(f"No paths found from {sell_token} to {buy_token} for order {self.order['order_number']}.")

    def make_strategy(self, path, market, verbose=False):
        """
        Given a path in the market, which is a collection of token names identifying the nodes that lead from
        A -> .. -> B,  (A = token sold by user, B = final token bought by user) it identifies the venues to 
        visit and the sell and buy tokens for each venue.
        It constructs the strategy graph (tokens as nodes and venues as edges). The strategy graph is a 
        directed sub-graph of the market graph containing only the nodes and edges needed to fulfill the user order.
        Moreover it creates the self.paths list. This list contains for a specific A -> .. -> B set of connected nodes,
        the venues that need to be visited.

        This method performs the following steps:
        1. Initializes a split variable to handle multigraphs.
        2. Iterates over each pair of consecutive tokens in the path.
        3. Checks if there is an edge between the token pair in the market graph.
        4. Gathers edge data from the market graph, including venues and liquidity information, and defines the price function
        5. Constructs or updates the strategy graph:
           - Gathers relevant information for each venue in the edge.
           - Prints information if `verbose` is `True`.
           - Updates the strategy graph, handling multigraphs by appending new variables if an edge already exists.
        6. Checks if the multigraph is too complex and exits if it is.
        7. Stores paths in self.paths. These are the edges, i.e. venues, that are visited along a specific coin path (A -> C -> B)

        Note:
            -Each edge of the strategy graph will be associated to a sell_token and to a buy_token uniquely defined 
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
        split = 1
        for i in range(len(path) - 1): # Go through the path
            token1 = path[i]
            token2 = path[i + 1]
            if market.graph.has_edge(token1, token2):
                # gather edge data information from the market graph
                edge_data = market.graph[token1][token2]
                venues = edge_data['venues']
                for ven_indx, venue in enumerate(venues):
                    # Gather information from the venues in that edge
                    sell_token_number = edge_data['tokens'][ven_indx].index(token1) + 1
                    buy_token_number = edge_data['tokens'][ven_indx].index(token2) + 1
                    liquidity_sell_token = edge_data['liquidity_token' + str(sell_token_number)][ven_indx]
                    liquidity_buy_token = edge_data['liquidity_token' + str(buy_token_number)][ven_indx]

                    if verbose:
                        print(f"Venue: {venue}, Sell Token: {token1}, Buy Token: {token2}, Liquidity: {liquidity_sell_token} {token1}, {liquidity_buy_token} {token2}")

                    # Construct strategy graph, assign the price_function, and all the data needed for the trade in each edge
                    if self.strategy.has_edge(token1,token2): # Multigraph, update appending the new variables
                        self.strategy[token1][token2]['venue'].append(venue)
                        self.strategy[token1][token2]['price_function'].append(market.price_function)
                        self.strategy[token1][token2]['liquidity_sell_token'].append(liquidity_sell_token)
                        self.strategy[token1][token2]['liquidity_buy_token'].append(liquidity_buy_token)
                        split += 1 #variable needed to construct split paths for multigraphs
                    else:
                        self.strategy.add_edge(token1, token2, sell_token=token1, buy_token=token2, venue=[venue], price_function=[market.price_function],
                                               liquidity_sell_token=[liquidity_sell_token], 
                                               liquidity_buy_token=[liquidity_buy_token])

        # Approximation. If the multigraph is too complex I exit.
        if (split > 2 and len(path) > 2) : # I have more than 2 splitting and a more than 2 tokens. Of course it is an approximation to make the code work in the third exercise.
            print('**********************')
            print('ERROR: the market multigraph is too complex.')
            sys.exit()

        # Store the paths where the agent will have to propagate
        edges =[[] for i in range(split)]
        for path_indx in range(split):
            for i in range(len(path)-1):
                if(len(self.strategy[path[i]][path[i+1]]['venue']) > 1): #is a multigraph, split the path
                    # Copy the values of the specific path and flatten them out
                    edge_to_append = self.strategy[path[i]][path[i+1]].copy()
                    edge_to_append['venue'] = edge_to_append['venue'][path_indx]
                    edge_to_append['price_function'] = edge_to_append['price_function'][path_indx]
                    edge_to_append['liquidity_sell_token'] = edge_to_append['liquidity_sell_token'][path_indx]
                    edge_to_append['liquidity_buy_token']  = edge_to_append['liquidity_buy_token'][path_indx]
                    edges[path_indx].append(edge_to_append) 
                else:
                    edge_to_append = self.strategy.edges[path[i], path[i+1]].copy()
                    edge_to_append['venue'] = edge_to_append['venue'][0]
                    edge_to_append['price_function'] = edge_to_append['price_function'][0]
                    edge_to_append['liquidity_sell_token'] = edge_to_append['liquidity_sell_token'][0]
                    edge_to_append['liquidity_buy_token']  = edge_to_append['liquidity_buy_token'][0]
                    edges[path_indx].append(edge_to_append) 

        # Create the paths as a list of edges with the specific information
        for edge in edges:
            self.paths.append(edge)

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
        This function propagates an initial amount of coins sold through the chain of venues stored in path,
        outputting the amount of coins bought at the end of path.

        Parameters:
        -----------
        path : list
            The list of edges of the strategy graph representing the path alogn which we propagate
        initial_sell_coin_amount : float
            The initial amount of coins to sell at the beginning of the path

        Returns:
        --------
        float
            The final value after propagation (i.e. the amount of buy_coin of the order bought along that path)
        """
        current_value = initial_sell_coin_amount
        for edge_data in path:
            # Call price function of this venue for the specific liquidities
            current_value = edge_data['price_function'](current_value, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'])
        return current_value

    def optimize_strategy(self):
        """
        Optimizes the strategy to maximize the order surplus

        This method performs the following steps:
        1. Calculates the worst acceptable exchange rate based on the order's limit sell and buy amounts.
        2. Defines a surplus function to be maximized:
            - The surplus is a function of the coins sold and bought through each path.
            - Along each path the amount of coins bnought is obtained with the propagate_along() function.
        3. Define Constraints:
           - Defines constraints to ensure the total sell amount does not exceed the limit sell amount and the total buy amount meets or exceeds the limit buy amount.
           - If the order allows partial fills, it sets an inequality constraint for the sell amount; otherwise, it sets an equality constraint for a fill-or-kill order.
        6. Run Optimization:
           - Uses the SLSQP method to minimize the negative surplus (maximize surplus) within the specified bounds and constraints.
        7. Extract and Compute Results:
           - Extracts the optimal sell amounts and computes the resulting buy amounts.
           - Computes the coin conservation error to check for discrepancies.
           - Prints optimization results and detailed information for each path.
        8. Update Order and Venues Information:
           - Updates the order with the executed sell and buy amounts.
           - Updates the venues with the optimal sell amounts.
        
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
            # Propagate along each path the initial amount
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
        
        # Check if continuity is preserved. Sum up swap errors obtained in each venue visited
        def coin_conservation(x,print_=False):
            error = 0
            for i,path in enumerate(self.paths):
                sell_amount = x[i]
                for index, edge_data in enumerate(path):
                    string = 'with ' + str(sell_amount) +  ' buy '
                    # Compute amount bought in this edge
                    buy_amount = edge_data['price_function'](sell_amount, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'],what_='buy')
                    string += str(buy_amount)

                    # What is the amount sold corresponding to this amount bought
                    inverse_buy = edge_data['price_function'](buy_amount, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'], what_='sell')
                    
                    # Updates consservation error
                    error += abs(sell_amount - inverse_buy)

                    sell_amount = buy_amount
                    string += ' inverse ' + str(inverse_buy)
                    if print_:
                        print(string)
            return error

        
        # Set the constraint dictionary according to the order
        if self.order.partial_fill:
            constraints = [{'type': 'ineq', 'fun': constraint_sell}]  # total_sold <= s_lim
        else: #Fly-or-kill
            constraints = [{'type': 'eq', 'fun': constraint_sell}]   # total_sold  = s_lim
        nlc2 = NonlinearConstraint(constraint_buy, 0, np.inf)
        constraints.append(nlc2)

        print(" ")
        print("MEV Agent ready to maximize the surplus .. or at least trying :)")

        # Initial guesses for sell amount through each path
        initial_guess = [0.0] * len(self.paths)

        # Bounds for the sell amount through each path
        bounds = Bounds([0.0] * len(self.paths), [self.order.limit_sell_amount] * len(self.paths))

        # Maximize the surplus
        result = minimize(surplus, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)


        # Extract the optimal values
        optimal_coins_sell = result.x

        # Compute the resulting values along the paths
        optimal_coins_buy = [self.propagate_along(self.paths[i], optimal_coins_sell[i]) for i in range(len(self.paths))]
        
        # Compute the coin conservation error
        error = coin_conservation(optimal_coins_sell)

        total_sell = sum(optimal_coins_sell)
        total_buy = sum(optimal_coins_buy)

        print(" ")
        print("Status:", result.status)
        if int(result.status) != 0:
            print('****** ERROR ******    :( ')
        print("Message:", result.message)
        print("Number of Iterations:", result.nit)
        print("Number of Function Evaluations:", result.nfev)
        print("Number of Gradient Evaluations:", result.njev)
        print(" ")

        # Print global information
        print(" ")
        print("The resulting total value sold   (via all paths) is: {:.18f}".format(total_sell))
        print("The resulting total value bought (via all paths) is: {:.18f}".format(total_buy))
        print("The resulting gamma is: {:.18f}".format(total_buy - total_sell/exch_rate))
        print("Total coin conservation error: {:.7e}".format(error))
        print(" ")

        # Print path specific information
        for i, val in enumerate(optimal_coins_sell):
            path = self.paths[i]
            vertices = [path[0]['sell_token']]
            venues = []
            for edge in path:
                vertices.append(edge['buy_token'])
                venues.append(edge['venue'])
            path_str = " -> ".join(venues)
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

        return optimal_coins_sell, optimal_coins_buy
        
    def update_venues(self, optimal_coins_sell):
        """
        Updates the venues' reserves based on the optimal coins to sell along each path.
        This method iterates through each path and updates the reserves of the venues involved 
        in the transactions. It calculates the new reserves after selling a specified amount of 
        coins and propagates the outcome of each transaction through the path.

        Note:
            - The values bought in each venue are not stored in memory, thus in this procedure
              we have to iterate along each path.

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
        # Cycle over paths 
        for i,path in enumerate(self.paths):
            current_value = optimal_coins_sell[i]
            # Get venues in the paths
            for edge_data in path:
                # Select the correct venue that we are meeting in this edge of the path
                venue_name = edge_data['venue']
                for v,venue in enumerate(self.venues):
                    if venue.name == venue_name:
                        break

                # Update venue information
                venue.reserves[edge_data['sell_token']] += current_value
                venue.reserves['ex_buy_amount'] = current_value

                # Propagate and get outcome of transaction
                current_value = edge_data['price_function'](current_value, edge_data['liquidity_sell_token'], edge_data['liquidity_buy_token'])

                # Update venue information
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
               

              


