import os, openai, random, json

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your fake database
known_weather_data = {
    "berlin": 20.0,
    "germany": 21.5,
    "paris": 24.0,
    "tokyo": 28.3
}

# The actual function
def get_weather(city: str) -> float:
    city = city.strip().lower()
    return known_weather_data.get(city, round(random.uniform(-5, 35), 1))

# Tell the model about your tool
functions = [{
    "name": "get_weather",
    "description": "Retrieve the current temperature for a specified city or region.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City or region name"}
        },
        "required": ["city"]
    }
}]

# Strong system prompt to force function use
system_prompt = """
You are a weather assistant with no internal data.
Always use the get_weather function to answer.
Pass the user’s exact input as the city argument.
""".strip()

def ask_weather(user_query: str) -> str:
    # Step A: model decides whether to call function
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user",   "content":user_query}
        ],
        functions=functions,
        function_call="auto"
    )
    msg = resp.choices[0].message

    # if function_call, run it
    if msg.function_call:
        args = json.loads(msg.function_call.arguments)
        temp = get_weather(**args)

        # Step C: feed back the result
        follow = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role":"system", "content":system_prompt},
                {"role":"user",   "content":user_query},
                msg,
                {"role":"function","name":msg.function_call.name,
                 "content":json.dumps({"result":temp})}
            ]
        )
        return follow.choices[0].message.content
    else:
        # if it didn’t pick the tool, just return its text
        return msg.content

if __name__ == "__main__":
    print("Type ‘exit’ to quit.")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit", "stop"):
            print("Assistant: Goodbye!")
            break
        answer = ask_weather(query)
        print("Assistant:", answer)
