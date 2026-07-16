from agents import Agent, Runner, WebSearchTool
import requests


# research certain
# generate a very engaging script

prompt = input("Enter the topic you want to create a video on >: ")

# research agent
research_agent = Agent(
    name="ResearchAgent",
    model="gpt-4o-mini",
    instructions="You are a professional researcher who can research about a topic. You have access to websearch tool that you" \
    "can use to conduct your research",
    tools=[WebSearchTool()]
)

# writer agent 
writer_agent = Agent(
    name="WriteAgent",
    model="gpt-4o-mini",
    instructions="You are a awesome content creator who can create a script for reels using the research provided " \
    "by the research agent. \
    The format of the script should be as follows: [Hook] [Title] [Description] [Hashtags] [Call to Action]",
)

async def main():
    
    result = await Runner.run(research_agent, prompt)
    
    writer_agent_result = await Runner.run(writer_agent, result.final_output)
    print(writer_agent_result.final_output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
