"""
Flask Application Initialization

This script creates and configures a Flask application.
It registers blueprints for user, space, assignment, and share controllers.
It also initializes the Flask-Login extension for user authentication and provides the LoginManager.

The application uses SQLAlchemy for database operations.
And Amazon Web Services: SQS, Lambda and S3 Buckets to maintain images.

Usage:
    flask --app 'app:create_app("<your-file>.config")' run

Author:
    Tomasz Lipka
"""
import secrets
from flask import Flask
from flask_injector import FlaskInjector
from flask_login import LoginManager
from injector import Injector


from src.controller.user_controller import user_controller
from src.controller.space_controller import space_controller
from src.controller.assignment_controller import assignment_controller
from src.controller.share_controller import share_controller
from src.controller.image_controller import image_controller
from src.repository.sql_alchemy_repository import Repository
from src.media.image_service import ImageService
from src.model.user import User
from appmodules import AppModules


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    app.config["SECRET_KEY"] = secrets.token_hex(32)

    app.register_blueprint(user_controller)
    app.register_blueprint(space_controller)
    app.register_blueprint(assignment_controller)
    app.register_blueprint(share_controller)
    app.register_blueprint(image_controller)

    app_modules = [AppModules(app)]

    FlaskInjector(app=app, modules=app_modules)
    injector = Injector(app_modules)
    repository = injector.get(Repository)

    repository.create_schema()
    injector.get(ImageService).create_temp_directory()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Request loader according to Flask-Login library"""
        return repository.get_by_id(User, user_id)

    app.engine = repository.engine

    return app
