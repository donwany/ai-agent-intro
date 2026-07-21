from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Customer MCP", host="localhost", port=1957)


@mcp.tool()
def get_customer(email: str):
    """_summary_

    Args:
        email (str): _description_

    Returns:
        _type_: _description_
    """
    customers = {
        "john@gmail.com": {
            "name": "John",
            "balance": 500,
            "country": "USA",
        }
    }

    return customers.get(email, {"error": "Customer not found"})


@mcp.tool()
def calculate_discount(price: float, percent: float):
    """_summary_

    Args:
        price (float): _description_
        percent (float): _description_

    Returns:
        _type_: _description_
    """
    return round(price * percent / 100, 2)


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