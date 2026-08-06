from pydantic_ai import Agent

agent = Agent('openai:gpt-4o-mini', instructions='You are a helpful assistant.')

@agent.tool_plain
def get_weather(city: str) -> str:
    return f'The weather in {city} is sunny'


app = agent.to_web(models=['openai:gpt-4o-mini', 'openai:gpt-5'])