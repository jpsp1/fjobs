from dotenv import load_dotenv 
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, output_guardrail, GuardrailFunctionOutput, ModelSettings
import os
import asyncio
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

#############################
# user must have permissions to run docker commands without sudo.
# shell test:
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
    # without this it is tempeted to use the default model settings, which will not allow the run_sandbox_python tool to be used.
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


        #         Result: Done — I wrote `workspace/llm_script.py`, ran it, and it printed π to 1000 decimal places.

        # Output:
        # ```text
        # 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989
        # ```


if __name__ == "__main__":
    asyncio.run(main())
