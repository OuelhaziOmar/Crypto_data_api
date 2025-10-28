from sqlalchemy.engine import Engine
from sqlmodel import Session

from .activator import activate_timescaledb_extension
from .compression import sync_compression_policies
from .hypertables import sync_all_hypertables
from .retention import sync_retention_policies


def create_all(engine: Engine) -> None:
    with Session(engine) as session:
        activate_timescaledb_extension(session)
        sync_all_hypertables(session)
        sync_compression_policies(session)
        sync_retention_policies(session, drop_after="1 day")
