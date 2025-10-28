
# db/models.py
from sqlmodel import Field, SQLModel
from datetime import date, datetime
from typing import Optional
from ..timescaledb import TimescaleModel

class Cryptocurrency(SQLModel, table=True):
    __tablename__ = "dim_cryptocurrency"

    crypto_id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, unique=True)
    name: str
    sector: Optional[str]
    launch_date: Optional[date]

class Exchange(SQLModel, table=True):
    __tablename__ = "dim_exchange"

    exchange_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    region: Optional[str]
    trading_fees: Optional[float]

class OHLCV(TimescaleModel, table=True):
    __tablename__ = "fact_ohlcv"

    # --- Timescale configuration ---
    __time_column__ = "time"             # which column is the time index
    __chunk_time_interval__ = "7 days"   # how big each chunk is
    __drop_after__ = None                # keep data indefinitely
    __enable_compression__ = True        # enable compression
    __compress_orderby__ = "time DESC"   # compression order
    __compress_segmentby__ = "crypto_id" # segment compression by coin

    # --- Dimensions ---
    crypto_id: int = Field(foreign_key="dim_cryptocurrency.crypto_id", nullable=False)
    exchange_id: int = Field(foreign_key="dim_exchange.exchange_id", nullable=False)

    # --- OHLCV metrics ---
    open: float
    high: float
    low: float
    close: float
    volume: float

    # --- Derived indicators ---
    sma_20: Optional[float] = None
    ema_50: Optional[float] = None
    rsi_14: Optional[float] = None

class TechnicalIndicators(TimescaleModel, table=True):
      __tablename__ = "fact_technical_indicators"

      crypto_id: int = Field(foreign_key="dim_cryptocurrency.crypto_id", primary_key=True)
      time: datetime = Field(primary_key=True)

      sma_20: Optional[float] = None
      sma_50: Optional[float] = None
      ema_20: Optional[float] = None
      ema_100: Optional[float] = None
      rsi: Optional[float] = None
      macd: Optional[float] = None
      signal: Optional[float] = None


class Sentiment(TimescaleModel, table=True):
        __tablename__ = "fact_sentiment"

        crypto_id: int = Field(foreign_key="dim_cryptocurrency.crypto_id", primary_key=True)
        time: datetime = Field(primary_key=True)

        positive: Optional[float] = None
        negative: Optional[float] = None
        neutral: Optional[float] = None
        overall_score: Optional[float] = None
        source: Optional[str] = None  # e.g., Twitter, Reddit, NewsAPI

class PortfolioPerformance(TimescaleModel, table=True):
     __tablename__ = "fact_portfolio_performance"

     portfolio_id: int = Field(primary_key=True)
     crypto_id: int = Field(foreign_key="dim_cryptocurrency.crypto_id", primary_key=True)
     time: datetime = Field(primary_key=True)

     quantity: float
     value_usd: float
     pnl_percentage: Optional[float] = None
     momentum: Optional[float] = None    