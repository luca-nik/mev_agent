# My Solution to Exercise 3

In this exercise I kept the `USDT`/`USDC` token pair, the same user order, and the same UNISWAP venue considered in [exercise 2](../second/Exercise2.md). 
In addtion to this, I also included a new venue (`METEORA_USDC_USDT`) which is a [liquidity pool of Meteora](https://www.geckoterminal.com/solana/pools/32D4zRxNc1EssbJieVHfPhZM3rH6CzfUPrWUuWxD9prG).

In this exercise I run the code [third_exercise.py](third_exercise.py).

This code, first identifies the initial JSON-file intent [data.json](data.json). Then it [downloads from the internet](https://www.geckoterminal.com/solana/pools/32D4zRxNc1EssbJieVHfPhZM3rH6CzfUPrWUuWxD9prG) the liquidities of the selected tokens creating a new venue called `METEORA_USDC_USDT`. The liquidity in `UNISWAP_USDC_USDT` is kept fixed.

At this point the procedure is analogous to the other two exercises. We create a graph and we try to maximize the surplus along this graph.

## Note
The `METEORA_USDC_USDT` liquidity is updated on-the-fly, thus to reproduce my results, one need to run the following code:
```console
user@pc:~$PATH-TO-MY-CODE/exercises/third$ python3 reproduce_results.py
```
Which takes as input [my_data.json](my_data.json) which contins the liquidities of the tokens at the time I executed the code.


## Results
Input (after data collection from the online pool):
```json
{
    "orders": {
        "0": {
            "sell_token": "USDC",
            "buy_token": "USDT",
            "limit_sell_amount": "1000_000000000000000000",
            "limit_buy_amount": "900_000000000000000000",
            "partial_fill": false
        }
    },
    "venues": {
        "UNISWAP_USDC_USDT": {
            "reserves": {
                "USDC": "2390981_000000000000000000",
                "USDT": "2394046_000000000000000000"
            }
        },
        "METEORA_USDC_USDT": {
            "reserves": {
                "USDC": "1566122_719999999972060323",
                "USDT": "10608171_289999999105930328"
            }
        }
    }
}
```
```console
luca@lime:~/programmi/mev_agent/exercises/third$ python3 third_exercise.py
Loading data from https://www.geckoterminal.com/solana/pools/32D4zRxNc1EssbJieVHfPhZM3rH6CzfUPrWUuWxD9prG
 
Extracted USDC liquidity: 1566122.72
Extracted USDT liquidity: 10608171.29
 
Temporary 'pool_data.html' file storing pool information has been deleted.
New venue METEORA_USDC_USDT added to the JSON file data.json

MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 7
Number of Function Evaluations: 21
Number of Gradient Evaluations: 7
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 6769.202663322582338878
The resulting gamma is: 5869.202663322582338878
Total coin conservation error: 1.1368684e-13
 
The resulting total value sold via   UNISWAP_USDC_USDT is: 0.000000002510027741
The resulting total value bought via UNISWAP_USDC_USDT is: 0.000000002513245347
 
The resulting total value sold via   METEORA_USDC_USDT is: 999.999999997490021997
The resulting total value bought via METEORA_USDC_USDT is: 6769.202663320069405017
```
Resulting output:
```json
{
    "venues": {
        "UNISWAP_USDC_USDT": {
            "sell_token": "USDT",
            "buy_token": "USDC",
            "ex_buy_amount": "0_000000002510027741",
            "ex_sell_amount": "0_000000002513245347"
        },
        "METEORA_USDC_USDT": {
            "sell_token": "USDT",
            "buy_token": "USDC",
            "ex_buy_amount": "999_999999997490021997",
            "ex_sell_amount": "6769_202663320069405017"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "USDT",
            "sell_token": "USDC",
            "ex_buy_amount": "6769_202663322582338878",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```
```
The surplus generated is 5869_202663322582338878
```
## Discussion
I will first discuss some technical details, and then I will focus on the results.

### Technical discussion
In this case, differently from the previous exercises, the graph is a multi-graph. Indeed the nodes `USDC` and `USDT` are connected by two distinct edges `UNISWAP_USDC_USDT` and `METEORA_USDC_USDT`.
To be honest, when I started writing the code for the first exercise, I did not consider this option and thus I had to change the code on-the-fly with some easy-to-implement fixes.
From a theoretical point of view, the problem of routing on multigraphs is still convex ([See Ref.](https://hal.science/hal-03455981/file/goroen.pdf)).

Thus, the solution I decided to implement is the following:

While creating the `mev_agent.strategy` graph, for each pair of nodes connected by N multiple edges I create N distinct paths. This is a rough approach because it is correct if only one pair of nodes is connected by multiple edges. Indeed, if we detect more than one branching, for paths containing more than just two tokens, the code will output an error, since it is not built to treat such more complex paths. Thus in my case, I created just two paths and I performed the optimization along such paths.

Nevertheless, the problem of counting simple paths in directed multigraph is rather interesting. If I have to exchange token `A` with `B` passing through `C`, the possible independent paths connecting `A`/`B` will be dependent on the numbers `N`, `M` of multiple paths connecting `A`/`C` (`N`) and `C`/`B` (`M`). The total number of available paths in this case will be `T = M*N`. However, also this is again a rough oversimplification of the problem which is combinatorial by nature and gets extremely complex as the dimension of the graph starts increasing. 

In addition to this, even if the directed graph wouldn't have multi-edged connected vertices, the problem of simple path detection from `A` to `B` is extremely complex ([#P-complete](https://epubs.siam.org/doi/abs/10.1137/0208032)), and requires [complex numerical techniques](https://arxiv.org/pdf/2103.06102) to be solved efficiently.

Moreover, in these exercises, we never considered multi-asset venues, which would imply more complex graphs, and for which the price functions could change during propagation. Indeed, if we consider a multi-asset pool, with tokens `A`,`B`, and `C`, it can happen that the price function `c(a)` might change if I first visited this venue but along a different edge of the graph e.g. `A`/`B`. 
Another source of additional complexity is the possibility that the graph changes through time. Indeed, it might be possible for new venues to be added to the market effectively introducing new connections among the nodes.

Aside from these considerations about the network complexity, an MEV agent should be able to perform the surplus optimization also accounting for multiple user orders (which is not implemented in this simple program I developed), should be capable of evaluating order books to identify possible optimal swaps or ring trades.

In short, considering all these factors, our little code appears even smaller in the face of this mountain of complexity.

**Considerations**: Given the complexity of the routing problem in real case scenarios I thought that MEV agents could be developed leveraging [reinforcement-learning](https://huggingface.co/learn/deep-rl-course/unit2/what-is-rl) techniques. One could use real-world data to create a training ground for single or multiple interacting agents, leveraging single or [Multi-Agents Reinforcement Learning](https://huggingface.co/learn/deep-rl-course/unit7/introduction-to-marl) techniques in order to learn optimal behavioral policies given the current market state.

### Results
Interestingly, adding the `METEORA_USDC_USDT` to the market graph (with the liquidities at the time I executed the code) has allowed me to increase the surplus by a factor ~58. This could be a rather interesting example where arbitrage could be exploited, buying `USDT` from `METEORA_USDC_USDT`, and selling them back for `USDC` in `UNISWAP_USDC_USDT`.


#### A question for you
Since I am new to the crypto world, I might have misunderstood something. Is it really possible to exploit such an arbitrage opportunity and come back with more USDC than before, basically for free, or am I losing something here? I mean my concern is regarding the fact that although the price of the USDC and USDT should be bound to the value of the US dollar, due to liquidity unbalances in the pool, the price of one token with respect to the other is significantly lower when swapping them. I know that this is the basis for arbitrage, but I was questioning if I was not mistaken or if I was not considering something (maybe the price function of the AMM is different from the standard constant product and keeps track of their value with respect to the dollar, ...).
Sorry for the naive question, but I was just curious :).

Go back to [First Exercise](../first/Exercise1.md)

Go back to [Second Exercise](../second/Exercise2.md)
