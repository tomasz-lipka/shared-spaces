from sqlalchemy import create_engine
from base import Base
from user import User


# connect with data base
engine = create_engine('sqlite:///sqlalchemy.sqlite')
Base.metadata.create_all(engine)