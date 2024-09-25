from transformers import LlamaTokenizer
import json

# Load a tokenizer that is compatible with LLaMA models
tokenizer = LlamaTokenizer.from_pretrained("huggyllama/llama-30b")

conversation_history_path = '../conversation_history.json'

def load_conversation():
    try:
        with open(conversation_history_path, 'r') as file:
            
            history = json.load(file)
            
            text = str(history)
            token_count = count_tokens(text)
            print(f"Number of tokens: {token_count}")
    except FileNotFoundError:
        history = {}
    return history


# Function to count tokens
def count_tokens(text):
    tokens = tokenizer.encode(text)
    return len(tokens)


if __name__ == "__main__":
    load_conversation()