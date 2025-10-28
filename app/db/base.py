from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class PyObject(BaseModel):
    class Config:
        orm_mode = True
