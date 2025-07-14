import os, openai, random, json
openai.api_key = os.getenv("OPENAI_API_KEY")

known_weather_data = {"berlin":20.0,"germany":21.5,"paris":24.0,"tokyo":28.3}

def get_weather(city: str)->float:
    city=city.strip().lower()
    return known_weather_data.get(city, round(random.uniform(-5,35),1))

def set_weather(city: str, temp: float)->str:
    city=city.strip().lower()
    known_weather_data[city]=temp
    return f"OK, temperature for {city.title()} set to {temp}°C."

functions=[
  {
    "name":"get_weather",
    "description":"Retrieve the current temperature.",
    "parameters": {
      "type":"object","properties":{"city":{"type":"string"}},
      "required":["city"]
    }
  },
  {
    "name":"set_weather",
    "description":"Set the temperature for a city.",
    "parameters":{
      "type":"object","properties":{
        "city":{"type":"string"},"temp":{"type":"number"}
      },
      "required":["city","temp"]
    }
  }
]

system_prompt = """
You are a weather assistant with no memory beyond get_weather and set_weather.
Always call the appropriate function for any weather query or update.
""".strip()

def handle_query(q:str)->str:
    resp = openai.chat.completions.create(
      model="gpt-4o",
      messages=[{"role":"system","content":system_prompt},
                {"role":"user","content":q}],
      functions=functions,
      function_call="auto"
    )
    msg = resp.choices[0].message

    if msg.function_call:
        name=msg.function_call.name
        args=json.loads(msg.function_call.arguments)
        result = get_weather(**args) if name=="get_weather" \
                 else set_weather(**args)
        follow = openai.chat.completions.create(
          model="gpt-4o",
          messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":q},
            msg,
            {"role":"function","name":name,"content":json.dumps({"result":result})}
          ]
        )
        return follow.choices[0].message.content
    return msg.content

if __name__=="__main__":
    print("Type exit to quit.")
    while True:
        u=input("You: ")
        if u.lower() in ("exit","quit"): break
        print("Assistant:", handle_query(u))
