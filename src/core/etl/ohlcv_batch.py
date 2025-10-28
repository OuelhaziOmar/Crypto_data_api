# etl/ohlcv_etl.py
import ccxt
import asyncio
from datetime import datetime
from sqlmodel import select
from typing import List
from sqlalchemy import func

from ...db.models import OHLCV, Cryptocurrency, Exchange
from .base_etl import BaseETL
from ...db.session import get_session


class OHLCVETL(BaseETL):
    def __init__(self, symbol: str, exchange_name: str, timeframe="1m", limit=200):
        super().__init__(f"OHLCV_{symbol}_{exchange_name}")
        self.symbol = symbol
        self.exchange_name = exchange_name
        self.timeframe = timeframe
        self.limit = limit
        self.exchange = getattr(ccxt, exchange_name)()

    def extract(self) -> List[list]:
        """Blocking OHLCV fetch"""
        print(f"Fetching {self.symbol} {self.timeframe} candles from {self.exchange_name}...")
        return self.exchange.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=self.limit)

    def transform(self, data: List[list]) -> List[dict]:
        transformed = []
        for ohlcv in data:
            t = datetime.utcfromtimestamp(ohlcv[0] / 1000)
            transformed.append({
                "time": t,
                "open": ohlcv[1],
                "high": ohlcv[2],
                "low": ohlcv[3],
                "close": ohlcv[4],
                "volume": ohlcv[5]
            })
        return transformed

    def load(self, transformed: List[dict]):
        """Insert into DB skipping duplicates"""
        with next(get_session()) as session:
            crypto = session.exec(
                select(Cryptocurrency).where(func.upper(Cryptocurrency.symbol) == self.symbol.split("/")[0].upper())
            ).first()
            exchange = session.exec(
                select(Exchange).where(func.upper(Exchange.name) == self.exchange_name.upper())
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
                    continue

                record = OHLCV(
                    crypto_id=crypto.crypto_id,
                    exchange_id=exchange.exchange_id,
                    **row
                )
                session.add(record)
            session.commit()

    async def run(self):
        """Asynchronous loop fetching 1-minute OHLCV continuously"""
        while True:
            try:
                # Run blocking extract/transform/load in a thread
                data = await asyncio.to_thread(self.extract)
                transformed = await asyncio.to_thread(self.transform, data)
                await asyncio.to_thread(self.load, transformed)
            except Exception as e:
                print("OHLCVETL error:", e)

            await asyncio.sleep(60)  # wait 1 minute
