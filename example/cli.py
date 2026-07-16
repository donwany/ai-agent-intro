import asyncio
from agents import Agent, run_demo_loop, function_tool


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


async def main() -> None:
    agent = Agent(
        name="Assistant", 
        instructions="You are a helpful assistant.",
        model="gpt-4o-mini",
        tools=[get_stock_price, get_weather, get_forecast]
    )
    await run_demo_loop(agent)


if __name__ == "__main__":
    asyncio.run(main())
