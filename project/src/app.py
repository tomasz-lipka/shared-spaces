from typing import Any
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# connect with data base
engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)

# manage tables
base = declarative_base()

class user (base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String)

    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

base.metadata.create_all(engine)


@app.route("/")
def hello_world():
    return "<p>Hello, World2!</p>"