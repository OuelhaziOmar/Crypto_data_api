import ccxt.pro as ccxt
import asyncio
from datetime import datetime
from typing import List
from sqlmodel import select
from sqlalchemy import func
import logging
logger = logging.getLogger(__name__)

from ...api.models import OHLCV, Cryptocurrency, Exchange
from .base_etl import BaseETL
from ...db.session import get_session


class OHLCVEL_Live(BaseETL):
    def __init__(self, symbol: str, exchange_name: str, timeframe="1s"):
        super().__init__(f"OHLCV_{symbol}_{exchange_name}")
        self.symbol = symbol
        self.exchange_name = exchange_name
        self.timeframe = timeframe

        self.exchange = getattr(ccxt, exchange_name)({
            "enableRateLimit": True
        })

    async def extract(self) -> List[dict]:
        """
        Extract latest real-time candle as list of dicts.
        """
        candles = await self.exchange.watch_ohlcv(self.symbol, self.timeframe)
        c = candles[-1]  # latest

        return [{
            "time": datetime.fromtimestamp(c[0] / 1000),
            "open": c[1],
            "high": c[2],
            "low": c[3],
            "close": c[4],
            "volume": c[5],
        }]
    def transform(self, data):
        pass

    def load(self, transformed: List[dict]):
        """
        Insert into DB, skip duplicates, ensure dimension consistency.
        """
        with next(get_session()) as session:
            # Find crypto dimension
            crypto = session.exec(
                select(Cryptocurrency).where(
                    func.upper(Cryptocurrency.symbol) == self.symbol.split("/")[0].upper()
                )
            ).first()

            # Find exchange dimension
            exchange = session.exec(
                select(Exchange).where(
                    func.upper(Exchange.name) == self.exchange_name.upper()
                )
            ).first()

            if not crypto or not exchange:
                raise ValueError("Cryptocurrency or exchange not found in dimension tables.")

            for row in transformed:
                exists = session.exec(
                    select(OHLCV).where(
                        (OHLCV.crypto_id == crypto.crypto_id) &
                        (OHLCV.exchange_id == exchange.exchange_id) &
                        (OHLCV.time == row["time"])
                    )
                ).first()

                if exists:
                    continue  # avoid duplicates

                record = OHLCV(
                    crypto_id=crypto.crypto_id,
                    exchange_id=exchange.exchange_id,
                    **row
                )
                session.add(record)

            session.commit()

    async def run(self):
        """
        Continuous live ETL loop.
        """
        while True:
            try:
                row = await self.extract()
                print()
                self.load(row)
                logger.info(f"Inserted OHLCV candle for {self.symbol}")
            except Exception as e:
                logger.error(f"OHLCV ETL error: {e}")
                await asyncio.sleep(2)

