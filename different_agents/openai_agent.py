import asyncio
from agents import Agent, Runner, function_tool


@function_tool
def get_forecast():
    """get weather forecast"""
    pass

history_agent = Agent(
    name="History tutor",
    instructions="You answer history questions clearly and concisely. Do not answer questions that are not related to history.",
    model="gpt-4o",
    tools=[get_forecast]
)

async def main() -> None:
    result = await Runner.run(history_agent, "Who was the first president of the United States?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())