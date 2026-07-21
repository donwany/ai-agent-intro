from mcp.server.fastmcp import FastMCP
import sqlite3


mcp = FastMCP("My Custom MCP Server")


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
def calculate_discount(price: float, percentage: float):

    return round(price * (percentage / 100), 2)


@mcp.tool()
def search_products(keyword: str):

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
def get_weather(city: str):

    return {
        "city": city,
        "temperature": 32,
        "condition": "Sunny"
    }


if __name__ == "__main__":
    # Exposes the MCP server over HTTP
    transport = "stdio"

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