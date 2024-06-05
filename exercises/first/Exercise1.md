# My Solutions of Excercise 1

To replicate the solutions I provide it is sufficient to run the code 
```console
example@example:~$PATH-TO-MEV_AGENT/mev_agent/exercises/first$ python3 maximize_surplus.py input.json
```
Where `input.json` is one of the three inputs provided.

In this case the keyword `partial_fill = false` in all the user orders, thus we are in a *Fly-or-kill* situation.


In the following I report the solutions I obtained emplyoing my protocol and my program.

### First input
```console
luca@lime:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input1.json 
 
MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 2
Number of Function Evaluations: 4
Number of Gradient Evaluations: 2
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 909.090909090909121915
The resulting gamma is: 9.090909090909121915
Total coin conservation error: 2.2737368e-13
 
The resulting total value sold via   RHO -> KAPPA is: 1000.000000000000000000
The resulting total value bought via RHO -> KAPPA is: 909.090909090909121915

```

With resulting JSON-file
```json
{
    "venues": {
        "AMM_RHO_KAPPA": {
            "sell_token": "KAPPA",
            "buy_token": "RHO",
            "ex_buy_amount": "1000_000000000000000000",
            "ex_sell_amount": "909_090909090909121915"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "KAPPA",
            "sell_token": "RHO",
            "ex_buy_amount": "909_090909090909121915",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```

<div align="center">
  <img src="https://github.com/nicoli-luca/mev_agent/blob/main/docs/images/graph_1_ex1.png" alt="Diagram" width="60%" height="60%">
  <p style="margin-top: 10px;">Strategy graph of the first input.</p>
</div>

### Second Input
```console
luca@lime:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input2.json 
 
MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 0
Message: Optimization terminated successfully
Number of Iterations: 2
Number of Function Evaluations: 4
Number of Gradient Evaluations: 2
 
 
The resulting total value sold   (via all paths) is: 1000.000000000000000000
The resulting total value bought (via all paths) is: 1081.081081081081038064
The resulting gamma is: 181.081081081081038064
Total coin conservation error: 2.2737368e-13
 
The resulting total value sold via   TAU -> PI -> PSI is: 1000.000000000000000000
The resulting total value bought via TAU -> PI -> PSI is: 1081.081081081081038064

```
With resulting JSON-file
```json
{
    "venues": {
        "AMM_TAU_PI": {
            "sell_token": "PI",
            "buy_token": "TAU",
            "ex_buy_amount": "1000_000000000000000000",
            "ex_sell_amount": "1818_181818181818243829"
        },
        "AMM_PI_PSI": {
            "sell_token": "PSI",
            "buy_token": "PI",
            "ex_buy_amount": "1818_181818181818243829",
            "ex_sell_amount": "1081_081081081081038064"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "PSI",
            "sell_token": "TAU",
            "ex_buy_amount": "1081_081081081081038064",
            "ex_sell_amount": "1000_000000000000000000"
        }
    }
}
```
<div align="center">
  <img src="https://github.com/nicoli-luca/mev_agent/blob/main/docs/images/graph_2_ex1.png" alt="Diagram" width="60%" height="60%">
  <p style="margin-top: 10px;">Strategy graph of the secon input.</p>
</div>

### Third input
```console
luca@lime:~/programmi/mev_agent/exercises/first$ python3 maximize_surplus.py input3.json 
 
MEV Agent ready to maximize the surplus .. or at least trying :)
 
Status: 8
Message: Positive directional derivative for linesearch
Number of Iterations: 42
Number of Function Evaluations: 356
Number of Gradient Evaluations: 38
 
 
The resulting total value sold   (via all paths) is: 1000.000000000019440449
The resulting total value bought (via all paths) is: 1301.146505249534584436
The resulting gamma is: 401.146505249517076663
Total coin conservation error: 1.1368684e-13
 
The resulting total value sold via   MU -> IOTA -> NU is: 289.078085936060801941
The resulting total value bought via MU -> IOTA -> NU is: 357.725107553711382025
 
The resulting total value sold via   MU -> RHO -> NU is: 0.000000000000000010
The resulting total value bought via MU -> RHO -> NU is: 0.000000000000000007
 
The resulting total value sold via   MU -> CHI -> NU is: 710.921914063958638508
The resulting total value bought via MU -> CHI -> NU is: 943.421397695823088725

```

With resulting JSON-file:
```json
{
    "venues": {
        "AMM_MU_IOTA": {
            "sell_token": "IOTA",
            "buy_token": "MU",
            "ex_buy_amount": "289_078085936060801941",
            "ex_sell_amount": "561_912512514014224507"
        },
        "AMM_MU_RHO": {
            "sell_token": "RHO",
            "buy_token": "MU",
            "ex_buy_amount": "0_000000000000000010",
            "ex_sell_amount": "0_000000000000000005"
        },
        "AMM_MU_CHI": {
            "sell_token": "CHI",
            "buy_token": "MU",
            "ex_buy_amount": "710_921914063958638508",
            "ex_sell_amount": "671_160048534979750912"
        },
        "AMM_IOTA_NU": {
            "sell_token": "NU",
            "buy_token": "IOTA",
            "ex_buy_amount": "561_912512514014224507",
            "ex_sell_amount": "357_725107553711382025"
        },
        "AMM_RHO_NU": {
            "sell_token": "NU",
            "buy_token": "RHO",
            "ex_buy_amount": "0_000000000000000005",
            "ex_sell_amount": "0_000000000000000007"
        },
        "AMM_CHI_NU": {
            "sell_token": "NU",
            "buy_token": "CHI",
            "ex_buy_amount": "671_160048534979750912",
            "ex_sell_amount": "943_421397695823088725"
        }
    },
    "orders": {
        "0": {
            "partial_fill": false,
            "buy_amount": "900_000000000000000000",
            "sell_amount": "1000_000000000000000000",
            "buy_token": "NU",
            "sell_token": "MU",
            "ex_buy_amount": "1301_146505249534584436",
            "ex_sell_amount": "1000_000000000019440449"
        }
    }
}
```
<div align="center">
  <img src="https://github.com/nicoli-luca/mev_agent/blob/main/docs/images/graph_3_ex1.png" alt="Diagram" width="60%" height="60%">
  <p style="margin-top: 10px;">Strategy graph of the third input.</p>
</div>

## Discussion
In this exercise we are considering a constant product AMM with zero gas-fees. The price function will thus be b(x) = xB/(A+x)

Regarding my results, numerical error is hindering the precision of the results, providing a coin conservation error in the order of 10**-13.
This is probably responsible for opening a the MU -> RHO -> NU channel in the third exercise.

This is for sure an error of my procedure. Maybe I should enforce global coin conservation, although I might be concerned with the convexity of such constraint.

Regarding the advantages of this procedure is that it is extremely fast since we are not searching for a gloabl minimum on a rough surface, but rather we just need to find the minimum of such convex problem. (We are minimizing -surplus).
Something that has to be noticed is that in all cases we are actually enforcing to sell the complete amount of coins (this is due to the keyword `partial_fill`). In this case, we might not hit the absolute maximum of the surplus.
