from agents import Agent, RunContextWrapper, Runner, function_tool
from httpx import AsyncClient
from typing_extensions import TypedDict

import logfire

logfire.configure()
logfire.instrument_openai_agents()


class Location(TypedDict):
    lat: float
    long: float


@function_tool
async def fetch_weather(ctx: RunContextWrapper[AsyncClient], location: Location) -> str:
    """Fetch the weather for a given location.

    Args:
        ctx: Run context object.
        location: The location to fetch the weather for.
    """
    r = await ctx.context.get('https://httpbin.org/get', params=location)
    return 'sunny' if r.status_code == 200 else 'rainy'


agent = Agent(name='weather agent', model="gpt-4o-mini", tools=[fetch_weather])


async def main():
    async with AsyncClient() as client:
        logfire.instrument_httpx(client)
        result = await Runner.run(agent, 'Get the weather at lat=51 lng=0.2', context=client)
    print(result.final_output)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())