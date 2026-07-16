import asyncio
from agents import Agent, run_demo_loop

async def main() -> None:

    general_agent = Agent(name="Assistant", instructions="You are a helpful assistant.")
    
    await run_demo_loop(general_agent, stream=True)

if __name__ == "__main__":
    asyncio.run(main())