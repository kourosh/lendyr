#!/bin/bash

# Lendyr Bank - Local Orchestrate ADK Setup Script
# This script helps you quickly set up the local development environment

set -e  # Exit on error

echo "================================================"
echo "Lendyr Bank - Orchestrate ADK Setup"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from correct directory
if [ ! -f "agents/lendyr_customer_care.yaml" ]; then
    echo -e "${RED}Error: Please run this script from the lendyr project root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if Orchestrate ADK is installed
if ! command -v orchestrate &> /dev/null; then
    echo -e "${YELLOW}Orchestrate ADK not found. Installing...${NC}"
    pip install ibm-watsonx-orchestrate-adk
    echo -e "${GREEN}✓ Orchestrate ADK installed${NC}"
else
    echo -e "${GREEN}✓ Orchestrate ADK already installed${NC}"
fi

echo ""
echo -e "${YELLOW}Step 2: Checking environment variables...${NC}"

# Check for required environment variables
if [ -z "$IBM_CLOUD_API_KEY" ]; then
    echo -e "${RED}Error: IBM_CLOUD_API_KEY environment variable is not set${NC}"
    echo "Please set it with: export IBM_CLOUD_API_KEY='your_api_key_here'"
    exit 1
fi
echo -e "${GREEN}✓ IBM_CLOUD_API_KEY is set${NC}"

if [ -z "$WATSONX_PROJECT_ID" ]; then
    echo -e "${YELLOW}Warning: WATSONX_PROJECT_ID is not set${NC}"
    echo "You may need to set it with: export WATSONX_PROJECT_ID='your_project_id_here'"
else
    echo -e "${GREEN}✓ WATSONX_PROJECT_ID is set${NC}"
fi

echo ""
echo -e "${YELLOW}Step 3: Verifying API endpoint...${NC}"

API_ENDPOINT="https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"
if curl -s -f "$API_ENDPOINT/health" > /dev/null; then
    echo -e "${GREEN}✓ API endpoint is accessible${NC}"
else
    echo -e "${RED}Error: Cannot reach API endpoint at $API_ENDPOINT${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 4: Initializing Orchestrate project...${NC}"

# Initialize Orchestrate project if not already done
if [ ! -f ".orchestrate/config.yaml" ]; then
    orchestrate init --force
    echo -e "${GREEN}✓ Orchestrate project initialized${NC}"
else
    echo -e "${GREEN}✓ Orchestrate project already initialized${NC}"
fi

echo ""
echo -e "${YELLOW}Step 5: Importing API tools...${NC}"

# Import OpenAPI specification
orchestrate tools import \
    --file tools/lendyr_openapi.json \
    --name "Lendyr Bank API" \
    --force

echo -e "${GREEN}✓ API tools imported${NC}"

echo ""
echo -e "${YELLOW}Step 6: Creating agents...${NC}"

# Create agents in the correct order
AGENTS=(
    "disputes_agent"
    "account_agent"
    "card_agent"
    "loan_agent"
    "lendyr_customer_care"
)

for agent in "${AGENTS[@]}"; do
    echo "Creating $agent..."
    if orchestrate agents create --file "agents/${agent}.yaml" --force; then
        echo -e "${GREEN}✓ $agent created${NC}"
    else
        echo -e "${RED}✗ Failed to create $agent${NC}"
    fi
done

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Setup Complete! 🎉${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test an agent: orchestrate agents test loan_agent --message 'Test message'"
echo "2. Start chat: orchestrate agents chat lendyr_customer_care"
echo "3. View agents: orchestrate agents list"
echo ""
echo "For the full demo, follow: docs/DEMO_CONVERSATION_FLOW_V2.md"
echo ""

# Made with Bob
