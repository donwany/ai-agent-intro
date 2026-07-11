import asyncio
from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str):
    """get weather information"""
    return f"Current weather in {city} is Hot!"


@function_tool
def get_forecast():
    """get weather forecast"""
    pass


@function_tool
def get_stock_price(ticker: str) -> str:
    """Return the stock price for a given ticker."""
    return f"The stock price of {ticker} is $100."

# Create the weather agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You are a weather assistant. Use the weather tool whenever the user asks about the weather",
    tools=[get_weather, get_forecast],
    model="gpt-4o-mini",
)

# stock_agent is another agent that can handle stock price questions
stock_agent = Agent(
    name="Stock bot",
    instructions="You are a helpful stock bot.",
    model="gpt-4o-mini",
    tools=[get_stock_price],
)

# Create the triage agent that routes questions to the right bot
orchestrator_agent = Agent(
    name="Triage bot",
    instructions="Route questions to the right bot.",
    model="gpt-4o-mini",
    handoffs=[weather_agent, stock_agent],
)


async def main() -> None:
    while  True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # You can choose which agent to use based on the user's input or context
        # For demonstration, we'll use the history agent
        result = await Runner.run(starting_agent=orchestrator_agent, input=user_input)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())