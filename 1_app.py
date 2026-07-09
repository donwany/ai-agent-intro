import asyncio
from agents import Agent, Runner

history_agent = Agent(
    name="History tutor",
    instructions="You answer history questions clearly and concisely. Do not answer questions that are not related to history.",
    model="gpt-4o",
)

math_agent = Agent(
    name="Math tutor",
    instructions="You answer math questions clearly and concisely.",
    model="gpt-4o",
)

spanish_agent = Agent(
    name="Spanish tutor",
    instructions="You are an expert in the Spanish language. Translate all English text to Spanish.",
    model="gpt-4o",
)


async def main() -> None:
    result = await Runner.run(spanish_agent, "My name is John. How are you?")
    print(result.final_output)

    #result = await Runner.run(math_agent, "What is the derivative of x^2?")
    # print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())