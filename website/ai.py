import json
import os
import requests
from flask import current_app
from .tokens import count_tokens

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

# Ensure the conversation history does not exceed 8000 tokens
def trim_conversation_history(conversation_history, limit=8000):
    while count_tokens(conversation_history) > limit:
        # Remove the oldest entry
        conversation_history = conversation_history.split('\n', 1)[-1]
    return conversation_history

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
    
    # Print the number of tokens before user input and AI response
    initial_token_count = count_tokens(conversation_history)
    print(f"Tokens before new input: {initial_token_count}")
    
    # Construct the prompt with previous interactions
    chat_prompt = f"""
    "You are the 'Assistant' to software developers, also known as the 'User', whom you assist with your knowledge. Remembering this conversation history: {conversation_history}, Respond to this prompt from: {chat_input}"]
    """
    conversation_history += f"<s>[INST] User:{chat_input}[/INST]\n"
    
    # Ollama API call
    url = "http://192.168.2.142:11434/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.1:70b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chat_prompt},
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_content = response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        response_content = "Sorry, I couldn't process that request."
    
    # Append the model's response to the conversation history
    conversation_history += f"Assistant: {response_content}\n"
    
    # Print the number of tokens after user input and AI response
    final_token_count = count_tokens(conversation_history)
    print(f"Tokens after new input and response: {final_token_count}")

    # If the token count exceeds the limit, trim the history
    if final_token_count > 8000:
        print(f"Token limit exceeded. Trimming conversation history.")
        conversation_history = trim_conversation_history(conversation_history)

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
    
    # Get AI response
    ai_response = get_llama_response(chat_input, conversation_id)
    print(f"AI response: {ai_response}")

if __name__ == "__main__":
    handle_new_message()
