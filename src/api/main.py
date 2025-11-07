from fastapi import FastAPI
from .endpoints import routercrypto
from contextlib import asynccontextmanager
from ..db.session import init_db
import asyncio
#from ..core.etl.ohlcv_liveupdate import LiveOHLCVETL
from  ..core.etl.EL_OHLCVLive import OHLCVEL_Live
from ..core.Dimensions.dimcryptocurrency import seed_cryptocurrencies
from ..core.Dimensions.dimexchange import seed_exchanges

ohlcv_el = OHLCVEL_Live(symbol="BTC/USDT", exchange_name="binance", timeframe="1s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_cryptocurrencies()
    seed_exchanges()
    task = asyncio.create_task(ohlcv_el.run())
    print("▶ App started")
    yield 
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(routercrypto,prefix='/crypto')

@app.get('/')
def initapi():
    return{"Hello":"Api"}
