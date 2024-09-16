#Updating get_llama_response function, storing conversation as json 
import json

from langchain_openai import ChatOpenAI
from rich import print
from flask import current_app
import jwt

# Load conversation history from JSON
def load_conversation_history():
    try:
        with open('conversation_history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = {}
    return history

# Save conversation history to JSON
def save_conversation_history(history):
    with open('conversation_history.json', 'w') as file:
        json.dump(history, file)

def initialize_llama():
    llama = ChatOpenAI(
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",
        openai_api_key=current_app.config['FIREWORKS_API_KEY'],
        openai_api_base="https://api.fireworks.ai/inference/v1"
    )
    print("Model initialized successfully!")
    return llama

def get_llama_response(chat_input, conversation_id):
    llama = initialize_llama()
    # Load the conversation history for the given conversation_id
    history = load_conversation_history()
    conversation_history = history.get(conversation_id, "")
    # Append the new user input to the conversation history
    conversation_history += f"<s>[INST]{chat_input}[/INST]\n"

    # Generate the response using the entire conversation history
    response = llama.invoke(conversation_history)
    
    response_content = response.content
    
    # Append the model's response to the conversation history
    conversation_history += f"Assistant : {response_content}</s>\n"
    
    # Save the updated conversation history back to the JSON file
    history[conversation_id] = conversation_history
    save_conversation_history(history)
    
    return response_content