
# db/seed_dimensions.py
from sqlmodel import Session
from ...db.models import Cryptocurrency
from ...db.session import get_session
from datetime import date

def seed_cryptocurrencies():
    cryptos = [
        {"symbol": "BTC", "name": "Bitcoin", "sector": "Currency", "launch_date": date(2009, 1, 3)},
        {"symbol": "ETH", "name": "Ethereum", "sector": "Smart Contract", "launch_date": date(2015, 7, 30)},
        {"symbol": "BNB", "name": "Binance Coin", "sector": "Exchange Token", "launch_date": date(2017, 7, 25)},
        {"symbol": "ADA", "name": "Cardano", "sector": "Smart Contract", "launch_date": date(2017, 9, 29)},
        {"symbol": "SOL", "name": "Solana", "sector": "Smart Contract", "launch_date": date(2020, 3, 1)},
        {"symbol": "XRP", "name": "Ripple", "sector": "Payment", "launch_date": date(2012, 8, 2)},
        {"symbol": "DOT", "name": "Polkadot", "sector": "Smart Contract", "launch_date": date(2020, 5, 26)},
        {"symbol": "LTC", "name": "Litecoin", "sector": "Currency", "launch_date": date(2011, 10, 13)},
        {"symbol": "LINK", "name": "Chainlink", "sector": "Oracle", "launch_date": date(2017, 9, 19)},
        {"symbol": "DOGE", "name": "Dogecoin", "sector": "Currency", "launch_date": date(2013, 12, 6)}
    ]

    with next(get_session()) as session:
        for crypto in cryptos:
            session.add(Cryptocurrency(**crypto))
        session.commit()
    print("✅ Inserted 10 cryptocurrencies")

