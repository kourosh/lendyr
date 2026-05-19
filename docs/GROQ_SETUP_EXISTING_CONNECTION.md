# Groq Setup - Existing Connection

Since the `groq_credentials` connection already exists, you just need to set the API key.

## Quick Steps

### 1. Get Your Groq API Key
Visit https://console.groq.com/ and get your API key

### 2. Set the API Key
```bash
source ~/.venv/bin/activate
orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=YOUR_GROQ_API_KEY"
```

Replace `YOUR_GROQ_API_KEY` with your actual key.

### 3. Import the Model (if not already done)
```bash
orchestrate models import --file models/groq_gpt_oss_120b.yaml --app-id groq_credentials
```

### 4. Verify Model is Available
```bash
orchestrate models list | grep groq
```

You should see: `virtual-model/groq/openai/gpt-oss-120b`

### 5. Test the Agent
The agent has already been updated. Open `webchat/index.html` in your browser and test it.

## Troubleshooting

### If you still get 401 errors:
1. Verify your API key is correct
2. Check the connection credentials:
   ```bash
   orchestrate connections list
   ```
3. Make sure you're using the draft environment
4. Try removing and recreating the connection:
   ```bash
   orchestrate connections remove -a groq_credentials
   ./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY
   ```

## Alternative: Use a Different Model

If you prefer not to use Groq, edit `agents/account_opening_agent.yaml` and change line 5:

```yaml
llm: openai/gpt-4o  # or anthropic/claude-3-5-sonnet-20241022
```

Then redeploy:
```bash
orchestrate agents import --file agents/account_opening_agent.yaml