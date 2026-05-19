#!/bin/bash

# Setup Groq Model for watsonx Orchestrate
# Usage: ./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY

set -e

if [ -z "$1" ]; then
    echo "Error: Groq API key required"
    echo "Usage: ./scripts/setup_groq_model.sh YOUR_GROQ_API_KEY"
    echo ""
    echo "To get a Groq API key:"
    echo "1. Visit https://console.groq.com/"
    echo "2. Sign up or log in"
    echo "3. Navigate to API Keys section"
    echo "4. Create a new API key"
    exit 1
fi

GROQ_API_KEY="$1"

echo "=========================================="
echo "Setting up Groq Model for watsonx Orchestrate"
echo "=========================================="
echo ""

echo "Step 1: Activating virtual environment..."
source ~/.venv/bin/activate

echo "Step 2: Creating/updating Groq credentials connection..."
orchestrate connections add -a groq_credentials 2>/dev/null || echo "Connection already exists, will update..."

echo "Step 3: Configuring connection as key-value type..."
orchestrate connections configure -a groq_credentials --env draft -k key_value -t team

echo "Step 4: Setting API key..."
orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=$GROQ_API_KEY"

echo "Step 5: Importing/updating Groq model..."
orchestrate models import --file models/groq_gpt_oss_120b.yaml --app-id groq_credentials 2>/dev/null || echo "Model may already exist, continuing..."

echo ""
echo "Step 6: Verifying model registration..."
orchestrate models list | grep groq || echo "Warning: Model not found in list"

echo ""
echo "=========================================="
echo "✅ Groq model configured successfully!"
echo "=========================================="
echo ""
echo "You can now use 'llm: groq/openai/gpt-oss-120b' in your agents"
echo ""
echo "Next steps:"
echo "1. Redeploy your agent: orchestrate agents import --file agents/account_opening_agent.yaml"
echo "2. Test in webchat: open webchat/index.html in your browser"
echo ""

# Made with Bob
