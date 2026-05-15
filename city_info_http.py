import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("City Explorer")

@mcp.tool()
async def get_city_info(city_name: str):
    """
    Fetches detailed information about a city including coordinates, 
    country, and timezone.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            return f"No information found for city: {city_name}"
        
        city_data = data["results"][0]
        
        # Formatting the output for the LLM
        return {
            "name": city_data.get("name"),
            "country": city_data.get("country"),
            "admin_area": city_data.get("admin1"),
            "latitude": city_data.get("latitude"),
            "longitude": city_data.get("longitude"),
            "timezone": city_data.get("timezone"),
            "population": city_data.get("population", "Unknown")
        }

if __name__ == "__main__":
    # Run using stdio transport (standard for local MCP)
    mcp.run(transport="stdio")
