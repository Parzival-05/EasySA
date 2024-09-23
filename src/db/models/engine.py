from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from config import CommonConfig

engine = create_engine(CommonConfig.DB_URL, echo=True)
session_maker = sessionmaker(bind=engine)
db_session = session_maker()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
