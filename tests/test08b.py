##############################
# this script is not tested
# as test08.py but with a proper tool, courtesy of Gemini
########################################
import asyncio
import os
import resend
from agents import Agent, Runner, function_tool

# Configure API keys from environment variables
resend.api_key = os.environ["RESEND_API_KEY"]

@function_tool
async def send_email(
    to: list[str],
    subject: str,
    html_body: str,
    from_address: str = "onboarding@resend.dev",
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    reply_to: str | None = None,
) -> str:
    """Send an email using the Resend API.

    Args:
        to: A list of recipient email addresses.
        subject: The subject line of the email.
        html_body: The HTML content of the email body.
        from_address: The verified sender email address (defaults to onboarding@resend.dev).
        cc: Optional list of CC recipient email addresses.
        bcc: Optional list of BCC recipient email addresses.
        reply_to: Optional reply-to email address.
    """
    params: resend.Emails.SendParams = {
        "from": from_address,
        "to": to,
        "subject": subject,
        "html": html_body,
    }

    if cc:
        params["cc"] = cc
    if bcc:
        params["bcc"] = bcc
    if reply_to:
        params["reply_to"] = reply_to

    try:
        response = await resend.Emails.send_async(params)
        return f"Email sent successfully. Resend ID: {response.get('id')}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# Attach the tool to an OpenAI Agent
email_agent = Agent(
    name="Email Assistant",
    instructions=(
        "You are a helpful assistant that sends emails on behalf of the user. "
        "Always format the email body in clean HTML before calling send_email."
    ),
    tools=[send_email],
)

async def main():
    result = await Runner.run(
        email_agent,
        "Send a quick welcome email to alex@example.com letting them know their account is active.",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

