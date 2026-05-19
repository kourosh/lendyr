# Quick Fix: Groq API Key Error

## The Problem
You're seeing this error when testing the account opening agent:
```
Error code: 401 - {'error': {'message': 'groq error: Invalid API Key', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}, 'provider': 'groq'}
```

## The Solution (3 Steps)

### 1. Get Your Groq API Key
- Visit: https://console.groq.com/
- Sign up/login → API Keys → Create new key
- Copy the key (save it somewhere safe)

### 2. Run the Setup Script
```bash
./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY
```

Replace `YOUR_GROQ_API_KEY` with the actual key you copied.

### 3. Redeploy the Agent
```bash
source ~/.venv/bin/activate
orchestrate agents import --file agents/account_opening_agent.yaml
```

## Test It
Open `webchat/index.html` in your browser and try the agent again.

## Alternative: Use a Different Model

If you don't want to configure Groq, you can switch to a different model:

### Option 1: Update Agent to Use OpenAI (if configured)
Edit `agents/account_opening_agent.yaml`:
```yaml
llm: openai/gpt-4o  # Change this line
```

### Option 2: Update Agent to Use Anthropic (if configured)
```yaml
llm: anthropic/claude-3-5-sonnet-20241022  # Change this line
```

Then redeploy:
```bash
orchestrate agents import --file agents/account_opening_agent.yaml
```

## Need More Details?
See the complete guide: `docs/GROQ_MODEL_CONFIGURATION.md`