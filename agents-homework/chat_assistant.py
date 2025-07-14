
import json
import os
import openai
from IPython.display import display, HTML
import markdown
from dotenv import load_dotenv
load_dotenv()   # this will read .env and set os.environ

# Load your API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

class Tools:
    def __init__(self):
        self.tools = {}
        self.functions = {}

    def add_tool(self, function, description):
        self.tools[function.__name__] = description
        self.functions[function.__name__] = function

    def get_tools(self):
        # Return the list of function schemas
        return list(self.tools.values())

    def function_call(self, entry):
        # entry.function_call carries the name + arguments
        func = entry.function_call
        name = func.name
        args = json.loads(func.arguments)
        result = self.functions[name](**args)
        # Return a JSON‐encoded result for the LLM
        return json.dumps({"result": result}, indent=2)

def shorten(text, max_length=50):
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

class ChatInterface:
    def input(self):
        return input("You: ").strip()

    def display_response(self, entry):
        # entry.content is a string (new SDK) or a list (old format)
        text = entry.content if isinstance(entry.content, str) else entry.content[0].text
        html = markdown.markdown(text)
        display(HTML(f"<div><b>Assistant:</b><br>{html}</div>"))

    def display_function_call(self, entry):
        func = entry.function_call
        name = func.name
        args = func.arguments
        call_html = f"""
        <details>
          <summary>Function call: <tt>{name}({args})</tt></summary>
          <div><b>Full call metadata:</b>
            <pre>{entry}</pre>
          </div>
        </details>
        """
        display(HTML(call_html))

class ChatAssistant:
    def __init__(self, tools, developer_prompt, chat_interface):
        self.tools = tools
        self.system = {"role": "system", "content": developer_prompt}
        self.chat_interface = chat_interface

    def gpt(self, messages):
        return openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=self.tools.get_tools(),
            function_call="auto"
        )

    def run(self):
        conversation = [self.system]
        while True:
            user_input = self.chat_interface.input()
            if user_input.lower() in ("stop", "exit", "quit"):
                print("Assistant: Chat ended.")
                break

            conversation.append({"role": "user", "content": user_input})

            while True:
                response = self.gpt(conversation)
                # Wrap into a list to unify handling
                entries = [response.choices[0].message]

                has_messages = False
                for entry in entries:
                    conversation.append(entry)

                    if getattr(entry, "function_call", None):
                        # Show the function call and run it
                        self.chat_interface.display_function_call(entry)
                        output = self.tools.function_call(entry)
                        conversation.append({
                        "role": "function",
                        "name": entry.function_call.name,
                        # dump the dict to a string
                        "content": json.dumps(output)
                        })
                    else:
                        # Render the assistant’s reply
                        self.chat_interface.display_response(entry)
                        has_messages = True

                if has_messages:
                    break
