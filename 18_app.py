from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

import asyncio

class HomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent( 
    name="Guardrail check",
    model="gpt-4o-mini",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=HomeworkOutput,
)

biology_guardrail_agent = Agent( 
    name="Guardrail check",
    model="gpt-4o-mini",
    instructions="Check if the user is asking you to do their biology homework.",
    output_type=HomeworkOutput,
)


@input_guardrail
async def math_guardrail( ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:

    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=result.final_output.is_math_homework,)


agent = Agent(  
    name="Customer support agent",
    model="gpt-4o-mini",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail not detected!")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail detected")


if __name__ == "__main__":
    asyncio.run(main())
