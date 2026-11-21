import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import openai
from pypdf import PdfReader
from IPython.display import Markdown, display
from tools.push import push, send_email
from agents.mcp import MCPServerStdio
import asyncio
from agents import Agent, Runner, trace, set_tracing_disabled
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta
import pprint
from tools.push import push



MODEL="gpt-5.4-mini"
MODEL_BIG="gpt-5.4"
MODEL_NANO="gpt-5.4-nano"

WDIR=os.path.abspath(os.path.join(os.getcwd(), "workspace"))
SANDBOX_PATH = os.path.join(WDIR, "sandbox")

CV_FILE=os.path.join(WDIR, "cv.pdf")
CV_FILE_MD=os.path.join(WDIR, "cv.md")

load_dotenv(override=True)

##################################################
# get the CV into MD format
#

if not os.path.exists(WDIR):
    os.makedirs(WDIR)
if not os.path.exists(SANDBOX_PATH):
    os.makedirs(SANDBOX_PATH)

if not os.path.exists(CV_FILE):
    print(f"Please put your CV in PDF format at {CV_FILE}")
    sys.exit(1)

reader = PdfReader(CV_FILE)
CV_text = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        CV_text += text
print(f"Extracted {len(CV_text)} characters from CV PDF")

################################
# structured output

class Offer(BaseModel):

    rank: int = Field(description="Number indicating the rank of the offering, with 1 being the highest rank, that is, the offering closest to the user's curriculum")    

    tittle_of_offering: str = Field(description="The title of the offering")

    institution_who_is_offering: str = Field(description="The institution that is offering the job opportunity")

    URL: str = Field(description="URL of the offering")

    pay_of_offering: float = Field(description="optional: The monthly pay of the offering, if available, in euros")

    date_of_offering: float = Field(description="The date of the offering, in  YYYY-MM-DD format, e.g., 2024-06-01")

    jobs_description: float = Field(description="A brief summary of the offering, if available, in a few sentences")

    jobs_description_score: int = Field(description="A score indicating how well the offering matches the user's curriculum, with 100 being the highest score, that is, the offering closest to the user's curriculum, and 0 being the lowest score, that is, the offering furthest from the user's curriculum")

    current_date: float = Field(description="The current date with  YYYY-MM-DD format, e.g., 2024-06-01")

class List_of_offers(BaseModel):
     offers: List[Offer] = Field(description="List of job offerings")

#pprint.pp(List_of_offers.model_json_schema())

