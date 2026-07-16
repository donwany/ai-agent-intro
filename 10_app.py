from agents import Agent, Runner, trace, set_tracing_disabled
import asyncio

set_tracing_disabled(False)

async def main():
    joke_agent = Agent(name="Joke generator", instructions="Tell funny jokes about Ghana", model="gpt-4o-mini")

    joke_rater_agent = Agent(name="Joke rater", instructions="You rate funny jokes on a scale of 1 to 10.", model="gpt-4o-mini")

    with trace("Joke workflow"): 
        first_result = await Runner.run(joke_agent, "Tell me 5 different jokes")
        second_result = await Runner.run(joke_rater_agent, f"Rate this joke: {first_result.final_output}")

        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())