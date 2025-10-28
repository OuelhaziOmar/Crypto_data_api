# etl/live_ohlcv_etl.py
import asyncio
from datetime import datetime
from typing import Optional

import ccxt.pro
from sqlmodel import select
from sqlalchemy import func

from ...db.models import OHLCV, Cryptocurrency, Exchange
from ...db.session import get_session


class LiveOHLCVETL:
    """
    Live 1-second OHLCV ETL using ccxt.pro WebSocket trades.
    Aggregates trades into 1-second candles and saves each second to DB.
    """

    def __init__(self, symbol: str, exchange_name: str):
        self.symbol = symbol
        self.exchange_name = exchange_name
        self.exchange: Optional[ccxt.pro.Exchange] = None
        self.crypto_id: Optional[int] = None
        self.exchange_id: Optional[int] = None
        self.current_candle = {"open": None, "high": None, "low": None, "close": None, "volume": 0, "time": None}

    async def init(self):
        # Initialize exchange object and load markets
        exchange_class = getattr(ccxt.pro, self.exchange_name)
        self.exchange = exchange_class()
        await self.exchange.load_markets()

        # Load dimension references
        base_symbol = self.symbol.split("/")[0].upper()
        with next(get_session()) as session:
            crypto = session.exec(
                select(Cryptocurrency).where(func.upper(Cryptocurrency.symbol) == base_symbol)
            ).first()
            exchange_dim = session.exec(
                select(Exchange).where(func.upper(Exchange.name) == self.exchange_name.upper())
            ).first()

        if not crypto or not exchange_dim:
            raise ValueError("Cryptocurrency or Exchange not found in dimensions!")

        self.crypto_id = crypto.crypto_id
        self.exchange_id = exchange_dim.exchange_id

    async def run(self):
        """Main loop: fetch trades, aggregate per-second OHLCV, save each second."""
        if not self.exchange:
            await self.init()

        while True:
            trades = await self.exchange.watch_trades(self.symbol)
            for trade in trades:
                ts = datetime.utcfromtimestamp(trade['timestamp'] / 1000)
                second = ts.replace(microsecond=0)

                # New second → save previous candle
                if self.current_candle["time"] != second:
                    if self.current_candle["time"] is not None:
                        self.save_candle(self.current_candle)

                    # Reset candle
                    self.current_candle = {
                        "open": trade['price'],
                        "high": trade['price'],
                        "low": trade['price'],
                        "close": trade['price'],
                        "volume": trade['amount'],
                        "time": second
                    }
                else:
                    # Update rolling candle
                    self.current_candle["high"] = max(self.current_candle["high"], trade['price'])
                    self.current_candle["low"] = min(self.current_candle["low"], trade['price'])
                    self.current_candle["close"] = trade['price']
                    self.current_candle["volume"] += trade['amount']

    def save_candle(self, candle: dict):
        """Save the aggregated candle to TimescaleDB."""
        with next(get_session()) as session:
            record = OHLCV(
                crypto_id=self.crypto_id,
                exchange_id=self.exchange_id,
                time=candle["time"],
                open=candle["open"],
                high=candle["high"],
                low=candle["low"],
                close=candle["close"],
                volume=candle["volume"]
            )
            session.add(record)
            session.commit()
