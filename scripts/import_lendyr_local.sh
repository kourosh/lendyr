#!/bin/bash
# Import All Lendyr Project Assets to watsonx Orchestrate
# This script imports all agents, tools, knowledge bases, and connections

set -e

PROJECT_DIR="/Users/kk76/Public/lendyr"
cd "$PROJECT_DIR"

echo "🚀 Importing All Lendyr Assets to watsonx Orchestrate"
echo "====================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counter for tracking
TOTAL_IMPORTED=0
TOTAL_FAILED=0

# Function to print section headers
print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to import with error handling
import_with_retry() {
    local cmd="$1"
    local description="$2"
    
    echo -e "${YELLOW}Importing: $description${NC}"
    
    if eval "$cmd" 2>&1 | tee /tmp/orchestrate_import.log; then
        if grep -q "error\|Error\|ERROR\|failed\|Failed" /tmp/orchestrate_import.log; then
            echo -e "${RED}✗ Failed: $description${NC}"
            cat /tmp/orchestrate_import.log
            ((TOTAL_FAILED++))
            return 1
        else
            echo -e "${GREEN}✓ Success: $description${NC}"
            ((TOTAL_IMPORTED++))
            return 0
        fi
    else
        echo -e "${RED}✗ Failed: $description${NC}"
        ((TOTAL_FAILED++))
        return 1
    fi
}

# ============================================================================
# STEP 1: Import Tools
# ============================================================================
print_section "📦 STEP 1: Importing Tools"

# OpenAPI Tools
echo "Importing OpenAPI tools..."

import_with_retry \
    "orchestrate tools import -k openapi -f tools/customer_auth_tool/customer_auth_openapi.json" \
    "Customer Authentication Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_customer_by_id/lendyr_openapi.json" \
    "Get Customer By ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_accounts_by_customer_id/lendyr_openapi.json" \
    "Get Accounts By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_cards_by_customer_id/lendyr_openapi.json" \
    "Get Cards By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_transactions_by_customer_id/lendyr_openapi.json" \
    "Get Transactions By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_disputes_by_customer_id/lendyr_openapi.json" \
    "Get Disputes By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_transfers_by_customer_id/lendyr_openapi.json" \
    "Get Transfers By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/transfer_money_by_customer_id/lendyr_openapi.json" \
    "Transfer Money By Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/get_account_by_type_and_customer_id/lendyr_openapi.json" \
    "Get Account By Type and Customer ID Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/update_card_limit_cards_card_id_limit_patch/lendyr_openapi.json" \
    "Update Card Limit Tool"

import_with_retry \
    "orchestrate tools import -k openapi -f tools/update_card_status_cards_card_id_status_patch/lendyr_openapi.json" \
    "Update Card Status Tool"

# Python Tools
echo ""
echo "Importing Python tools..."

if [ -f "tools/calculate_deferral_terms/calculate_deferral_terms.py" ]; then
    import_with_retry \
        "orchestrate tools import -k python -f tools/calculate_deferral_terms/calculate_deferral_terms.py --requirements-file tools/calculate_deferral_terms/requirements.txt" \
        "Calculate Deferral Terms Tool (Python)"
fi

if [ -f "tools/get_loan_details/get_loan_details.py" ]; then
    import_with_retry \
        "orchestrate tools import -k python -f tools/get_loan_details/get_loan_details.py --requirements-file tools/get_loan_details/requirements.txt" \
        "Get Loan Details Tool (Python)"
fi

# ============================================================================
# STEP 2: Import Knowledge Bases
# ============================================================================
print_section "📚 STEP 2: Importing Knowledge Bases"

if [ -f "knowledge_bases/lendyr_overlimit_transfers_knowledge_base.yaml" ]; then
    import_with_retry \
        "orchestrate knowledge-bases import -f knowledge_bases/lendyr_overlimit_transfers_knowledge_base.yaml" \
        "Lendyr Overlimit Transfers Knowledge Base"
fi

if [ -f "knowledge_bases/Lendyr_agent_assist_4368Rc.yaml" ]; then
    import_with_retry \
        "orchestrate knowledge-bases import -f knowledge_bases/Lendyr_agent_assist_4368Rc.yaml" \
        "Lendyr Agent Assist Knowledge Base"
fi

# ============================================================================
# STEP 3: Import Agents
# ============================================================================
print_section "🤖 STEP 3: Importing Agents"

echo "Importing specialist agents first (dependencies)..."

import_with_retry \
    "orchestrate agents import -f agents/account_agent.yaml" \
    "Account Agent"

import_with_retry \
    "orchestrate agents import -f agents/card_agent.yaml" \
    "Card Agent"

import_with_retry \
    "orchestrate agents import -f agents/loan_deferral_agent.yaml" \
    "Loan Deferral Agent"

import_with_retry \
    "orchestrate agents import -f agents/loan_agent.yaml" \
    "Loan Agent"

import_with_retry \
    "orchestrate agents import -f agents/lendyr_disputes_agent.yaml" \
    "Disputes Agent"

if [ -f "agents/transfer_agent.yaml" ]; then
    import_with_retry \
        "orchestrate agents import -f agents/transfer_agent.yaml" \
        "Transfer Agent"
fi

echo ""
echo "Importing main customer care agent..."

import_with_retry \
    "orchestrate agents import -f agents/lendyr_customer_care.yaml" \
    "Lendyr Customer Care Agent (Main)"

echo ""
echo "Importing agent assist agent..."

if [ -f "agents/lendyr_agent_assist.yaml" ]; then
    import_with_retry \
        "orchestrate agents import -f agents/lendyr_agent_assist.yaml" \
        "Lendyr Agent Assist"
fi

echo ""
echo "Importing Gartner demo agents..."

if [ -f "agents/Gartner_Banking_Agent.yaml" ]; then
    import_with_retry \
        "orchestrate agents import -f agents/Gartner_Banking_Agent.yaml" \
        "Gartner Banking Agent"
fi

if [ -f "agents/Gartner_Realtime_Agent_58153S.yaml" ]; then
    import_with_retry \
        "orchestrate agents import -f agents/Gartner_Realtime_Agent_58153S.yaml" \
        "Gartner Realtime Agent"
fi

# ============================================================================
# STEP 4: Import Connections (if any)
# ============================================================================
print_section "🔗 STEP 4: Checking for Connections"

if [ -d "connections" ] && [ "$(ls -A connections/*.yaml 2>/dev/null)" ]; then
    echo "Importing connections..."
    for conn_file in connections/*.yaml; do
        if [ -f "$conn_file" ]; then
            conn_name=$(basename "$conn_file" .yaml)
            import_with_retry \
                "orchestrate connections import -f $conn_file" \
                "Connection: $conn_name"
        fi
    done
else
    echo -e "${YELLOW}No connections found to import${NC}"
fi

# ============================================================================
# Summary
# ============================================================================
print_section "📊 IMPORT SUMMARY"

echo ""
echo -e "${GREEN}✓ Successfully imported: $TOTAL_IMPORTED assets${NC}"
if [ $TOTAL_FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed to import: $TOTAL_FAILED assets${NC}"
    echo ""
    echo -e "${YELLOW}Check the output above for details on failed imports${NC}"
    exit 1
else
    echo -e "${GREEN}✓ All assets imported successfully!${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Verify imports: orchestrate list agents"
echo "2. Test main agent: orchestrate test lendyr_customer_care"
echo "3. Deploy to live: orchestrate deploy lendyr_customer_care"
echo ""
echo "For Gartner demo:"
echo "  orchestrate test Gartner_Banking_Agent"
echo ""

# Made with Bob
