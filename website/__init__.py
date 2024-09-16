from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

db = SQLAlchemy()
DB_NAME = "database.db"

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Config database with increased pool size and overflow
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,  # Increase pool size
        'max_overflow': 20,  # Increase max overflow
        'pool_timeout': 30,  # Timeout before giving up on a connection
    }
    db.init_app(app)
    # Telling Flask Blueprints info
    from .views import views
    from .auth import auth

    # Registering with Flask
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Defining models in the db
    from .models import User, Chat
    create_database(app)

    # Keeping track of logins
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')