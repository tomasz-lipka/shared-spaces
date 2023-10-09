"""
Flask Application Initialization

This script creates and configures a Flask application.
It registers blueprints for user, space, assignment, and share controllers.
It also initializes the Flask-JWT-Extended extension for user authentication and provides the JWTManager.

The application uses SQLAlchemy for database operations.
And Amazon Web Services: SQS, Lambda and S3 Buckets to maintain images.

Usage:
    export AWS_ACCESS_KEY_ID=<value>
    export AWS_SECRET_ACCESS_KEY=<value>
    export SECRET_KEY=<value>
    export JWT_SECRET_KEY=<value>
    flask --app 'app:create_app("<your-file>.config")' run

Author:
    Tomasz Lipka
"""
import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import Injector
from flask_jwt_extended import JWTManager


from src.controller.user_controller import user_controller
from src.controller.space_controller import space_controller
from src.controller.assignment_controller import assignment_controller
from src.controller.share_controller import share_controller
from src.controller.image_controller import image_controller
from src.repository.sql_alchemy_repository import Repository
from src.service.image.image_service import ImageService
from src.model.tockenblocklist import TokenBlocklist
from appmodules import AppModules


def create_app(config_filename):
    app = Flask(__name__)

    app.config.from_pyfile(config_filename)
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=999)

    CORS(app, resources={r'*': {'origins': app.config['CORS_DOMAIN']}})

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

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        """
        From https://flask-jwt-extended.readthedocs.io/en/stable/
        Callback function to check if a JWT exists in the database blocklist
        """
        jti = jwt_payload["jti"]
        token = repository.get_first_by_filter(
            TokenBlocklist, TokenBlocklist.jti == jti)
        return token is not None

    app.engine = repository.engine

    return app
