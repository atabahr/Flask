#db models 
#in current directory . 
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 
 
#db model for users storing objects
#db model for messages 
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
#associate different info with different users with foreign key
#lower case foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class User(db.Model, UserMixin):
#schema and table config
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
#capital case because relationship class    
    chats = db.relationship('Chat')



