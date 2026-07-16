from agents import Agent, Runner, WebSearchTool, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Assistant",
    tools=[WebSearchTool()],
    model="gpt-4o-mini"
)


async def main():
    result = await Runner.run(
        agent,
        "Which coffee shop should I go to around Dallas, TX area?",
    )
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
