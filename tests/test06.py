from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, output_guardrail, GuardrailFunctionOutput
import os
from pydantic import BaseModel, Field
from typing import List
import asyncio
from datetime import datetime
import pprint

now=datetime.today().strftime('%Y-%m-%d %H:%M')

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')

class Offering(BaseModel):
    rank: int = Field(description="Number indicating the rank of the offering, with 1 being the highest rank, that is, the offering closest to the user's curriculum")    
    URL: str = Field(description="URL of the offering")
    institution_who_is_offering: str = Field(description="The institution that is offering the job opportunity")
    tittle_of_offering: str = Field(description="The title of the offering, e.g., 'Software Engineer', 'Data Scientist', etc.")
    pay_of_offering: float = Field(description="optional: The monthly pay of the offering, if available, in euros")
    date_of_offering: float = Field(description="optional: The date of the offering, if available, in ISO 8601 format (YYYY-MM-DD)")
    summary_of_offering: float = Field(description="optional: A brief summary of the offering, if available, in a few sentences")
    current_date: float = Field(description="The current date, in ISO 8601 format (YYYY-MM-DD)")

class List_of_offerings(BaseModel):
     offerings: List[Offering] = Field(description="List of job offerings")

pprint.pp(List_of_offerings.model_json_schema())

INSTRUCTIONS = f"""
You are a job seeker who is looking for job opportunities that match a given curriculum. You will be given a list of job offerings, and you will need to rank them based on how well they match a given curriculum. You will also need to provide a brief summary of each offering, including the title, institution, pay, date, and URL. You will also need to provide the current date that is {now}.
"""
TASK="""
make up an output list of job offerings, with at least 3 offerings 
"""

async def main():       
    job_seeker = Agent(name="Job Seeker", instructions=INSTRUCTIONS, model="gpt-5.4-mini", output_type=List_of_offerings)
    with trace("job_seeker"):
        result = await Runner.run(job_seeker, TASK, max_turns=20)
    lst=result.final_output.offerings
    for i in lst:
        print(i.rank)
        print(i.URL)
        print(i.institution_who_is_offering)
        print(i.tittle_of_offering)
        print(i.pay_of_offering)
        print(i.date_of_offering)
        print(i.summary_of_offering)
        print(i.current_date)


if __name__ == "__main__":
    asyncio.run(main())

