import os
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv(override=True)

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="""
    Send an email to .......@gmail.com with subject 'Hello' and body 'Sent via Resend MCP'.  From address is ..........@resend.dev    
    """,
    tools=[
        {
            "type": "mcp",
            "server_label": "resend",
            "server_url": "https://mcp.resend.com/mcp",
            "headers": {
                "Authorization": f"Bearer {os.environ['RESEND_API_KEY']}"
            },
            "require_approval": "never",
        }
    ],
)

print(response.output_text)

# got email:


# ---------- Forwarded message ---------
# From: <j........@resend.dev>
# Date: Sat, Nov 21, 2026 at 12:24 PM
# Subject: Hello
# To: <.........@gmail.com>


# Sent via Resend MCP