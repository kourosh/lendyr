#!/bin/bash

# Script to import all agents and tools to lendyr-cloud environment
# Based on watsonx Orchestrate ADK documentation

set -e  # Exit on error

echo "=========================================="
echo "Importing All Tools and Agents to lendyr-cloud"
echo "=========================================="

# Ensure we're in the correct directory
cd "$(dirname "$0")/.."

# Check if lendyr-cloud environment is active
echo ""
echo "Checking active environment..."
ACTIVE_ENV=$(orchestrate env list | grep "(active)" | awk '{print $1}')
if [ "$ACTIVE_ENV" != "lendyr-cloud" ]; then
    echo "ERROR: lendyr-cloud environment is not active. Current active: $ACTIVE_ENV"
    echo "Please run: orchestrate env activate lendyr-cloud"
    exit 1
fi
echo "✓ lendyr-cloud environment is active"

# Import all OpenAPI tools
echo ""
echo "=========================================="
echo "Importing OpenAPI Tools"
echo "=========================================="

TOOL_DIRS=(
    "tools/get_account_by_type_and_customer_id_customers_by_id_customer_id_accounts_account_type_get"
    "tools/get_account_by_type_customers_email_accounts_account_type_get"
    "tools/get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get"
    "tools/get_accounts_customers_email_accounts_get"
    "tools/get_cards_by_customer_id_customers_by_id_customer_id_cards_get"
    "tools/get_cards_customers_email_cards_get"
    "tools/get_customer_by_id_customers_by_id_customer_id_get"
    "tools/get_customer_customers_email_get"
    "tools/get_disputes_by_customer_id_customers_by_id_customer_id_disputes_get"
    "tools/get_disputes_customers_email_disputes_get"
    "tools/get_loans_by_customer_id_customers_by_id_customer_id_loans_get"
    "tools/get_loans_customers_email_loans_get"
    "tools/get_payment_history_by_customer_id_customers_by_id_customer_id_payment_history_get"
    "tools/get_payment_history_customers_email_payment_history_get"
    "tools/get_transactions_by_customer_id_customers_by_id_customer_id_transactions_get"
    "tools/get_transactions_customers_email_transactions_get"
    "tools/get_transfers_by_customer_id_customers_by_id_customer_id_transfers_get"
    "tools/get_transfers_customers_email_transfers_get"
    "tools/request_loan_deferral_by_customer_id_customers_by_id_customer_id_loans_loan_id_defer_post"
    "tools/request_loan_deferral_customers_email_loans_loan_id_defer_post"
    "tools/update_card_limit_cards_card_id_limit_patch"
    "tools/update_card_status_cards_card_id_status_patch"
)

TOOL_COUNT=0
TOOL_SUCCESS=0
TOOL_FAILED=0

for TOOL_DIR in "${TOOL_DIRS[@]}"; do
    TOOL_COUNT=$((TOOL_COUNT + 1))
    TOOL_FILE="$TOOL_DIR/lendyr_openapi.json"
    
    if [ -f "$TOOL_FILE" ]; then
        TOOL_NAME=$(basename "$TOOL_DIR")
        echo ""
        echo "[$TOOL_COUNT/${#TOOL_DIRS[@]}] Importing: $TOOL_NAME"
        
        if orchestrate tools import -f "$TOOL_FILE" --kind openapi 2>&1 | tee /tmp/import_output.txt; then
            if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
                echo "  ✓ Success"
                TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
            else
                echo "  ⚠ Warning: Unexpected output"
                TOOL_FAILED=$((TOOL_FAILED + 1))
            fi
        else
            echo "  ✗ Failed"
            TOOL_FAILED=$((TOOL_FAILED + 1))
        fi
    else
        echo "  ⚠ Skipping: $TOOL_FILE not found"
        TOOL_FAILED=$((TOOL_FAILED + 1))
    fi
done

# Import customer auth tool
echo ""
echo "Importing customer authentication tool..."
if [ -f "tools/customer_auth_tool/customer_auth_openapi.json" ]; then
    if orchestrate tools import -f "tools/customer_auth_tool/customer_auth_openapi.json" --kind openapi; then
        echo "  ✓ Customer auth tool imported"
        TOOL_SUCCESS=$((TOOL_SUCCESS + 1))
    else
        echo "  ✗ Customer auth tool failed"
        TOOL_FAILED=$((TOOL_FAILED + 1))
    fi
fi

echo ""
echo "Tool Import Summary:"
echo "  Total: $TOOL_COUNT"
echo "  Success: $TOOL_SUCCESS"
echo "  Failed: $TOOL_FAILED"

# Import all agents
echo ""
echo "=========================================="
echo "Importing Agents"
echo "=========================================="

AGENT_FILES=(
    "agents/account_agent.yaml"
    "agents/card_agent.yaml"
    "agents/loan_agent.yaml"
    "agents/lendyr_disputes_agent.yaml"
    "agents/loan_deferral_agent.yaml"
    "agents/lendyr_customer_care.yaml"
)

AGENT_COUNT=0
AGENT_SUCCESS=0
AGENT_FAILED=0

for AGENT_FILE in "${AGENT_FILES[@]}"; do
    AGENT_COUNT=$((AGENT_COUNT + 1))
    
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .yaml)
        echo ""
        echo "[$AGENT_COUNT/${#AGENT_FILES[@]}] Importing: $AGENT_NAME"
        
        if orchestrate agents import -f "$AGENT_FILE" 2>&1 | tee /tmp/import_output.txt; then
            if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
                echo "  ✓ Success"
                AGENT_SUCCESS=$((AGENT_SUCCESS + 1))
            else
                echo "  ⚠ Warning: Unexpected output"
                AGENT_FAILED=$((AGENT_FAILED + 1))
            fi
        else
            echo "  ✗ Failed"
            AGENT_FAILED=$((AGENT_FAILED + 1))
        fi
    else
        echo "  ⚠ Skipping: $AGENT_FILE not found"
        AGENT_FAILED=$((AGENT_FAILED + 1))
    fi
done

echo ""
echo "Agent Import Summary:"
echo "  Total: $AGENT_COUNT"
echo "  Success: $AGENT_SUCCESS"
echo "  Failed: $AGENT_FAILED"

# Final summary
echo ""
echo "=========================================="
echo "Import Complete!"
echo "=========================================="
echo "Tools: $TOOL_SUCCESS/$TOOL_COUNT successful"
echo "Agents: $AGENT_SUCCESS/$AGENT_COUNT successful"
echo ""

if [ $TOOL_FAILED -gt 0 ] || [ $AGENT_FAILED -gt 0 ]; then
    echo "⚠ Some imports failed. Please review the output above."
    exit 1
else
    echo "✓ All imports successful!"
    exit 0
fi

# Made with Bob
