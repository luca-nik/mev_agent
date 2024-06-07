# My solutions to Exercise 2

In this exercise I choose to swap the token pair `USDT`/`USDC`.

For the reserves I considered a [liquidity pool on Uniswap](https://v2.info.uniswap.org/pair/0x3041cbd36888becc7bbcbc0045e3b1f144466f5f) in date 7 June 2024.

In the following the JSON file of the input provided to the `maximize_mev.py` code.

```json
{
    "orders": {
        "0": {
            "sell_token": "USDC",
            "buy_token": "USDT",
            "limit_sell_amount": "1000_000000000000000000",
            "limit_buy_amount": "900_000000000000000000",
            "partial_fill": false}
    },
    "venues": {
        "UNISWAP_USDC_USDT": {
            "reserves": {
                "USDT":  "2394046_000000000000000000",
                "USDC":  "2390981_000000000000000000"
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
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 1000.863301171706666537
The resulting gamma is: 100.863301171706666537
Total coin conservation error: 1.1368684e-13
 
The resulting total value sold via   UNISWAP_USDC_USDT is: 1000.000000000000000000
The resulting total value bought via UNISWAP_USDC_USDT is: 1000.863301171706666537
```
```json
{
    "venues": {
        "UNISWAP_USDC_USDT": {
            "sell_token": "USDT",
            "buy_token": "USDC",
            "ex_buy_amount": "1000_000000000000000000",
            "ex_sell_amount": "1000_863301171706666537"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "USDT",
            "sell_token": "USDC",
            "ex_buy_amount": "1000_863301171706666537",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```
```
The surplus generated is 100_863301171706666537
```

## Discussion
The code I am running in this exercise is the same of the previous. Thus, we are trying to maximize the surplus along all the simlpe paths connecting `USDC`\`USDT`, which in this case is just one. 
Given the almost equal liquidity of the two tokens in the `UNISWAP_USDC_USDT` pool at the time I gathered the data, the amount of `USDC` tokens bought is not extremely high.

However, this is an ideal condition. 
Indeed, when comparing this result with real swaps, several factors might influence our outcome. In the following, I will try to address some of these factors.

### Liquidity Pool Providers' Fee
First, we must consider that in my example, the price of token `B` (denoted as `b`) in an Automated Market Maker (AMM) will be `b(x) = [B]x/(x + [A])`, where `[A]` and `[B]` are the initial liquidities of the pool of the two tokens and `x` is the amount of token `A` sold. In real-world scenarios, such as on Uniswap, real price functions account for the fee extracted by the liquidity providers for every transaction. This fee is denoted as `0 <= 1 - γ < 1`, and the price function becomes `b(x) = [B]γx/(γx + [A])`. This adjustment means that part of the transaction is taken as a fee, affecting the resulting price and received amount of token `B`.

### Price Function
In real AMM models, the price function is often influenced by more complex algorithms. For example, Uniswap V3 uses a concentrated liquidity model, where liquidity is provided within specific price ranges. This makes the price function more dynamic and complex compared to a simple constant product formula.

### Routing
In my example, the two tokens `USDT` and `USDC` are present in a single liquidity pool, where I perform the swap. In real-world scenarios, this might not always be the case. Swaps are often executed on DEX aggregators (e.g., [1inch](https://1inch.io/)), which have access to multiple liquidity pools. Thus, there can be multiple possible routes from `USDT` to `USDC`. The routing algorithm will seek the best price across various pools, which can lead to variations in the executed buy amount due to differences in liquidity, fees, and slippage across routes.

### Price Slippage
Another important factor to consider is price slippage. By the time the transaction order I intend to perform is processed by the miners, the price of at least one of the assets in the path connecting `USDT` to `USDC` might have changed. This can result in a different executed buy amount than what was initially expected. Slippage is more significant in volatile markets or with large order sizes relative to the liquidity available in the pool.

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
