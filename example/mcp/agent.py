from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import asyncio

# mcp server
server = MCPServerStdio(
    params={
        "command": "uv run",
        "args": ["server.py"]
    }
)

# customer agent
agent = Agent(
    name="Customer Assistant",
    instructions="""
    You help customers by using available MCP tools.
    """,
    mcp_servers=[server],
    model="gpt-4o-mini"
)


# "What is the balance for john@gmail.com?"

async def main() -> None:
    while  True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # You can choose which agent to use based on the user's input or context
        # For demonstration, we'll use the history agent
        result = await Runner.run(starting_agent=agent, input=user_input)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())


