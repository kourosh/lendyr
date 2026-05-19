# Groq Model Configuration Guide

## Overview
The `groq/openai/gpt-oss-120b` model requires proper configuration in watsonx Orchestrate before it can be used by agents. This guide walks through the complete setup process.

## Problem
When using an agent configured with `llm: groq/openai/gpt-oss-120b`, you may encounter:
```
Error code: 401 - {'error': {'message': 'groq error: Invalid API Key', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}, 'provider': 'groq'}
```

This occurs because the Groq model hasn't been properly configured with API credentials.

## Solution: Configure Groq Model

### Step 1: Get Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (you won't be able to see it again)

### Step 2: Create Model Specification File

Create `models/groq_gpt_oss_120b.yaml`:

```yaml
spec_version: v1
kind: model
name: virtual-model/groq/openai/gpt-oss-120b
display_name: GPT-OSS-120B (Groq)
description: |
  Welcome to the gpt-oss series, OpenAI's open-weight models designed for 
  powerful reasoning, agentic tasks, and versatile developer use cases.
tags:
  - openai
  - gpt-oss-120b
  - groq
model_type: chat
provider_config:
  custom_host: https://api.groq.com/openai/v1
```

### Step 3: Create Connection for API Key

Activate your virtual environment and create a key-value connection:

```bash
# Activate virtual environment
source ~/.venv/bin/activate

# Create connection
orchestrate connections add -a groq_credentials

# Configure connection as key-value type for draft environment
orchestrate connections configure -a groq_credentials --env draft -k key_value -t team

# Set the API key (replace YOUR_GROQ_API_KEY with your actual key)
orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=YOUR_GROQ_API_KEY"
```

### Step 4: Import the Model

Import the model and link it to the connection:

```bash
orchestrate models import --file models/groq_gpt_oss_120b.yaml --app-id groq_credentials
```

### Step 5: Verify Model is Available

List models to confirm it's registered:

```bash
orchestrate models list
```

You should see `virtual-model/groq/openai/gpt-oss-120b` in the list.

### Step 6: Update Agent Configuration

Your agent YAML should reference the model correctly:

```yaml
spec_version: v1
kind: native
name: account_opening_agent_v2
description: Helps customers open new bank accounts
llm: groq/openai/gpt-oss-120b  # or virtual-model/groq/openai/gpt-oss-120b
style: default
# ... rest of configuration
```

### Step 7: Redeploy Agent

```bash
orchestrate agents import --file agents/account_opening_agent_v2.yaml
```

## Alternative: Use Built-in Models

If you prefer not to configure external API keys, consider using built-in models that don't require additional configuration:

### Option 1: OpenAI Models (if configured)
```yaml
llm: openai/gpt-4o
```

### Option 2: Anthropic Models (if configured)
```yaml
llm: anthropic/claude-3-5-sonnet-20241022
```

### Option 3: Mistral Models (if configured)
```yaml
llm: mistral-ai/mistral-large-latest
```

## Troubleshooting

### Error: "Model not found"
- Ensure you've imported the model using `orchestrate models import`
- Verify the model name matches exactly in your agent YAML

### Error: "Invalid API Key"
- Verify your Groq API key is correct
- Check that the connection credentials are set properly
- Ensure you're using the correct environment (draft/live)

### Error: "Connection not found"
- Verify the connection was created: `orchestrate connections list`
- Ensure the app_id matches between model import and connection

## Complete Setup Script

Create `scripts/setup_groq_model.sh`:

```bash
#!/bin/bash

# Setup Groq Model for watsonx Orchestrate
# Usage: ./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY

set -e

if [ -z "$1" ]; then
    echo "Error: Groq API key required"
    echo "Usage: ./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY"
    exit 1
fi

GROQ_API_KEY="$1"

echo "Activating virtual environment..."
source ~/.venv/bin/activate

echo "Creating Groq credentials connection..."
orchestrate connections add -a groq_credentials

echo "Configuring connection..."
orchestrate connections configure -a groq_credentials --env draft -k key_value -t team

echo "Setting API key..."
orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=$GROQ_API_KEY"

echo "Importing Groq model..."
orchestrate models import --file models/groq_gpt_oss_120b.yaml --app-id groq_credentials

echo "Verifying model..."
orchestrate models list | grep groq

echo ""
echo "✅ Groq model configured successfully!"
echo "You can now use 'llm: groq/openai/gpt-oss-120b' in your agents"
```

Make it executable:
```bash
chmod +x scripts/setup_groq_model.sh
```

Run it:
```bash
./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY
```

## References

- [Groq Documentation](https://console.groq.com/docs)
- [watsonx Orchestrate Model Management](https://developer.watson-orchestrate.ibm.com/llm/managing_llm)
- [watsonx Orchestrate Connections](https://developer.watson-orchestrate.ibm.com/connections/build_connections)

## Next Steps

After configuring the Groq model:
1. Test the agent in webchat at `webchat/index.html`
2. Verify the agent responds without API key errors
3. Consider configuring for live environment if needed