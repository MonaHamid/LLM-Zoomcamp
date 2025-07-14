# chat_with_mcp.py
from chat_assistant import ChatAssistant, ChatInterface, Tools
import os, openai, sys
from mcp_client import MCPClient
from mcp_tools  import MCPTools

# 1. Start MCP server
mcp = MCPClient([sys.executable, "-u", "weather_server.py"])
mcp.start_server()
mcp.initialize()
mcp.initialized()

# 2. Wrap tools
tools = MCPTools(mcp)

# 3. System prompt
developer_prompt = """
You help users find out the weather in their cities.
If they don't specify a city, ask for one.
Always use the provided tools; never guess.
""".strip()

# 4. Instantiate and run
chat = ChatAssistant(tools, developer_prompt, ChatInterface())
chat.run()
