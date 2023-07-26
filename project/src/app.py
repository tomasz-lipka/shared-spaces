from flask import Flask
from flask_login import LoginManager, login_required
import secrets
from controller.auth_controller import auth_controller
import repository.user_repository as repository
from exception.repository_exception import RepositoryException


app = Flask(__name__)
app.register_blueprint(auth_controller)
# Generates a 32-byte (64-character) random hex string
app.config["SECRET_KEY"] = secrets.token_hex(32)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Request loader according to Flask-Login library"""
    return repository.get_user_by_id(user_id)


@app.route("/")
@login_required
def hello_world():
    """Hello world"""
    return "<p>Hello, World!</p>"
