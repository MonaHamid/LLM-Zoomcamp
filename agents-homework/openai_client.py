# openai_client.py
import os
import openai
from dotenv import load_dotenv
load_dotenv()

# Load your API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self):
        self.client = openai

    @property
    def responses(self):
        return self

    def create(self, model, input, tools):
        # tools → functions for the new API
        return openai.chat.completions.create(
            model=model,
            messages=input,
            functions=tools,         # pass your tool list here
            function_call="auto"     # now valid, because we have functions
        )