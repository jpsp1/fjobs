from dotenv import load_dotenv
import os
from openai import OpenAI
import openai

MODEL="gpt-5.4-nano"

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
# And now - the all important import statement
# If you get an import error - head over to Q5 and Q25 in the FAQ at https://edwarddonner.com/avatar
# Even for other LLM providers like Gemini, you still use this OpenAI import - see Guide 9 for why



messages = [{"role": "user", "content": "Tell me a fun fact"}]

response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)



