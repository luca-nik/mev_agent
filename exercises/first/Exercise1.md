# Discussion Excercise 1

To evalyuate the solutions I provide it is sufficient to run the code 
```console
example@example:~$PATH-TO-MEV_AGENT/mev_agent/exercises/first python3 maximize_surplus.py input.json
```
Where `input.json` is one of the three inputs provided.

In the following I report the solutions I obtained emplyoing my protocol and my program

### First input
```console
luca@NTNU19403:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input1.json 
 
MEV Agent reporting for duty, ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 2
Number of Function Evaluations: 4
Number of Gradient Evaluations: 2
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 909.090909090909349288
The resulting gamma is: 9.090909090909349288
Total coin conservation error: 0.000000000000909495
 
The resulting total value sold via   RHO -> KAPPA is: 1000.000000000000000000
The resulting total value bought via RHO -> KAPPA is: 909.090909090909349288

```

With resulting JSON-file
```json
{
    "venues": {
        "AMM_RHO_KAPPA": {
            "sell_token": "KAPPA",
            "buy_token": "RHO",
            "ex_buy_amount": "1000_000000000000000000",
            "ex_sell_amount": "909_090909090909349288"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "KAPPA",
            "sell_token": "RHO",
            "ex_buy_amount": "909_090909090909349288",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```

