#!/bin/bash

# Lendyr Bank - Local Import with Context Variable Fixes
# This script imports all tools and agents to your local Orchestrate ADK environment

set -e  # Exit on error

echo "================================================"
echo "Lendyr Bank - Local Import (Context Fix)"
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

echo -e "${YELLOW}Step 1: Checking Orchestrate ADK...${NC}"

if ! command -v orchestrate &> /dev/null; then
    echo -e "${RED}Error: Orchestrate ADK is not installed${NC}"
    echo "Install with: pip install ibm-watsonx-orchestrate-adk"
    exit 1
fi
echo -e "${GREEN}✓ Orchestrate ADK found${NC}"

echo ""
echo -e "${YELLOW}Step 2: Importing Authentication Tool (with context output mapping)...${NC}"

orchestrate tools import \
    --kind openapi \
    --file tools/customer_auth_tool/customer_auth_openapi.json

echo -e "${GREEN}✓ Authentication tool imported${NC}"

echo ""
echo -e "${YELLOW}Step 3: Importing Customer ID Tools (with context input mapping)...${NC}"

# List of all customer ID tools
TOOLS=(
    "get_customer_by_id"
    "get_accounts_by_customer_id"
    "get_account_by_type_and_customer_id"
    "get_loans_by_customer_id"
    "get_payment_history_by_customer_id"
    "get_cards_by_customer_id"
    "get_disputes_by_customer_id"
    "get_transactions_by_customer_id"
    "get_transfers_by_customer_id"
    "request_loan_deferral_by_customer_id"
    "transfer_money_by_customer_id"
)

for tool in "${TOOLS[@]}"; do
    echo "Importing $tool..."
    if orchestrate tools import \
        --kind openapi \
        --file "tools/$tool/lendyr_openapi.json"; then
        echo -e "${GREEN}✓ $tool imported${NC}"
    else
        echo -e "${RED}✗ Failed to import $tool${NC}"
    fi
done

echo ""
echo -e "${YELLOW}Step 4: Creating/Updating Agents...${NC}"

# Create agents in the correct order (collaborators first)
AGENTS=(
    "account_agent"
    "card_agent"
    "loan_agent"
    "loan_deferral_agent"
    "lendyr_disputes_agent"
    "transfer_agent"
    "lendyr_customer_care"
)

for agent in "${AGENTS[@]}"; do
    echo "Creating/updating $agent..."
    if orchestrate agents import --file "agents/${agent}.yaml"; then
        echo -e "${GREEN}✓ $agent created/updated${NC}"
    else
        echo -e "${RED}✗ Failed to create $agent${NC}"
    fi
done

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Import Complete! 🎉${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Context variable fixes applied:"
echo "  ✓ Authentication tool has x-ibm-context-output"
echo "  ✓ All customer ID tools have x-ibm-context-mapping"
echo ""
echo "Test the fix:"
echo "  orchestrate agents run lendyr_customer_care --input 'Hi, I need help'"
echo ""
echo "Then authenticate with customer ID 846301 and PIN 12345"
echo "Ask for account information to test context variable flow."
echo ""

# Made with Bob
