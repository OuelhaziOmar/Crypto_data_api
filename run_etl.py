from src.core.etl.ohlcv import OHLCVETL
if __name__ == "__main__":
    etl = OHLCVETL(symbol="BTC/USDT", exchange_name="binance", timeframe="1h")
    etl.run()