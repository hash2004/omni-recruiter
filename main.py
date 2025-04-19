from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
# import uvicorn # No longer need uvicorn here if only running via supergateway --stdio
# from starlette.sse import EventSourceResponse   
import asyncio

# Your existing FastAPI application
app = FastAPI()

# Define some basic API endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/items")
async def read_items():
    return {"items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/items")
async def create_item(item: dict):
    return {"item": item, "message": "Item created successfully"}

# Keep your stream endpoint
@app.get("/stream")
async def stream_endpoint():
    async def event_generator():
        for i in range(5):
            # Yield in the format MCP expects for streaming/SSE via stdio if necessary
            # This might need adjustment depending on how FastApiMCP handles SSE over stdio.
            # For simple JSON it works automatically, SSE might need specific handling
            # within FastApiMCP or you might need to structure the output differently.
            # Let's assume for now simple data works.
            # yield f"data: Stream message {i}\n\n" # This is HTTP SSE format
            yield {"event": "message", "data": f"Stream message {i}"} # More likely MCP format? Check FastApiMCP docs.
            await asyncio.sleep(0.5) # Add a small delay
    # FastApiMCP likely handles the wrapping, you might just return the generator
    # return EventSourceResponse(event_generator()) # Probably NOT needed with FastApiMCP/stdio
    return event_generator() # Return the generator directly? Or FastApiMCP might have a specific way.
                            # Let's stick to the original endpoints working first.


# Add the MCP server to your FastAPI app
mcp = FastApiMCP(
    app,
    name="My API MCP",  # Name for your MCP server
    description="MCP server for my API",  # Description
    # base_url="http://localhost:8081", # Base URL is less relevant for stdio communication itself
                                        # It's more for how supergateway presents it externally
    describe_all_responses=True,
    describe_full_response_schema=True
)

# Mount the MCP server to your FastAPI app
mcp.mount()

# Run the app (REMOVE or COMMENT OUT this block when using supergateway --stdio)
# if __name__ == "__main__":
#     # This block causes the conflict when run via supergateway --stdio
#     # Keep it only if you want to run the app standalone for testing WITHOUT supergateway
#     import uvicorn
#     print("Starting Uvicorn directly (NOT recommended when using supergateway --stdio)")
#     uvicorn.run(app, host="0.0.0.0", port=8081)

# --- End of main.py ---

# Important: If you *do* want to run main.py standalone sometimes for testing,
# you can keep the if __name__ == "__main__": block, but just be aware you
# cannot run it standalone *and* run supergateway pointing to it on the same port
# at the same time. When using supergateway --stdio, that block should ideally not run
# or not attempt to bind the port.

# For using with supergateway --stdio, the file should effectively end after mcp.mount()