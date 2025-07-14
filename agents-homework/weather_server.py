import random
from fastmcp import FastMCP

# In-memory weather database
known_weather_data = {
    'berlin': 20.0,
    'germany': 21.5,
    'paris': 24.0,
    'tokyo': 28.3
}

# Name your server (shown in startup message)
mcp = FastMCP("WeatherBot ")

@mcp.tool
def get_weather(city: str) -> float:
    """
    Retrieves the temperature for a specified city or region.
    """
    city = city.strip().lower()
    return known_weather_data.get(city, round(random.uniform(-5, 35), 1))

@mcp.tool
def set_weather(city: str, temp: float) -> str:
    """
    Sets the temperature for a specified city or region.
    """
    city = city.strip().lower()
    known_weather_data[city] = temp
    return f"OK, temperature for {city.title()} set to {temp}°C."

if __name__ == "__main__":
    # This will print: Starting MCP server 'WeatherBot ' with transport 'stdin/stdout'
    mcp.run()
