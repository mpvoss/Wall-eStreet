import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


# Real Postgres DB
engine = create_engine('postgresql://postgres:postgres@localhost:5432/wallstreet')

Base = declarative_base()

def setup_db():
    # Boilerplate configuration

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()



