from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class BaseIDModel(BaseModel):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
