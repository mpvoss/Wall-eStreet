from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
import DatabaseService


class Stock(DatabaseService.Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    timestamp = Column(Date)
    adj_close = Column(Float)

    def __repr__(self):
        return "%s" % (self.ticker)

