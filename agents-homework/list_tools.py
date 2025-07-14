import asyncio
from fastmcp import Client

async def main():
    # Tell the client where to find your MCP server:
    # Since you're running it as a separate script, point to the file:
    async with Client("weather_server.py") as mcp_client:
        # Ask the server to list its tools
        tools = await mcp_client.list_tools()
        # Print out the raw list of tool descriptions
        print(tools)

if __name__ == "__main__":
    # Run the async main() function
    asyncio.run(main())
