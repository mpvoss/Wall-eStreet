from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
import math
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


    def __init__(self, ticker, high, low, open, close, volume, adj_close, timestamp):
        self.ticker = ticker
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.adj_close = adj_close
        self.timestamp = timestamp

    def is_nan(self):
        return math.isnan(self.adj_close) or math.isnan(self.high) or math.isnan(self.low) or math.isnan(self.open) or math.isnan(self.close) or math.isnan(self.volume)

    def __repr__(self):
        return "%s" % (self.ticker)

