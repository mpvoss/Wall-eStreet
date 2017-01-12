from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select
import DatabaseService


class Stock(DatabaseService.Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volumn = Column(Integer)
    adj_close = Column(Float)

    def __repr__(self):
        return "%s:%s" % (self.ticker)

