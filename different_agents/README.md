## OpenAI SDK
```python

import asyncio
from agents import Agent, Runner, function_tool


@function_tool
def get_forecast():
    """get weather forecast"""
    pass

history_agent = Agent(
    name="History tutor",
    instructions="You answer history questions clearly and concisely. Do not answer questions that are not related to history.",
    model="gpt-4o",
    tools=[get_forecast]
)

async def main() -> None:
    result = await Runner.run(history_agent, "Who was the first president of the United States?")
    print(result.final_output)

asyncio.run(main())

```

## Pydantic AI
```python
from pydantic_ai import Agent

agent = Agent(  
  'anthropic:claude-sonnet-4-6',
  instructions='Be concise, reply with one sentence.',  
)

result = agent.run_sync('Where does "hello world" come from?')  
print(result.output)
"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""

```

## Langchain
```python
# pip install -qU langchain langchain-ollama
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)

```

## DeepAgents
```python
from deepagents import create_deep_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
print(result["messages"][-1].content_blocks)
```

## CrewAI
```python
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[SerperDevTool()],
    verbose=True
)

async def main():
    result = await researcher.kickoff_async("What are the latest developments in AI?")
    print(result.raw)

asyncio.run(main())

```

## Google ADK
```python
from google.adk.agents.llm_agent import Agent

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)

# run this from the terminal
adk run my_agent
```