from agents import Agent, Runner
import logfire

logfire.configure()
logfire.instrument_openai_agents()

agent = Agent(name='Assistant', model="gpt-4o-mini", instructions='You are a helpful assistant')

result = Runner.run_sync(agent, 'who was the first president of ghana and what killed him?')
print(result.final_output)