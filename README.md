# omni-recruiter

# Custom MCPs
 npx -y supergateway --stdio "mcp-proxy http://0.0.0.0:8000/mcp" --port 8001 --baseUrl http://localhost:8000 --ssePath /sse --messagePath /message --cors

 uvicorn app:app --reload

 # Taviliy MCP
  npx -y supergateway --stdio "npx -y tavily-mcp@0.1.4" --port 8002 --baseUrl http://localhost:8001 --ssePath /sse --messagePath /message --cors