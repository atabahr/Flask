from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Chat
from . import db
from .ai import get_llama_response

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        chat = request.form.get('chat', '').strip()  # Default to an empty string if chat is None
        
        if not chat:
            flash('Chat is too short!', category='error')
        else:
            # Assuming you're using the user's ID as the conversation ID
            conversation_id = str(current_user.id)
            response = get_llama_response(chat, conversation_id)
            new_chat = Chat(data=f"You: {chat}\nBot: {response}", user_id=current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            flash('Chat is added!', category='success')
            
    return render_template("home.html", user=current_user)

#API Call : relational format to JSON
@views.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    # Using a hardcoded conversation_id for the API; customize as needed
    conversation_id = "api_conversation"
    response = get_llama_response(question, conversation_id)
    return jsonify({'response': response})