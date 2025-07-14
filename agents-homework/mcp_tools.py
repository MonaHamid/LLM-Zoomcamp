# mcp_tools.py
import json
from mcp_client import MCPClient

def convert_tools_list(mcp_tools):
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["inputSchema"],
        }
        for tool in mcp_tools
    ]

class MCPTools:
    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client
        self._tools = None

    def get_tools(self):
        if self._tools is None:
            mcp_list = self.mcp.get_tools()       # sends tools/list
            self._tools = convert_tools_list(mcp_list)
        return self._tools

    def function_call(self, entry):
        func = entry.function_call
        name = func.name
        args = json.loads(func.arguments)
        result = self.mcp.call_tool(name, args)  # sends tools/call
        return {
            "type": "function_call_output",
            "call_id": None,
            "output": json.dumps(result, indent=2),
        }
