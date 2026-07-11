import asyncio
from agents import Agent, Runner

# Create the agents
history_tutor = Agent(
    name="History tutor",
    handoff_description="Specialist for history questions.",
    instructions="Answer history questions clearly and concisely.",
    model="gpt-4o-mini"
)

# Create a second agent to handle math questions
math_tutor = Agent(
    name="Math tutor",
    handoff_description="Specialist for math questions.",
    instructions="Explain math step by step and include worked examples.",
    model="gpt-4o-mini"
)

# Create the triage agent that routes questions to the right tutor
orchestrator_agent = Agent(
    name="Homework triage",
    instructions="Route each homework question to the right specialist.",
    handoffs=[history_tutor, math_tutor],
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
        result = await Runner.run(starting_agent=orchestrator_agent, input=user_input)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())