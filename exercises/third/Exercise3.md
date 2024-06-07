# My solutions to Exercise 3

In this exercise I connected to the liquidity pool of Meteora with token pair `USDT`/`USDC`



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
Connettere un paio e fare l'exchange esemplificativo.
Qui dovro parlare delle gas-fees e del processo in realta' di mining del mio coso, per cui in realta' noi avremo casini causati da ordini di altri utenti che quindi potranno ridurre il nostro surplus

Inoltre dovro' vedere anche cosa vuol dire lo slippage.
Vedere in uniswap v3 come calcolano lo scambio, magari in alcune liquididty pools la funzione di prezzo non e' proprio giusta giusta.
