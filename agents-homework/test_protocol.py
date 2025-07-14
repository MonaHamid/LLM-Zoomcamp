from mcp_client import MCPClient
import json

# 1) Start your MCP server
client = MCPClient(["python", "weather_server.py"])
client.start_server()

# 2) Do the JSON-RPC handshake
init_res = client.initialize()        # sends “initialize”
client.initialized()                  # sends “notifications/initialized”

# 3) List available tools
tools = client.get_tools()            # sends “tools/list”
# (you’ll see ['get_weather', 'set_weather'] printed)

# 4) Call get_weather on Berlin
result = client.call_tool("get_weather", {"city": "Berlin"})
print("get_weather →", result)
