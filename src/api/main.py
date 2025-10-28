from fastapi import FastAPI
from .endpoints import routeritem
from contextlib import asynccontextmanager
from ..db.session import init_db



@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app=FastAPI(lifespan=lifespan)
app.include_router(routeritem,prefix='/items')

@app.get('/')
def initapi():
    return{"Hello":"Api"}
