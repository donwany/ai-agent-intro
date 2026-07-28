from pydantic_ai import Agent

agent = Agent(  
  'anthropic:claude-sonnet-4-6',
  instructions='Be concise, reply with one sentence.',  
)

if __name__ == "__main__":
  result = agent.run_sync('Where does "hello world" come from?')
  print(result.output)
