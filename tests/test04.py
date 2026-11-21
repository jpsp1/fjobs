# The imports

from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from IPython.display import Image, display
import os
import asyncio

load_dotenv(override=True)

fetch_params = {"command": "uvx", "args": ["--with", "mcp<2","mcp-server-fetch"]}
playwright_params = {"command": "npx", "args": [ "@playwright/mcp@latest"]}
files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}

sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))  # the only folder the filesystem server may touch
os.makedirs(sandbox_path, exist_ok=True)


INSTRUCTIONS = """
You browse the internet to accomplish your instructions.
Accept cookies and navigate pop-ups as needed.
If one website isn't fruitful, try another.
Be persistent until you have solved your assignment,
trying different options and sites as needed.
When you need to write files, you do that inside the sandbox/ folder only.
"""

TASK = "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee.md"



async def main():       
    # async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
    #     fetch_tools = await server.list_tools()
    # print(f"Fetched tools: {fetch_tools}")

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as server:
        file_tools = await server.list_tools()
    print(f"Filesystem tools: {file_tools}")

    async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
        playwright_tools = await server.list_tools()

    print(f"\n\n\nPlaywright tools: {playwright_tools}")


    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator",
                instructions=INSTRUCTIONS,
                model="gpt-5.4-mini",
                mcp_servers=[mcp_server_files, mcp_server_browser]
                )
            with trace("investigate"):
                result = await Runner.run(agent, TASK, max_turns=20)
                print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())







