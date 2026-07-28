from deepagents import create_deep_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

if __name__ == "__main__":
    # Run the agent
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )
    print(result["messages"][-1].content_blocks)