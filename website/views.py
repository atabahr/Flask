from flask import Blueprint, render_template, request, flash 
from flask_login import login_required, current_user
from .models import Chat
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        chat = request.form.get('chat', '')  # Default to an empty string if chat is None
        
        if chat.strip() == '':
            flash('Chat is too short!', category='error')
        else:
            new_chat = Chat(data=chat, user_id=current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            flash('Chat is added!', category='success')
    
    return render_template("home.html", user=current_user)
