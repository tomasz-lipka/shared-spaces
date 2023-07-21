import db
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=db.engine)
session = Session()


def create_user(email):
    user = db.User(email)
    session.add(user)
    session.commit()

def get_all_users():
    return session.query(db.User).all()

def find_user_by_email(email):
    return session.query(db.User).filter(db.User.email==email)
