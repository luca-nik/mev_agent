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
When comparing this result with real swaps we have to consider several factors that might influence our outcome.
In the follwoing I will try to adress some of these factors. 

### Liqidity Pool providers fee
First of all we have to consider that in my example, the price of token `B` (b) in a AMM will be `b(x) = [B]x/(x + [A])` where `[A]` and `[B]` are the initial liquidities of the pool of the two tokens and `x` is the amount of token `A` sold. In real case scenarios, as in Uniswap, real price functions account for the fee extracted by the liquidity providers for every transaction ` 0 <= 1 − γ < 1`, and the price function becomes
`b(x) = [B]γx/(γx + [A])`.

### Price function


### Routing


### Price slippage

Connettere un paio e fare l'exchange esemplificativo.
Qui dovro parlare delle gas-fees e del processo in realta' di mining del mio coso, per cui in realta' noi avremo casini causati da ordini di altri utenti che quindi potranno ridurre il nostro surplus

Inoltre dovro' vedere anche cosa vuol dire lo slippage.
Vedere in uniswap v3 come calcolano lo scambio, magari in alcune liquididty pools la funzione di prezzo non e' proprio giusta giusta.


Dire che in genere quando facciamo degli swaps su aggregatori tipo.., non e' garantito che sia a singolo hop, quindi non necessariamente avro gli stessi risultati.

-gas prices
-multiple hops
-price slippage
-non perfect constant-product price functions
