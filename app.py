from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.linkedin.linkedin import get_linkedin_profile_data
from src.google_drive.gdrive import get_resume_info_from_gdrive

app = FastAPI()


@app.get("/linkedin/{username}", operation_id="get_linkedin_profile")
async def linkedin_profile(username: str):
    """
    Get LinkedIn profile data for a specific username
    """
    profile_data = get_linkedin_profile_data(username)
    return profile_data


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
