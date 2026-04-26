#!/bin/bash
# Import Transfer Agent and Tools to lendyr-cloud Environment
# This script imports the transfer_agent and its associated tools

set -e

PROJECT_DIR="/Users/kk76/Public/lendyr"
cd "$PROJECT_DIR"

echo "🚀 Importing Transfer Agent to lendyr-cloud Environment"
echo "========================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right environment
echo -e "${YELLOW}Checking active environment...${NC}"
CURRENT_ENV=$(uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate env list 2>/dev/null | grep "active" | awk '{print $2}' || echo "unknown")
echo "Current environment: $CURRENT_ENV"
echo ""

if [ "$CURRENT_ENV" != "lendyr-cloud" ]; then
    echo -e "${RED}Error: Not in lendyr-cloud environment${NC}"
    echo "Please activate lendyr-cloud environment first:"
    echo "  uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate env activate lendyr-cloud"
    exit 1
fi

# Import tools first (dependencies)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 1: Importing Tools${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}Importing get_accounts_by_customer_id tool...${NC}"
if uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate tools import \
    -k openapi \
    -f backups/transfer_agent_export/tools/get_accounts_by_customer_id/lendyr_openapi.json; then
    echo -e "${GREEN}✓ get_accounts_by_customer_id imported${NC}"
else
    echo -e "${RED}✗ Failed to import get_accounts_by_customer_id${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Importing transfer_money_by_customer_id tool...${NC}"
if uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate tools import \
    -k openapi \
    -f backups/transfer_agent_export/tools/transfer_money_by_customer_id/lendyr_openapi.json; then
    echo -e "${GREEN}✓ transfer_money_by_customer_id imported${NC}"
else
    echo -e "${RED}✗ Failed to import transfer_money_by_customer_id${NC}"
    exit 1
fi

# Import agent
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 2: Importing Agent${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}Importing transfer_agent...${NC}"
if uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate agents import \
    -f backups/transfer_agent_export/agents/native/transfer_agent.yaml; then
    echo -e "${GREEN}✓ transfer_agent imported${NC}"
else
    echo -e "${RED}✗ Failed to import transfer_agent${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Import Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "1. Verify import: uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate agents list"
echo "2. Test agent: uvx --with ibm-watsonx-orchestrate==2.8.0 orchestrate chat ask --agent-name transfer_agent"
echo ""

# Made with Bob
