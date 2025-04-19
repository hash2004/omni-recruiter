from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.linkedin.linkedin import get_linkedin_profile_data


app = FastAPI()


@app.get("/linkedin/{username}", operation_id="get_linkedin_profile")
async def linkedin_profile(username: str):
    """
    Get LinkedIn profile data for a specific username
    """
    profile_data = get_linkedin_profile_data(username)
    return profile_data


#return hello at /hello
@app.get("/hello", operation_id="hello")
async def hello():
    return {"message": "Shrhary!"}

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
