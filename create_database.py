from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'USERINFO'

    id = Column(Integer, primary_key = True)
    username = Column(String)
    client_database_id = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_time = Column(BigInteger)
    idle_time = Column(BigInteger)
    messege_sent = Column(Boolean)
    online = Column(Boolean)


engine = create_engine(
    "postgresql://postgres:hog55555@localhost:5432/teamspeak"
)

Base.metadata.create_all(engine)