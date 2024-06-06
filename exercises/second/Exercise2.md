# My solutions to Exercise 2

In this exercise I choose `ETH` and `USDC` as token pairs to swap.

For the reserves I considered a [liquidity pool on Uniswap](https://v2.info.uniswap.org/pair/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc) in date 5 June 2024.

In the following the JSON file of the input provided to the `maximize_mev.py` code.

```json
{
    "orders": {
        "0": {
            "sell_token": "ETH",
            "buy_token": "USDC",
            "limit_sell_amount": "100_000000000000000000",
            "limit_buy_amount": "35000_000000000000000000",
            "partial_fill": false}
    },
    "venues": {
        "UNISWAP_USDC_ETH": {
            "reserves": {
                "ETH":  "14211_000000000000000000",
                "USDC": "53804606_000000000000000000"
            }
        }
    }
}
```

With results 

```console
luca@lime:~/programmi/mev_agent/exercises/second$ python3 maximize_surplus.py input.json 
 
MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 2
Number of Function Evaluations: 4
Number of Gradient Evaluations: 2
 
 
The resulting total value sold   (via all paths) is: 100.000000000000000000
The resulting total value bought (via all paths) is: 375966.780797987594269216
The resulting gamma is: 25966.780797987594269216
Total coin conservation error: 1.4210855e-14
 
The resulting total value sold via   ETH -> USDC is: 100.000000000000000000
The resulting total value bought via ETH -> USDC is: 375966.78079798759426921
```
```json
{
   "venues": {
        "UNISWAP_USDC_ETH": {
            "sell_token": "USDC",
            "buy_token": "ETH",
            "ex_buy_amount": "100_000000000000000000",
            "ex_sell_amount": "375966_780797987594269216"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "350000_000000000000000000",
            "sell_amount": "100_000000000000000000",
            "buy_token": "USDC",
            "sell_token": "ETH",
            "ex_buy_amount": "375966_780797987594269216",
            "ex_sell_amount": "100_000000000000000000"
        }
    }
}
```

```
The surplus generated is 25966_780797987594269216
```

## Discussion
When comparing this result with real swaps, several factors might influence our outcome. In the following, I will address some of these factors.

### Liquidity Pool Providers' Fee
First, we must consider that in my example, the price of token `B` (denoted as `b`) in an Automated Market Maker (AMM) will be `b(x) = [B]x/(x + [A])`, where `[A]` and `[B]` are the initial liquidities of the pool of the two tokens and `x` is the amount of token `A` sold. In real-world scenarios, such as on Uniswap, real price functions account for the fee extracted by the liquidity providers for every transaction. This fee is denoted as `0 <= 1 - γ < 1`, and the price function becomes `b(x) = [B]γx/(γx + [A])`. This adjustment means that part of the transaction is taken as a fee, affecting the resulting price and received amount of token `B`.

### Price Function
In real AMM models, the price function is often influenced by more complex algorithms. For example, Uniswap V3 uses a concentrated liquidity model, where liquidity is provided within specific price ranges. This makes the price function more dynamic and complex compared to a simple constant product formula.

### Routing
In my example, the two tokens `ETH` and `USDC` are present in a single liquidity pool, where I perform the swap. In real-world scenarios, this might not always be the case. Swaps are often executed on DEX aggregators (e.g., [1inch](https://1inch.io/)), which have access to multiple liquidity pools. Thus, there can be multiple possible routes from `ETH` to `USDC`. The routing algorithm will seek the best price across various pools, which can lead to variations in the executed buy amount due to differences in liquidity, fees, and slippage across routes.

### Price Slippage
Another important factor to consider is price slippage. By the time the transaction order I intend to perform is processed by the miners, the price of at least one of the assets in the path connecting `ETH` to `USDC` might have changed. This can result in a different executed buy amount than what was initially expected. Slippage is more significant in volatile markets or with large order sizes relative to the liquidity available in the pool.

### Mining
The process of mining and the time it takes for a transaction to be included in a block can also impact the outcome. During this period, market conditions can change, and other transactions can alter the state of the liquidity pool. This can lead to differences between the expected and the actual execution price.

### Other Users
Other market participants can also influence the outcome. Frontrunning, sandwich attacks, and arbitrage are common in DeFi and can significantly impact the price and execution of a swap. For instance, a frontrunner might detect a large swap and place their transaction before it to profit from the expected price movement, resulting in a worse price for the original transaction.

QUI BISOGNA DIRE CHE COME MEV AGENT, PIU CHE GLI ALTRI USERS, SONO GLI ALTRI MEV AGENTS O I MINERS A SECONDA DELLA BLOCKCHAIN. ALTRI ORDINI DI UTENTI POI SONO DA CONSIDERARE E QUINDI L'ORDINE IN CUI ESERGUIRLI, I.E. IL BLOCCO DI ORDINI DI DARE AL VALIDATOR, ETC ETC.

### Gas Fees
Finally, gas fees are a crucial consideration in executing swaps on Ethereum. High gas fees can make small trades unprofitable or reduce the net gain from arbitrage opportunities. Additionally, during times of network congestion, gas fees can spike, making it more expensive to execute swaps and affecting the overall profitability.

# Altro
Connettere un paio e fare l'exchange esemplificativo.
Qui dovro parlare delle gas-fees e del processo in realta' di mining del mio coso, per cui in realta' noi avremo casini causati da ordini di altri utenti che quindi potranno ridurre il nostro surplus

Inoltre dovro' vedere anche cosa vuol dire lo slippage.
Vedere in uniswap v3 come calcolano lo scambio, magari in alcune liquididty pools la funzione di prezzo non e' proprio giusta giusta.


Dire che in genere quando facciamo degli swaps su aggregatori tipo.., non e' garantito che sia a singolo hop, quindi non necessariamente avro gli stessi risultati.

-gas prices
-multiple hops
-price slippage
-non perfect constant-product price functions


Go to [third exercise](../third.Exercise3.md)
