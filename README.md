# Overview

Omni Recruiter is an end‑to‑end AI recruitment assistant driven by custom and open‑source MCPs. It automates the full pre‑screening pipeline:

1. Resume parsing from Google Drive
2. LinkedIn profile, posts & reactions analysis
3. Autonomous AI phone calls for pre‑screening interviews
4. Call transcript summarization
5. Automated GitHub repo creation & email invitations
6. Web browsing via Brave MCP

All MCPs communicate with a central “Illegal Agent” LLM (e.g. GPT‑4O) to orchestrate each step.

## Custom MCPs

1. get_resume_info
    
    What it does:
    
    – Takes a Google Drive folder link, downloads all PDF resumes
    
    – Runs each PDF through Mistral OCR to extract text
    
    – Forwards cleaned Markdown‑formatted text to the Illegal Agent
    
    How it’s done:
    
    – Google Drive API → download files
    
    – Mistral OCR client call (client.ocr.process(...))
    
    – Format result as Markdown
    
    Invocation example:
    
    `{`
    
    `"mcp": "get_resume_info",`
    
    `"args": { "drive_link": "https://..." }`
    
    `}`
    
2. get_linkedin_profile
    
    What it does:
    
    – Fetches a user’s LinkedIn profile via RapidAPI
    
    – Summarizes experience, skills, headline with GPT‑4O
    
    How it’s done:
    
    – RapidAPI “linkedin-data-api” → /get-profile endpoint
    
    – Summarization chain in GPT‑4O
    
    Invocation example:
    
    `{`
    
    `"mcp": "get_linkedin_profile",`
    
    `"args": { "username": "john‑doe" }`
    
    `}`
    
3. get_profile_posts
    
    What it does:
    
    – Retrieves latest LinkedIn posts via RapidAPI
    
    – Summarizes content & engagement metrics
    
    How it’s done:
    
    – RapidAPI → /get-profile-posts?start=0
    
    – Truncate to 5 posts to respect token limits
    
    Invocation example:
    
    `{`
    
    `"mcp": "get_profile_posts",`
    
    `"args": { "username": "john‑doe" }`
    
    `}`
    
4. get_profile_reactions
    
    What it does:
    
    – Gets text of last 5 posts the user reacted to
    
    – Trims metadata, delivers to Illegal Agent
    
    How it’s done:
    
    – RapidAPI → /get-profile-likes
    
    – Slice to 5 items, strip extra fields
    
    Invocation example:
    
    `{`
    
    `"mcp": "get_profile_reactions",`
    
    `"args": { "username": "john‑doe" }`
    
    `}`
    
5. perform_pre_screening_interview
    
    What it does:
    
    – Places an AI‑driven call via Vapi.ai + Twilio
    
    – Asks a configurable question set
    
    – Returns a call_id for later summarization
    
    How it’s done:
    
    – Twilio Voice API + Vapi.ai TTS/ASR integration
    
    Invocation example:
    
    `{`
    
    `"mcp": "perform_pre_screening_interview",`
    
    `"args": { "phone": "+15551234567" }`
    
    `}`
    
6. get_call_summary
    
    What it does:
    
    – Fetches the transcript by call_id
    
    – Summarizes candidate responses with GPT‑4O
    
    How it’s done:
    
    – Twilio transcript API → raw text
    
    – Prompt GPT‑4O for concise summary
    
    Invocation example:
    
    `{`
    
    `"mcp": "get_call_summary",`
    
    `"args": { "call_id": "abc123" }`
    
    `}`
    
7. send_email_to_recipient
    
    What it does:
    
    – Sends an email via SMTP or SendGrid using an app password or API key
    
    How it’s done:
    
    – FastAPI endpoint → SMTP client call
    
    Invocation example:
    
    `{`
    
    `"mcp": "send_email_to_recipient",`
    
    `"args": {`
    
    `"to": "candidate@example.com",`
    
    `"subject": "Next Interview Round",`
    
    `"body": "Hi there, please find details..."`
    
    `}`
    
    `}`
    

# Open Source MCPs

## Brave MCP

Purpose: Allows the Illegal Agent to browse the web and return links, snippets, and sources for up‑to‑date information.

Run command:

`npx -y supergateway`

`--stdio "npx -y @modelcontextprotocol/server-brave-search"`

`--port 8002`

`--baseUrl [http://localhost:8001](http://localhost:8001/)`

`--ssePath /sse`

`--messagePath /message`

`--cors`

## GitHub MCP

Purpose: Enables the Illegal Agent to autonomously create repos, commit changes, open PRs, etc.

Run command:

`GITHUB_PERSONAL_ACCESS_TOKEN="YOUR_TOKEN"`

`npx -y supergateway`

`--stdio "npx -y @modelcontextprotocol/server-github"`

`--port 8003`

`--baseUrl [http://localhost:8003](http://localhost:8003/)`

`--ssePath /sse`

`--messagePath /message`

`--cors`

## RUNNING YOUR CUSTOM MCPS

1. Start the FastAPI MCP server:
    
    uvicorn app:app --reload
    
2. Proxy MCPs for LLM integration:
    
    `npx -y supergateway`
    
    `--stdio "mcp-proxy http://0.0.0.0:8000/mcp"`
    
    `--port 8001`
    
    `--baseUrl [http://localhost:8000](http://localhost:8000/)`
    
    `--ssePath /sse`
    
    `--messagePath /message`
    
    `--cors`