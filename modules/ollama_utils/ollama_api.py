import requests
import json
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from .param import embed_model_name, model_name

class OllamaAPI:
    def __init__(self, host="http://localhost:11434"):
        self.host = host

    def chat(self, model, messages, **kwargs):
        """
        Send chat to Ollama API.
        :param model: model name (ví dụ: "my-custom-model")
        :param messages: message list (every message is a dict with "role" and "content")
        :param kwargs: arguments if needed
        :return: JSON response from API.
        """
        url = f"{self.host}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
        }
        payload.update(kwargs)
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
        
def parse_multiple_json(raw_text):
    """
    Changing raw text of model in the server into json list

    This list will then be changed into a list of words responded by model
    (the model predicts word by word)!
    """
    decoder = json.JSONDecoder()
    pos = 0
    objects = []
    while pos < len(raw_text):
        # Remove blank at current position
        while pos < len(raw_text) and raw_text[pos].isspace():
            pos += 1
        if pos >= len(raw_text):
            break
        try:
            obj, new_pos = decoder.raw_decode(raw_text, pos)
            objects.append(obj)
            pos = new_pos
        except json.JSONDecodeError:
            # If cannot decode, break loop
            break
    return objects

# Load model used for embedding
embed_model = HuggingFaceEmbedding(model_name = embed_model_name)

# Choose llm model
llm_model = Ollama(model = model_name, temperature = 0.75)