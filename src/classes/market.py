import networkx as nx
from .venue import venue
from matplotlib import pyplot as plt
import sys

class market:
    """
    A class to represent a market of trading venues and generate a graph.
    
    Attributes:
    -----------
    venues : list
        A list containing venue instances.
    graph : networkx.Graph
        A graph where each unique coin is a node and each reserve acts as an edge with properties.
    
    Methods:
    --------
    generate_graph():
        Generates a graph from the venues.
    print_graph_info():
        Prints the graph information including nodes and edges.
    plot_graph():
        Prints the graph with matplotlib.
    weight_function(sell_amount, liquidity_sell_token, liquidity_buy_token):
        Calculates the weight for an edge based on the sell amount and token liquidity.
    """

    def __init__(self, venues):
        """
        Constructs all the necessary attributes for the market object.
        
        Parameters:
        -----------
        venues : list
            A list containing venue instances.
        """
        self.venues = venues
        self.graph = nx.Graph()
        self.generate_graph()

    def generate_graph(self):
        """
        Generates a graph from the venues.
        """
        for venue in self.venues:
            for token, amount in venue.reserves.items():
                if token not in self.graph:
                    self.graph.add_node(token)

            # Ensure each pair of tokens creates an edge with the venue name as attribute only once
            tokens = list(venue.reserves.keys())
            for i in range(len(tokens)):
                for j in range(i + 1, len(tokens)):
                    token1 = tokens[i]
                    token2 = tokens[j]
                    if not self.graph.has_edge(token1, token2):
                        self.graph.add_edge(token1, token2, venues=[venue.name],       
                                            liquidity_token1 = venue.reserves[token1], 
                                            liquidity_token2 = venue.reserves[token2]) 
                    else:
                        # If still nameless, name the edge
                        if venue.name not in self.graph[token1][token2]['venues']:
                            self.graph[token1][token2]['venues'].append(venue.name)

    def print_graph_info(self):
        """
        Prints the graph information including nodes and edges.
        """
        print("Graph Nodes:")
        print(self.graph.nodes())
        print("\nGraph Edges:")
        for edge in self.graph.edges(data=True):
            print(edge)

    def plot_graph(self):
        """
        Plots the graph using matplotlib.
        """
        pos = nx.spring_layout(self.graph)  # positions for all nodes
        plt.figure(figsize=(10, 8))

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_size=7000, node_color='lightblue')

        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, width=2)

        # Draw node labels
        nx.draw_networkx_labels(self.graph, pos, font_size=12, font_family='sans-serif')

        # Draw edge labels
        edge_labels = {(u, v): ', '.join(data['venues']) for u, v, data in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=10, font_family='sans-serif')

        plt.title("Market Graph")
        plt.show()

    @staticmethod
    def c_prod_amm(sell_amount, liquidity_sell_token, liquidity_buy_token):
        """
        Calculates the price function for a constant product amm

        Parameters:
        -----------
        sell_amount : int
            The amount of the sell token.
        liquidity_sell_token : int
            The liquidity of the sell token in the venue.
        liquidity_buy_token : int
            The liquidity of the buy token in the venue.

        Returns:
        --------
        float
            The calculated buy amount.
        """

        buy_amount = liquidity_buy_token * (1 - liquidity_sell_token / (liquidity_sell_token + sell_amount))
        return buy_amount
