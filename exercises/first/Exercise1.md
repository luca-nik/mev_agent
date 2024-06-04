# Discussion Excercise 1

To replicate the solutions I provide it is sufficient to run the code 
```console
example@example:~$PATH-TO-MEV_AGENT/mev_agent/exercises/first$ python3 maximize_surplus.py input.json
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
Total coin conservation error: 9.0949470e-13
 
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

<div align="center">
  <img src="docs/images/graph_1_ex1.png" alt="Diagram">
  <p style="margin-top: 10px;">Strategy graph of the first input.</p>
</div>

### Second Input
```console
luca@NTNU19403:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input2.json 
 
MEV Agent reporting for duty, ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 2
Number of Function Evaluations: 4
Number of Gradient Evaluations: 2
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 1081.081081081082174933
The resulting gamma is: 181.081081081082174933
Total coin conservation error: 2.0463631e-12
 
The resulting total value sold via   TAU -> PI -> PSI is: 1000.000000000000000000
The resulting total value bought via TAU -> PI -> PSI is: 1081.081081081082174933
```
With resulting JSON-file
```json
{
    "venues": {
        "AMM_TAU_PI": {
            "sell_token": "PI",
            "buy_token": "TAU",
            "ex_buy_amount": "1000_000000000000000000",
            "ex_sell_amount": "1818_181818181818698577"
        },
        "AMM_PI_PSI": {
            "sell_token": "PSI",
            "buy_token": "PI",
            "ex_buy_amount": "1818_181818181818698577",
            "ex_sell_amount": "1081_081081081082174933"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "PSI",
            "sell_token": "TAU",
            "ex_buy_amount": "1081_081081081082174933",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```
<div align="center">
  <img src="docs/images/graph_2_ex1.png" alt="Diagram">
  <p style="margin-top: 10px;">Strategy graph of the secon input.</p>
</div>

### Third input
```console
luca@NTNU19403:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input3.json 
 
MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 20
Number of Function Evaluations: 102
Number of Gradient Evaluations: 19
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 1301.146504402049686178
The resulting gamma is: 401.146504402049686178
Total coin conservation error: 3.2969438e-12
 
The resulting total value sold via   MU -> IOTA -> NU is: 289.120006524611255827
The resulting total value bought via MU -> IOTA -> NU is: 357.774322750772341806
 
The resulting total value sold via   MU -> RHO -> NU is: 0.000000000000000025
The resulting total value bought via MU -> RHO -> NU is: 0.000000000000000000
 
The resulting total value sold via   MU -> CHI -> NU is: 710.879993475388687330
The resulting total value bought via MU -> CHI -> NU is: 943.372181651277401215
```

With resulting JSON-file:
```json
{
    "venues": {
        "AMM_MU_IOTA": {
            "sell_token": "IOTA",
            "buy_token": "MU",
            "ex_buy_amount": "289_120006524611255827",
            "ex_sell_amount": "561_991708409024226967"
        },
        "AMM_MU_RHO": {
            "sell_token": "RHO",
            "buy_token": "MU",
            "ex_buy_amount": "0_000000000000000025",
            "ex_sell_amount": "0_000000000000000000"
        },
        "AMM_MU_CHI": {
            "sell_token": "CHI",
            "buy_token": "MU",
            "ex_buy_amount": "710_879993475388687330",
            "ex_sell_amount": "671_122685926031067538"
        },
        "AMM_IOTA_NU": {
            "sell_token": "NU",
            "buy_token": "IOTA",
            "ex_buy_amount": "561_991708409024226967",
            "ex_sell_amount": "357_774322750772341806"
        },
        "AMM_RHO_NU": {
            "sell_token": "NU",
            "buy_token": "RHO",
            "ex_buy_amount": "0_000000000000000000",
            "ex_sell_amount": "0_000000000000000000"
        },
        "AMM_CHI_NU": {
            "sell_token": "NU",
            "buy_token": "CHI",
            "ex_buy_amount": "671_122685926031067538",
            "ex_sell_amount": "943_372181651277401215"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "NU",
            "sell_token": "MU",
            "ex_buy_amount": "1301_146504402049686178",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```
<div align="center">
  <img src="docs/images/graph_3_ex1.png" alt="Diagram">
  <p style="margin-top: 10px;">Strategy graph of the third input.</p>
</div>

## Discussion
Numerical error is hindering the precision of the results, providing a coin conservation error in the order of 10**-12.

This for example results (in exercise 3) in exchanging a very small amount of coins through channel MU_RHO, resulting in zero coins bought.

This is for sure an error of my procedure. Maybe I should enforce global coin conservation, although I might be concerned with the convexity of such constraint.

