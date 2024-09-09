#Updating get_llama_response function, storing conversation as json 
import json
import os
import requests
from flask import current_app
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from fireworks.client import Fireworks

# Load environment variables from .env file
load_dotenv()

# Initialize API key from environment variables
api_key = os.getenv("FIREWORKS_API_KEY")

# Define the paths to the JSON files
conversation_history_path = 'conversation_history.json'
latest_message_path = 'latest_message.json'

# Load conversation history from JSON
def load_conversation_history():
    try:
        with open(conversation_history_path, 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = {}
    return history

# Save conversation history to JSON
def save_conversation_history(history):
    with open(conversation_history_path, 'w') as file:
        json.dump(history, file)

# Load the new message from the JSON file
def load_latest_message():
    try:
        with open(latest_message_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {latest_message_path}")
        return None

def initialize_llama():
    llama = ChatOpenAI(
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",
        openai_api_key=api_key,
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
    conversation_history += f"Assistant: {response_content}</s>\n"
    
    # Save the updated conversation history back to the JSON file
    history[conversation_id] = conversation_history
    save_conversation_history(history)
    
    return response_content

def handle_new_message():
    new_message = load_latest_message()
    if not new_message:
        return
    
    conversation_id = new_message.get("conversationId")
    if not conversation_id:
        print("No conversation ID found in the message")
        return
    
    chat_input = new_message.get("content", "")
    print("New message content:", chat_input)
    
    # Get AI response
    ai_response = get_llama_response(chat_input, conversation_id)
    

if __name__ == "__main__":
    handle_new_message()