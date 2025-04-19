from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.linkedin.linkedin import get_linkedin_profile_data, get_profile_posts, get_profile_reactions
from src.google_drive.gdrive import get_resume_info_from_gdrive
from src.email.email import send_email
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import requests
import time
import asyncio
import logging
from src.ai_caller.prompt import system_prompt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/resume/gdrive", operation_id="get_resume_info")
async def resume_info(folder_url: str, output_dir: str = "output"):
    """
    Get resume information from a Google Drive folder
    """
    resume_data = get_resume_info_from_gdrive(
        folder_url=folder_url,
        output_dir=output_dir,
        api_key="edytn5mDI26B5eaqqM83ildOZDvVvTEG"
    )
    return resume_data

@app.get("/linkedin/{username}", operation_id="get_linkedin_profile")
async def linkedin_profile(username: str):
    """
    Get LinkedIn profile data for a specific username
    """
    profile_data = get_linkedin_profile_data(username)
    return profile_data

@app.get("/linkedin/{username}/posts", operation_id="get_profile_posts")
async def linkedin_profile_posts(username: str):
    """
    Get LinkedIn profile posts for a specific username.
    """
    posts_data = get_profile_posts(username)
    return posts_data

@app.get("/linkedin/{username}/reactions", operation_id="get_profile_reactions")
async def linkedin_profile_reactions(username: str, start: int = 0):
    """
    Get LinkedIn profile reactions for a specific username, starting from a given offset.
    """
    reactions_data = get_profile_reactions(username, start)
    return reactions_data

@app.post("/email/send", operation_id="send_email_to_recipient")
async def send_email_endpoint(
    to_email: str, 
    body: str, 
    subject: str 
):
    """
    Send an email to the specified recipient
    
    Args:
        to_email: Recipient's email address
        body: The content of the email
        subject: Subject line for the email (optional)
    """
    try:
        send_email(
            to_email=to_email,
            body=body,
            subject=subject
        )
        return {"status": "success", "message": f"Email sent to {to_email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Define request body schema
class CallRequest(BaseModel):
    customer_number: str

# Fetch sensitive data from environment variables
#AUTH_TOKEN = os.getenv('VAPI_AUTH_TOKEN')
#PHONE_NUMBER_ID = os.getenv('VAPI_PHONE_NUMBER_ID')
PHONE_NUMBER_ID="7a62a1c7-e4b5-41ff-934b-4befd5cc3b95"
AUTH_TOKEN="4be43c29-d225-4054-b430-764fe1718bdd"

if not AUTH_TOKEN or not PHONE_NUMBER_ID:
    raise RuntimeError('VAPI_AUTH_TOKEN and VAPI_PHONE_NUMBER_ID must be set in the environment.')

@app.post('/prescreening/interview', operation_id="perform_pre_screening_interview")
async def complete_interview(request: CallRequest):
    """
    Initiates a call for a pre-screening interview and returns the call ID.
    Check the call summary separately using the /call-summary endpoint.
    """
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    logger.info(f"Initiating call to {request.customer_number}")
    
    # In your complete_interview function, modify the data dictionary:
    data = {
        'assistant': {
            "firstMessage": "Hello, this is Omni Recruiter AI, a recruitment assistant. This is a pre-screening interview call. Are you ready to begin?",
            "provider": "openai",  # Move these properties inside assistant
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": f"{system_prompt}"
                }
            ]
        },  
        'phoneNumberId': PHONE_NUMBER_ID,
        'customer': {
            'number': request.customer_number,
        },
    }
    
    # Start the call
    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data)
    
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    call_data = response.json()
    call_id = call_data.get('id')
    logger.info(f"Call initiated with ID: {call_id}")
    
    # Return immediately with instructions to check summary separately
    return {
        "call_id": call_id, 
        "status": "initiated",
        "message": "Call initiated. Check summary separately once the call completes.",
        "check_summary_with": f"GET /call-summary/{call_id}"
    }

@app.get("/call-summary/{call_id}", operation_id="get_call_summary")
async def get_call_summary(call_id: str):
    """
    Retrieve the summary for a completed call
    """
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    # Get call status
    status_response = requests.get(
        f'https://api.vapi.ai/call/{call_id}', headers=headers)
    
    if status_response.status_code != 200:
        logger.error(f"Error checking call status: {status_response.text}")
        raise HTTPException(status_code=status_response.status_code, detail=status_response.text)
    
    status_data = status_response.json()
    call_status = status_data.get('status')
    
    # Determine analysis status
    analysis_status = "not_started"
    if 'analysis' in status_data:
        if status_data['analysis'].get('status') == 'pending':
            analysis_status = "pending"
        elif status_data['analysis'].get('status') == 'completed':
            analysis_status = "completed"
        elif 'summary' in status_data['analysis'] and status_data['analysis']['summary']:
            analysis_status = "completed"
        else:
            analysis_status = "pending"
    
    # Return summary if available, otherwise status
    if analysis_status == "completed" and 'summary' in status_data['analysis'] and status_data['analysis']['summary']:
        return {
            "call_id": call_id,
            "status": call_status,
            "analysis_status": analysis_status,
            "summary": status_data['analysis']['summary']
        }
    else:
        return {
            "call_id": call_id,
            "status": call_status,
            "analysis_status": analysis_status,
            "message": "Summary not yet available"
        }
        
mcp = FastApiMCP(
    app,  
    name="Omni Recruiter",  
    description="MCP server the Omni Recruiter",  
    base_url="http://localhost:8000"  
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
