# Crypto Live Data Tracker
##Reminder: This is a downscaled prove to see how the project behaves but it will actually be extanded in next commits


A FastAPI project to track live cryptocurrency OHLCV data using **CCXT**, with database storage and asynchronous updates.

In this project we trying to adapt data warehouse so it supports live data and not only historical data

I am going to use timescaledb hypertables for the fact tables to enhance data storage and retrieval of time series data

In TimescaleDB, a hypertable is a virtual table that automatically partitions data into time- and optionally space-based “chunks”, 
which are smaller physical tables optimized for fast inserts, queries, and retention policies.

To simplify The hypertables are going to behave like normal tables for the user (same sql commands behavior) thanks to an in-between
system that acts like a translator between the commands and the table chunks created where data actually resides

We are going to see how the database will continuosly save the data but still able to provide data for api endpoints

## Features

- Fetch and store cryptocurrency data from multiple exchanges using CCXT API
- Live OHLCV updates using WebSocket (where supported)
- Asynchronous FastAPI app for non-blocking operations
- PostgreSQL (TimeScaleDB) database integration with SQLModel
- Automated seeding of dimensions
- Automated ETL pipelines for real-time data handling

##Reminder: This is a downscaled prove to see how the project behaves but it will actually be extanded in next commits
## Data Warehouse Structure

### Dimension Tables

#### `dim_cryptocurrency`
Stores information about cryptocurrencies.

| Column       | Type       | Notes |
|--------------|-----------|-------|
| crypto_id    | int       | Primary key |
| symbol       | string    | Ticker symbol, e.g., BTC/USDT |
| name         | string    | Full name of the cryptocurrency, e.g., Bitcoin |
| sector       | string    | Category or sector of the cryptocurrency, e.g., Layer 1, DeFi |
| launch_date  | date      | Launch date of the cryptocurrency |

#### `dim_exchange`
Stores information about exchanges.

| Column        | Type       | Notes |
|---------------|-----------|-------|
| exchange_id   | int       | Primary key |
| name          | string    | Exchange name, e.g., Binance |
| region        | string    | Region or country of the exchange |
| trading_fees  | float     | Typical trading fee percentage, e.g., 0.1 |

### Fact Table

#### `fact_ohlcv`
Stores OHLCV (Open, High, Low, Close, Volume) data.

| Column       | Type       | Notes |
|--------------|-----------|-------|
| crypto_id    | int       | Foreign key → `dim_cryptocurrency.crypto_id` |
| exchange_id  | int       | Foreign key → `dim_exchange.exchange_id` |
| timestamp    | timestamp | Candle timestamp |
| open         | float     | Open price |
| high         | float     | High price |
| low          | float     | Low price |
| close        | float     | Close price |
| volume       | float     | Traded volume |
