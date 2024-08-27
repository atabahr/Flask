#makes this folder a Python package 
from flask import Flask
import secrets
#setting up db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
#Configuring the FIREWORKS API key
    app.config['FIREWORKS_API_KEY'] = 'DIGaPgDjUZTeWJrTIZJzOAXWWn2fS9hGCA6tcKgtlyCxs1Xm'
#config db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #telling Flask Blueprints info
    from .views import views
    from .auth import auth

    #registering with Flask
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    #defining models in db
    from .models import User, Chat
    
    #create_database(app)
    create_database(app)
    
    #keeping tracks of logins  
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
