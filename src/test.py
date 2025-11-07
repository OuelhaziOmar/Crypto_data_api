import asyncio
import ccxt.pro as ccxt

async def main():
    exchange = ccxt.binance()

    while True:
        ohlcv = await exchange.watch_ohlcv('BTC/USDT', '1s')
        last_candle = ohlcv[-1]
        print("Time:", last_candle[0], 
              "O:", last_candle[1], 
              "H:", last_candle[2], 
              "L:", last_candle[3], 
              "C:", last_candle[4], 
              "V:", last_candle[5])

asyncio.run(main())