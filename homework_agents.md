# Homework: Agents

In this homework, we explore function calling and the Model-Context Protocol (MCP).

---

## Q1. Define function description

We want to use the `get_weather` function as a tool. Fill in missing parts:

```python
get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Retrieve the current temperature for a specified city or region.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city for which to retrieve the weather."
            }
        },
        "required": ["city"],
        "additionalProperties": False
    }
}
```

**Answer (TODO3):**  
`city`

---

## Q2. Adding another tool

Define a `set_weather` tool that adds weather data:

```python
set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "Set the temperature for a specified city or region.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City or region name"
            },
            "temp": {
                "type": "number",
                "description": "Temperature in Celsius to set for that city"
            }
        },
        "required": ["city", "temp"],
        "additionalProperties": False
    }
}
```

**Answer:**  
I wrote the above `set_weather_tool` schema with the description:  
`"Set the temperature for a specified city or region."`

---

## Q3. Install FastMCP

```bash
pip install fastmcp
```

**Answer:**  
Version installed: **2.10.5**

---

## Q4. Simple MCP Server

Run your `weather_server.py`:

```
Starting MCP server 'WeatherBot ' with transport 'stdio'
```

**Answer:**  
Transport: **`stdio`**

---

## Q5. Protocol

Call the `get_weather` tool via JSON-RPC:

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Berlin"}}}
```

**Response:**
```json
{
  "content": [{"type": "text", "text": "20.0"}],
  "structuredContent": {"result": 20.0},
  "isError": false
}
```

---

## Q6. Client

Using the non-async MCP client to list tools:

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("weather_server.py") as mcp_client:
        tools = await mcp_client.list_tools()
        print(tools)

asyncio.run(main())
```

**Result:**
```python
[
  Tool(
    name='get_weather',
    title=None,
    description='Retrieves the temperature for a specified city or region.',
    inputSchema={
      'properties': {'city': {'title': 'City', 'type': 'string'}},
      'required': ['city'],
      'type': 'object'
    },
    outputSchema={
      'properties': {'result': {'title': 'Result', 'type': 'number'}},
      'required': ['result'],
      'title': '_WrappedResult',
      'type': 'object',
      'x-fastmcp-wrap-result': True
    },
    annotations=None,
    meta=None
  ),
  Tool(
    name='set_weather',
    title=None,
    description='Sets the temperature for a specified city or region.',
    inputSchema={
      'properties': {
        'city': {'title': 'City', 'type': 'string'},
        'temp': {'title': 'Temp', 'type': 'number'}
      },
      'required': ['city', 'temp'],
      'type': 'object'
    },
    outputSchema={
      'properties': {'result': {'title': 'Result', 'type': 'string'}},
      'required': ['result'],
      'title': '_WrappedResult',
      'type': 'object',
      'x-fastmcp-wrap-result': True
    },
    annotations=None,
    meta=None
  )
]
```
