import json
import os
import requests
from dotenv import load_dotenv
from fireworks.client import Fireworks

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("FIREWORKS_API_KEY")

# Define the path to the JSON file
json_file_path = 'latest_message.json'

# Load the new message from the JSON file
try:
    with open(json_file_path, 'r') as file:
        new_message = json.load(file)
except FileNotFoundError:
    print(f"File not found: {json_file_path}")
    exit(1)  # Exit if the file is not found

# Extract conversation ID and other necessary information
conversation_id = new_message.get("conversationId")
if not conversation_id:
    print("No conversation ID found in the message")
    exit(1)

print("New message content:", new_message.get("content", "No content"))
print(api_key)

# Generate AI response using the Fireworks API
client = Fireworks(api_key=api_key)

response = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    messages=[{
        "role": "user",
        "content": new_message.get("content", ""),  # Use the content from the latest message
    }],
)
chatgpt_response = response.choices[0].message.content
print("AI Response:", chatgpt_response)

# Prepare the payload for the POST request
payload = {
    "sender": "chatgpt",
    "content": chatgpt_response,
    "timestamp": "test"  # Keep the timestamp as "test"
}

# Make a POST request to your Node.js backend to save the AI response
post_url = f"http://localhost:8000/message/{conversation_id}"
try:
    post_response = requests.post(post_url, json=payload)
    post_response.raise_for_status()  # Raises an HTTPError if the request fails
    print("AI response successfully saved to the conversation:", post_response.json())
except requests.exceptions.RequestException as e:
    print(f"Failed to save AI response: {e}")