async def main():       

    ##################################################
    # tool setting 
    #
    playwright_params = {"command": "npx", "args": [ "@playwright/mcp@latest"]}
    files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", SANDBOX_PATH]}

    pay=2700

    ##################################################
    # summarize old job offers found in previous reports
    #
    print(f"\n\nSearching for old job offers in previous reports in {SANDBOX_PATH}")

    INSTRUCTIONS = """
    You'r a good local file manipulator and text / json parser
    """

    TASK = f"""
    find all files with names starting with "report_on_job_offers_" on the sandbox folder, and produce a text output with one job offer per line, with the following information: tittle_of_offering and URL 
    Don't repeat lines for the same job offer, if they appear in more than one file.
    """ 
    old=None
    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=120) as mcp_server_files:
        agent = Agent(
            name="file_parser",
            instructions=INSTRUCTIONS,
            model=MODEL,
            mcp_servers=[mcp_server_files],            
            )                
        with trace("file_parser"):
            result = await Runner.run(agent, TASK, max_turns=30)                
        old=result.final_output
    print(f"Length of old job offers found in previous reports: {len(old)}")

    minimum_date = datetime.now() - timedelta(days=120)

    ##################################################
    # seek on the first special website 
    #
    INSTRUCTIONS = """
    You browse the internet to accomplish your instructions.
    Translate from Portuguese to English as needed, and vice versa.
    Accept cookies and navigate pop-ups as needed.
    If one website isn't fruitful, try another.
    Be persistent until you have solved your assignment,
    trying different options and sites as needed.
    When you need to write files, you do that inside the sandbox/ folder only.
    Don't create the sandbox folder, it already exists.
    """

    TASK = f"""
    Find 3 job offers in the Lisbon area, using the first website at the job_sites.txt file in the sandbox folder, ignoring the following  offers: "{old}"  as they are reports of previous searches.

        Jobs you seek should be compatible, as much as possible, with the following cv:
    ' {CV_text} '. 

    In the website www.bep.gov.pt fill in Região/Distrito as "Lisboa" and "Data de Publicação Posterior a"  as 2026-01-01. Leave all other fields untouched. Then cick "Pesquisar" and seek information in the following pages

    Jobs you find should be described in the Portuguese language, preferably with monthly salary of at least {pay} euros.
    Exclude any offers related to software engineering, software development or software managment.

    Use the List_of_offers structured output and write to the jobs.json file in the sandbox.
    """ 

    # TASK = f"""
    # make up a list of 5 entries of job offers compatible  with 
    # the requested structured output.
    # don't use any tools.
    # Use the List_of_offers structured output and write to the jobs.json file in the sandbox.
    # """ 

    print(f"\n\nSearching for new job offers in the first special website www.bep.gov.pt")

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator",
                instructions=INSTRUCTIONS,
                model=MODEL_BIG,
                mcp_servers=[mcp_server_files, mcp_server_browser],
                output_type=List_of_offers,
                )
            with trace("investigate"):
                result = await Runner.run(agent, TASK, max_turns=60)
                # print(result)                
                # print(result.final_output.offers)
                # pprint.pp(result.final_output.offers)

    report_date=datetime.now().strftime("%Y%m%d%H%M")
    fn=f"{SANDBOX_PATH}/report_on_job_offers_{report_date}.json"
    with open(f"{fn}", "w", encoding="utf-8") as f:
        f.write(str(result.final_output))
        f.close()
    print(f"Report written to {fn}")


    ##################################################
    # seek on other  websites
    #
    
    TASK = f"""
    Find 3 job offers in the Lisbon area, using the second and third websites at the job_sites.txt file in the sandbox folder, ignoring the following  offers: "{old}"  as they are reports of previous searches.

        Jobs you seek should be compatible, as much as possible, with the following cv:
    ' {CV_text} '. 

    Jobs you find should be described in the Portuguese language, preferably with monthly salary of at least {pay} euros.
    Exclude any offers related to software engineering, software development or software managment.

    Use the List_of_offers structured output and write to the jobs.json file in the sandbox.
    """ 

    print(f"\n\nSearching for new job offers in the second and third websites at the job_sites.txt file in the sandbox folder")

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator2",
                instructions=INSTRUCTIONS,
                model=MODEL,
                mcp_servers=[mcp_server_files, mcp_server_browser],
                output_type=List_of_offers,
                )
            with trace("investigate2"):
                result2 = await Runner.run(agent, TASK, max_turns=60)

    with open(f"{fn}", "a", encoding="utf-8") as f:
        f.write(str(result2.final_output))
        f.close()
    print(f"Report updated to {fn}")

    Email_to=os.getenv("EMAIL_TO")
    Email_from=os.getenv("EMAIL_FROM")

    ##################################################
    # make the report
    #

    INSTRUCTIONS = """
    You produce human readable reports. Clear and concise.
    """

    TASK = f"""
    Produce a human readable report in 2 parts, titled "Job Offers Report", in plain text format, with the following content:
 
    The first part of the report, part one, with tittle new jobs offers, are new offers found in  following structered output:
    ' {result.final_output.offers} ' and
    ' {result2.final_output.offers} ' 
    present all information available, starting with the score, the title, the institution and the URL. Present first the highest score offers, and then the lower score offers.  

    On the second  part of the report, part two, with tittle old jobs offers, present the same information  found in  files  with names starting with "report_on_job_offers_" on the sandbox folder.  
    Consider only files that are at least 2 hours old.
    Sort the offfer by the highest score first, and then the lower score offers.
 
     Include in the report date of the report, {report_date},   in the format YYYY-MM-DD, 
    the file name you wrote to, and the number of job offers found.

    Also write your text report to a file in the sandbox folder in a file with name starting with "human_report_{report_date}.txt".
    
        Don't create the sandbox folder, it already exists.
        Tell the file name of your final output.

    Using the send_email tool, send a  email to {Email_to}
    from {Email_from}
    with the subject "Job Offers Report" and the body of the email being the text report you produced.
    """ 

    print(f"\n\nMaking the report...")

    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=120) as mcp_server_files:
        agent = Agent(
            name="reporter",
            instructions=INSTRUCTIONS,
            model=MODEL,
            mcp_servers=[mcp_server_files],
            tools=[send_email],
            )        
        set_tracing_disabled(True)
        result = await Runner.run(agent, TASK, max_turns=30)                
        fn=f"{SANDBOX_PATH}/human_report_{report_date}.txt"
        with open(f"{fn}", "r", encoding="utf-8") as f:
            file_content = f.read()
            f.close()
        print(f"Report written to {fn}")
        push(f"Job Offers Report\n\n Find a new report at {fn}\n\n Email sent to {Email_to}")

if __name__ == "__main__":
    asyncio.run(main())

