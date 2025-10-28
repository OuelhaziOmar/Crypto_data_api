# etl/base_etl.py
from abc import ABC, abstractmethod
from sqlmodel import Session

from ...db.session import get_session
class BaseETL(ABC):
    """Abstract base class for all ETL processes."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract(self):
        """Fetch raw data from an external source."""
        pass

    @abstractmethod
    def transform(self, data):
        """Clean and format data into a warehouse-ready structure."""
        pass

    @abstractmethod
    def load(self, transformed):
        """Insert or update data in the database."""
        pass

    def run(self):
        """Full ETL flow with basic error handling."""
        print(f"🚀 Starting ETL: {self.name}")
        try:
            raw = self.extract()
            transformed = self.transform(raw)
            self.load(transformed)
            print(f"✅ ETL {self.name} completed successfully.")
        except Exception as e:
            print(f"❌ ETL {self.name} failed: {e}")
