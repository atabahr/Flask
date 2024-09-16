import json
import os
import requests
from flask import current_app
from langchain_openai import ChatOpenAI

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

def get_llama_response(chat_input, conversation_id):
    # Load the conversation history for the given conversation_id
    history = load_conversation_history()
    conversation_history = history.get(conversation_id, "")
    
    # Append the new user input to the conversation history
    conversation_history += f"<s>[INST]{chat_input}[/INST]\n"
    
    # Ollama API call
    url = "http://localhost:11434/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama2",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chat_input},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_content = response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        response_content = "Sorry, I couldn't process that request."
        
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
    print(f"AI response: {ai_response}")

if __name__ == "__main__":
    handle_new_message()