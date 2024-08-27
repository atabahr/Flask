from langchain_openai import ChatOpenAI
from rich import print
from flask import current_app

def initialize_llama():
    llama = ChatOpenAI(
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",
        openai_api_key=current_app.config['FIREWORKS_API_KEY'],
        openai_api_base="https://api.fireworks.ai/inference/v1"
    )
    print("Model initialized successfully!")
    return llama

def get_llama_response(chat_input):
    llama = initialize_llama()
    response = llama.invoke(chat_input)
    return response.content