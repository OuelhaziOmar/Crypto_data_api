from fastapi import APIRouter,Depends
from ...db.models import *
from sqlmodel import Session,select
from ...db.session import get_session
from timescaledb import TimescaleModel
from ...core.static_dimensions.dimcryptocurrency import seed_cryptocurrencies
from ...core.static_dimensions.dimexchange import seed_exchanges

router=APIRouter()

@router.post('/dimcrypt')
def addcryptocurrencies():
    seed_cryptocurrencies()
    return {'result':'dim fed'}
@router.post('/dimexchange')
def addcryptocurrencies():
    seed_exchanges()
    return {'result':'dim fed'}

