from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

import DatabaseService


class Stock(DatabaseService.Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    parent = relationship("User", back_populates="interests")

    def __repr__(self):
        return "%s:%s" % (self.name, self.value)