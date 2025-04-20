# omni-recruiter

# Custom MCPs
 npx -y supergateway --stdio "mcp-proxy http://0.0.0.0:8000/mcp" --port 8001 --baseUrl http://localhost:8000 --ssePath /sse --messagePath /message --cors

 uvicorn app:app --reload

 # Brave MCP
npx -y supergateway --stdio "npx -y @modelcontextprotocol/server-brave-search" --port 8002 --baseUrl http://localhost:8001 --ssePath /sse --messagePath /message --cors

# Google Calendar API 
npx -y supergateway --stdio "npx -y @modelcontextprotocol/server-brave-search" --port 8003 --baseUrl http://localhost:8002 --ssePath /sse --messagePath /message --cors


 {
   "mcpServers": {
     "google-calendar": {
       "command": "npx",
       "args": ["-y", "google-calendar-mcp"],
       "env": {
         "GOOGLE_CLIENT_ID": "617327125899-ljlak9n7atpi66kbd4g73vsaua4dsf3s.apps.googleusercontent.com",
         "GOOGLE_CLIENT_SECRET": "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",
         "GOOGLE_REDIRECT_URI": "http://localhost:3000/auth/callback"
       },
       "description": "Google Calendar MCP server using npx"
     }
   }
 }