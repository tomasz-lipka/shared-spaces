from flask import Flask
from flask_login import LoginManager
import secrets

from src.controller.user_controller import user_controller
from src.controller.space_controller import space_controller
from src.controller.assignment_controller import assignment_controller
from src.controller.share_controller import share_controller
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_controller)
    app.register_blueprint(space_controller)
    app.register_blueprint(assignment_controller)
    app.register_blueprint(share_controller)
    # Generates a 32-byte (64-character) random hex string
    app.config["SECRET_KEY"] = secrets.token_hex(32)

    return app


app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Request loader according to Flask-Login library"""
    return SqlAlchemyRepository().get_by_id(User, user_id)
