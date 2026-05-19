#!/bin/bash

# Deploy Account Opening Agent and Tool
# This script deploys the account opening functionality to Orchestrate

set -e

echo "=========================================="
echo "Deploying Account Opening Solution"
echo "=========================================="
echo ""

# Check if orchestrate CLI is available
if ! command -v orchestrate &> /dev/null; then
    echo "❌ Error: orchestrate CLI not found"
    echo "Please install the Orchestrate CLI first"
    exit 1
fi

echo "✓ Orchestrate CLI found"
echo ""

# Deploy the tool
echo "📦 Deploying open_account tool..."
orchestrate tools import \
  -k python \
  -f tools/open_account/open_account.py

if [ $? -eq 0 ]; then
    echo "✓ Tool deployed successfully"
else
    echo "❌ Tool deployment failed"
    exit 1
fi
echo ""

# Deploy the agent
echo "🤖 Deploying account_opening_agent_v2..."
orchestrate agents import \
  -f agents/account_opening_agent_v2.yaml

if [ $? -eq 0 ]; then
    echo "✓ Agent deployed successfully"
else
    echo "❌ Agent deployment failed"
    exit 1
fi
echo ""

# Verify deployment
echo "🔍 Verifying deployment..."
echo ""

echo "Tools:"
orchestrate tools list | grep -i "open_account" || echo "⚠️  Tool not found in list"
echo ""

echo "Agents:"
orchestrate agents list | grep -i "account_opening" || echo "⚠️  Agent not found in list"
echo ""

echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test the agent: orchestrate agents test account_opening_agent_v2"
echo "2. Try opening an account in the UI"
echo "3. Verify dropdown menu appears for account type selection"
echo ""
echo "Documentation:"
echo "- Implementation Guide: docs/ACCOUNT_OPENING_IMPLEMENTATION.md"
echo ""

# Made with Bob
