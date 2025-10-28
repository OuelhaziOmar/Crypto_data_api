from fastapi import FastAPI
from .endpoints import routeritem
from contextlib import asynccontextmanager
from ..db.session import init_db
import asyncio
#from ..core.etl.ohlcv_liveupdate import LiveOHLCVETL
from ..core.etl.ohlcv_batch import OHLCVETL

from ..core.static_dimensions.dimcryptocurrency import seed_cryptocurrencies
from ..core.static_dimensions.dimexchange import seed_exchanges


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    ohlcv_etl = OHLCVETL(symbol="BTC/USDT", exchange_name="binance", timeframe="1m",limit=1)
    task = asyncio.create_task(ohlcv_etl.run())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("OHLCVETL stopped.")

app = FastAPI(lifespan=lifespan)

"""
#live data saving_ it's not my goal here but could be a solution for any wonderer
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    live_etl = LiveOHLCVETL(symbol="BTC/USDT", exchange_name="binance")
    task = asyncio.create_task(live_etl.run())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Live OHLCV streaming stopped.")
"""


app.include_router(routeritem,prefix='/admin')

@app.get('/')
def initapi():
    return{"Hello":"Api"}
