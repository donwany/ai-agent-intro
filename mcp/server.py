from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP(name="My Custom MCP Server", host="localhost", port=1957)


@mcp.tool()
def get_customer(email: str):
    """
    Returns customer information.
    """

    customers = {
        "john@gmail.com": {
            "name": "John",
            "balance": 250,
            "country": "USA"
        },
        "alice@gmail.com": {
            "name": "Alice",
            "balance": 600,
            "country": "Canada"
        }
    }

    return customers.get(email, "Customer not found")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b


@mcp.tool()
def calculate_discount(price: float, percentage: float):
    """calculate discount"""
    return round(price * (percentage / 100), 2)


@mcp.tool()
def search_products(keyword: str):
    """search products"""
    return [
        {
            "id": 1,
            "name": "Laptop"
        },
        {
            "id": 2,
            "name": "Keyboard"
        }
    ]

@mcp.tool()
def get_current_weather(city: str) -> str:
    print(f"[debug-server] get_current_weather({city})")
    # Avoid slow or flaky network calls during automated runs.
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}", timeout=2)
        if response.ok:
            return response.text
    except Exception:
        pass
    # Fallback keeps the tool responsive even when offline.
    return f"Weather data unavailable right now; assume clear skies in {city}."


if __name__ == "__main__":
    # Exposes the MCP server over HTTP
    transport = "streamable-http"

    if transport == "stdio":
        print("Server running on stdio")
        mcp.run(transport=transport)
    elif transport == "streamable-http":
        print("Server running on streamable-http")
        mcp.run(transport=transport)
    elif transport == "sse":
        print("Server running on sse")
        mcp.run(transport=transport)
    else:
        print("Running on unknown server")