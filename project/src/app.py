from flask import Flask
from flask_login import LoginManager
import secrets

from controller.user_controller import user_controller
from repository.sql_alchemy_repository import SqlAlchemyRepository
from model.user import User


app = Flask(__name__)
app.register_blueprint(user_controller)

# Generates a 32-byte (64-character) random hex string
app.config["SECRET_KEY"] = secrets.token_hex(32)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Request loader according to Flask-Login library"""
    return SqlAlchemyRepository().get_by_id(User, user_id)


@app.route("/")
def hello_world():
    """Hello world"""
    return "<p>Hello, World!</p>"
