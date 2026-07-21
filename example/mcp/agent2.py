import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp


async def main():
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": "http://localhost:1957/mcp",
        }
    ) as mcp_server:

        agent = Agent(
            name="Customer Assistant",
            instructions="Use the MCP tools to answer customer questions.",
            mcp_servers=[mcp_server],
            model="gpt-4o-mini"
        )

        result = await Runner.run(
            agent,
            "What is the balance for john@gmail.com?",
        )

        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())