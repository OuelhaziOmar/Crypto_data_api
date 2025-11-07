# db/seed_dimensions.py

from sqlmodel import Session, select
from ...api.models import Exchange
from ...db.session import get_session

def seed_exchanges():
    exchanges = [
        {"name": "Binance", "region": "Global", "trading_fees": 0.1},
        {"name": "Coinbase Pro", "region": "USA", "trading_fees": 0.5},
        {"name": "Kraken", "region": "USA", "trading_fees": 0.26},
        {"name": "Bitfinex", "region": "Global", "trading_fees": 0.2},
        {"name": "Huobi", "region": "Asia", "trading_fees": 0.2},
        {"name": "OKX", "region": "Global", "trading_fees": 0.15},
        {"name": "Gemini", "region": "USA", "trading_fees": 0.35},
        {"name": "Bitstamp", "region": "Europe", "trading_fees": 0.25},
        {"name": "Bittrex", "region": "Global", "trading_fees": 0.25},
        {"name": "KuCoin", "region": "Global", "trading_fees": 0.1}
    ]

    with next(get_session()) as session:
        for ex in exchanges:
            # Check if exchange already exists (by name)
            exists = session.exec(
                select(Exchange).where(Exchange.name == ex["name"])
            ).first()

            if exists:
                print(f"⚠️ {ex['name']} already exists — skipping")
                continue

            session.add(Exchange(**ex))

        session.commit()

    print("✅ Inserted missing exchanges successfully")
