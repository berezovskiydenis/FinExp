from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_class


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.sign_in'


def create_app(config='default'):
    app = Flask(__name__)
    app.config.from_object(config_class[config])

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.account import bp as account_bp
    app.register_blueprint(account_bp)

    from app.reference import bp as reference_bp
    app.register_blueprint(reference_bp)

    from app.transaction import bp as transaction_bp
    app.register_blueprint(transaction_bp)

    return app

from app import models
