from decouple import config as db_config
from sqlmodel import SQLModel, create_engine, Session, select
from ..timescaledb import TimescaleModel
DATABASE_URL = db_config('DATABASE_URL', default='')
DB_NAME = db_config('Db_name', default='')

if not DATABASE_URL:
    raise NotImplementedError("DATABASE_URL needs to be set")

engine = create_engine(DATABASE_URL, echo=True, connect_args={"options": "-c timezone=utc"})

def init_db():
    print(f"Creating tables in database: {DB_NAME}")
    SQLModel.metadata.create_all(engine)
    print(f"Creating Hypertables in database: {DB_NAME}")
    TimescaleModel.metadata.create_all(engine)


    try:
        with Session(engine) as session:
            session.exec(select(1))
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
