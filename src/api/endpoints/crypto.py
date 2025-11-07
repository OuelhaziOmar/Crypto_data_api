from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ...db.session import get_session
from ...api.models import OHLCV

router = APIRouter()

@router.get("/latest")
def fetch_latest_data(session: Session = Depends(get_session)):
    latest = session.exec(
        select(OHLCV).order_by(OHLCV.time.desc()).limit(1)
    ).first()

    return latest
