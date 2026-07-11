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


async def main() -> None:
    while  True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # You can choose which agent to use based on the user's input or context
        # For demonstration, we'll use the Spanish agent for translation
        result = await Runner.run(history_agent, user_input)
        print(f"Agent: {result.final_output}\n")




if __name__ == "__main__":
    asyncio.run(main())