import asyncio
import os
import shutil
import socket
import subprocess
import time
from typing import Any, cast

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

SSE_HOST = os.getenv("SSE_HOST", "127.0.0.1")


SSE_PORT =  8000
os.environ.setdefault("SSE_PORT", str(SSE_PORT))
SSE_URL = f"http://{SSE_HOST}:{SSE_PORT}/sse"


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_weather` tool
    message = "What's the weather in Dallas,TX?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    async with MCPServerSse(name="SSE Python Server",params={"url": SSE_URL,},) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="SSE Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    try:
        print(f"Starting SSE server at {SSE_URL} ...")
        print("SSE server started. Running example...\n\n")
        asyncio.run(main())
    except Exception as e:
        print(f"Error starting SSE server: {e}")
        exit(1)