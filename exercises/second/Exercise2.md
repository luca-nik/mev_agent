# My solutions to Exercise 2

In this exercise I choose `ETH` and `USDC` as token pairs to swap.
In particular I considered a liquidity pool on UNiswap https://v2.info.uniswap.org/pair/0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc.

```json
{
    "orders": {
        "0": {
            "sell_token": "ETH",
            "buy_token": "USDC",
            "limit_sell_amount": "100_000000000000000000",
            "limit_buy_amount": "6000_000000000000000000",
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

Connettere un paio e fare l'exchange esemplificativo.
Qui dovro parlare delle gas-fees e del processo in realta' di mining del mio coso, per cui in realta' noi avremo casini causati da ordini di altri utenti che quindi potranno ridurre il nostro surplus

Inoltre dovro' vedere anche cosa vuol dire lo slippage.
Vedere in uniswap v3 come calcolano lo scambio, magari in alcune liquididty pools la funzione di prezzo non e' proprio giusta giusta.


Dire che in genere quando facciamo degli swaps su aggregatori tipo.., non e' garantito che sia a singolo hop, quindi non necessariamente avro gli stessi risultati.

-gas prices
-multiple hops
-price slippage
-non perfect constant-product price functions
