"""
Flask Application Initialization

This script creates and configures a Flask application.
It registers blueprints for user, space, assignment, and share controllers.
It also initializes the Flask-Login extension for user authentication and provides the LoginManager.

The application uses SQLAlchemy for database operations.

Usage:
    To start the Flask application, run this script.

Author:
    Tomasz Lipka
"""
import secrets
from flask import Flask
from flask_injector import FlaskInjector
from flask_login import LoginManager

from src.controller.user_controller import user_controller
from src.controller.space_controller import space_controller
from src.controller.assignment_controller import assignment_controller
from src.controller.share_controller import share_controller
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.model.user import User
from appmodules import AppModules

app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(space_controller)
app.register_blueprint(assignment_controller)
app.register_blueprint(share_controller)

app.config["SECRET_KEY"] = secrets.token_hex(32)

login_manager = LoginManager()
login_manager.init_app(app)

FlaskInjector(app=app, modules=[AppModules()])


@login_manager.user_loader
def load_user(user_id):
    """Request loader according to Flask-Login library"""
    return SqlAlchemyRepository().get_by_id(User, user_id)

#
#
# create_temp_bucket()
#
#
#  def create_db_schema(self):
