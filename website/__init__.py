from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
DB_NAME = "database.db"

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Config database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Load FIREWORKS_API_KEY into the app config
    app.config['FIREWORKS_API_KEY'] = os.getenv('FIREWORKS_API_KEY')

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