import asyncio
from agents import Agent, Runner
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]
    location: str


calendar_agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text.",
    output_type=CalendarEvent,
    model="gpt-4o-mini"
)


async def main() -> None:
    while  True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # You can choose which agent to use based on the user's input or context
        # For demonstration, we'll use the history agent
        result = await Runner.run(starting_agent=calendar_agent, input=user_input)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())