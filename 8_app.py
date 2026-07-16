from agents import Agent, Runner, Prompt
from agents.extensions.visualization import draw_graph
from agents import Agent, function_tool
import asyncio

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


@function_tool
def get_stock_price(ticker: str) -> str:
    return f"The stock price of {ticker} is $100."


summarizer_agent = Agent(
    name="Summarizer",
    instructions="Generate a concise summary of the supplied text.",
    model="gpt-4o-mini",
)

classification_agent = Agent(
    name="Classification agent",
    instructions="Classify the sentiment of the following text as positive, negative, or neutral.",
    model="gpt-4o-mini",
)

maintenance_agent = Agent(
    name="Maintenance agent",
    instructions="Assist with maintenance requests and scheduling.",
    handoff_description="If the request is related to leasing, handoff to the Leasing agent.",
    model="gpt-4o-mini",
    tools=[get_weather],
)

leasing_agent = Agent(
    name="Leasing agent",
    instructions="Assist with leasing inquiries and applications.",
    handoff_description="If the request is related to maintenance, handoff to the Maintenance agent.",
    model="gpt-4o-mini",
    tools=[get_weather],
)

finance_agent = Agent(
    name="finance agent",
    instructions="Assist with finance inquiries and applications.",
    handoff_description="If the request is related to maintenance, handoff to the Maintenance agent.",
    model="gpt-4o-mini",
)


orchestrator_agent = Agent(
    name="Orchestrator agent",
    instructions="Route requests to the right agent.",
    handoffs=[maintenance_agent, leasing_agent],
    model="gpt-4o-mini",
    tools=[get_weather, get_stock_price],
)


# supervisor agent style
main_agent = Agent(
    name="Supervisor Agent",
    tools=[
        summarizer_agent.as_tool(
            tool_name="summarize_text",
            tool_description="generate a concise summary of the supplied text",
        ),
        classification_agent.as_tool(
            tool_name="classify_sentiment",
            tool_description="classify the sentiment of the following text as positive,negative or neutral",
        ),
        get_weather,
    ],
    model="gpt-4o-mini",
    handoffs=[finance_agent]
)


async def main() -> None:
    while  True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # You can choose which agent to use based on the user's input or context
        # For demonstration, we'll use the history agent
        result = await Runner.run(starting_agent=main_agent, input=user_input)
        print(f"{result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":

    # visualization
    # draw_graph(main_agent).view()
    draw_graph(main_agent, filename="agent_supervisor_visualization")
    draw_graph(orchestrator_agent, filename="agent_orchestrator_visualization")

    asyncio.run(main())
