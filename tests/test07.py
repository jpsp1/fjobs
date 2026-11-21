from dotenv import load_dotenv
# from openai import AsyncOpenAI
    
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, output_guardrail, GuardrailFunctionOutput, ModelSettings
import os
# from pydantic import BaseModel, Field
# from typing import List
import asyncio
# from datetime import datetime
# import pprint
# from pathlib import Path
import subprocess
from agents.mcp import MCPServerStdio
import sys

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

SANDBOX_DIR = os.path.join(os.getcwd(), "sandbox")
WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")
if not os.path.exists(SANDBOX_DIR):
    os.makedirs(SANDBOX_DIR)
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

@function_tool
def run_sandbox_python(filename: str) -> str:
    """
    Execute a Python file from the sandbox directory inside an ephemeral
    Docker container, with the sandbox mounted as the working directory,
    and return whatever the script printed to stdout.

    Args:
        filename: The name of the Python file to run (e.g. "solution.py").
    Returns:
        The text printed to stdout by the executed script.
    """
    result = subprocess.run(
        #scripts are at sandbox/workspace 
        [
            "docker", "run", "--rm",
            #"-v", f"{SANDBOX_DIR}:/workspace",
            "-v", f"{SANDBOX_DIR}/workspace:/workspace",
            "-w", "/workspace",
            "python:3.13-slim",
            "python", filename,
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout

#$ docker run --rm -v "$(pwd)/sandbox/workspace:/workspace" -w /workspace python:3.13-slim python llm_script.py
#3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381

async def main():       
    sandbox_path=SANDBOX_DIR
    files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as server:
        file_tools = await server.list_tools()
    #print(f"Filesystem tools: {file_tools}")
    
    INSTRUCTIONS = """
    You're a python coder. You can use local filesystem tools and can
    write and run python scripts in a sandbox/workspace folder. You can use the run_sandbox_python tool to run a script in the sandbox folder and get its output.
    """

    TASK = f"""
    using your tools write a python script to the sandbox/workspace folder that calculates the pi number to  at least 1000 decimal places and prints it to stdout. The script name should be llm_script.py.
    Don't create the sandbox folder, it already exists. Don't create the workspace folder, it already exists. Don't create any other folders, just write the script to the sandbox/workspace folder.
    Leave the script in the sandbox folder.
    Run the script and return the output.
    """ 
    # without this it just wrote the script but did not run it
    ms=ModelSettings(tool_choice="required")
    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        p_runner = Agent(
            name="p_runner", 
            model="gpt-5.4-mini", 
            instructions=INSTRUCTIONS,
            tools=[run_sandbox_python],
            model_settings=ms,
            mcp_servers=[mcp_server_files])
        with trace("p_runner"):
            result = await Runner.run(p_runner, TASK, max_turns=10)
        print(f"Result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
