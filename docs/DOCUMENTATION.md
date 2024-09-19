# Documentation

This documentation provides details on the various pieces of the MEV agent code. 

-  [mev_project_interface](mev_project_interface.md): to know more about how the main function to process the user request given the venues and the JSON file storing such information.
-  [classes](CLASSES.md): to know more about the classes employed in the project and how do they work, get a look at 

## Brief explaination of how does the code work
1. Read the User intent and store the information of the required transaction in the [order](classes/order.md) object;
2. Read the Venues and store them in a list of [venue](classes/venue.md) objects;
3. Create a [market](classes/market.md) oject representing the non-directed graph. The edges are the coins present in the liquidity pools, whereas the edges are the venues. Edges store information about the venue and the liquidity of each token. Moreover we also endow each edge with a price function. Before using such price funciton, however, we will need to assess the direction of exchange of coins in the pool;
4. Create a MEV agent [agent](classes/agent.md) object. This object then reads the `order` intent and the `market` graph;
5. From the `order` intent and the `market` graph, `agent` determines the connected token pairs that allow to perform the user requested trade;
6. The agent creates the directed multi-graph connecting requested sell token `A` to requested buy token `B`. This is stored in `agent.strategy`;
7. The agent now creates a set of paths, each of which is a list of the edges (i.e. the venues) that need to be visited along a simple path connecting `A` with `B`. The price function of the edge now can be determined since the direction of token swap is known;
8. Having the list of simple paths to walk, the agent runs `optimize_strategy()`. This procedure creates a vector `x` of dimension `N` which is the number of simple paths connecting `A` to `B`. Defines the surplus function and the constraint functions. The surplus function is built in such a way that `agent` propagates the i-th `x` component through the i-th path and obtaines the i-th component of the bought `b` vector. The surplus is then obtained with the standard formula `Γ(x) = sum(b(x)) - sum(x)/π`. The surplus is optimized thanks to scipy.minimize.
9. The optimal `x` maximizing the surplus under the constrained defined by the `order` is then used to update `venue` information and to compute the coin conservation error.
    


