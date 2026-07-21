from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
    model="gpt-4o-mini"
)

# Create a session instance with a session ID
session = SQLiteSession(session_id="conversation_123", db_path="conversations.db")

async def main():

    # First turn
    result = await Runner.run(
        agent,
        "What city is the Golden Gate Bridge in?",
        session=session
    )
    print(result.final_output)  # "San Francisco"

    # Second turn - agent automatically remembers previous context
    result = await Runner.run(
        agent,
        "What state is it in?",
        session=session
    )
    print(result.final_output)  # "California"

    # Also works with synchronous runner
    result = await Runner.run(
        agent,
        "What's the population?",
        session=session
    )
    print(result.final_output)  # "Approximately 39 million"


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())