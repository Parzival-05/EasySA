from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import CommonConfig

engine = create_engine(CommonConfig.DB_URL, echo=True)
session_maker = sessionmaker(bind=engine)
db_session = session_maker()
