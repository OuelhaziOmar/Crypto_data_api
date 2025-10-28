from fastapi import APIRouter,Depends
from ...db.models import *
from sqlmodel import Session,select
from ...db.session import get_session
from ...timescaledb import TimescaleModel


router=APIRouter()

