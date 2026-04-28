#!/bin/bash

# Script to remove unused email-based and duplicate tools from lendyr-cloud environment

set -e

echo "=========================================="
echo "Removing Unused Tools from lendyr-cloud"
echo "=========================================="

# Check if lendyr-cloud environment is active
echo ""
echo "Checking active environment..."
ACTIVE_ENV=$(uvx --from ibm-watsonx-orchestrate orchestrate env list | grep "(active)" | awk '{print $1}')
if [ "$ACTIVE_ENV" != "lendyr-cloud" ]; then
    echo "ERROR: lendyr-cloud environment is not active. Current active: $ACTIVE_ENV"
    echo "Please run: uvx --from ibm-watsonx-orchestrate orchestrate env activate lendyr-cloud"
    exit 1
fi
echo "✓ lendyr-cloud environment is active"

# List of unused email-based tools to remove
TOOLS_TO_REMOVE=(
    "get_accounts_customers_email_accounts_get"
    "get_account_by_type_customers_email_accounts_account_type_get"
    "get_cards_customers_email_cards_get"
    "get_customer_customers_email_get"
    "get_transactions_customers_email_transactions_get"
    "get_transfers_customers_email_transfers_get"
    "get_disputes_customers_email_disputes_get"
    "get_loans_customers_email_loans_get"
    "get_payment_history_customers_email_payment_history_get"
    "request_loan_deferral_customers_email_loans_loan_id_defer_post"
    "authenticate_customer_auth_validate_post"
    "get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get"
    "get_account_by_type_and_customer_id_customers_by_id_customer_id_accounts_account_type_get"
    "get_loans_by_customer_id_customers_by_id_customer_id_loans_get"
    "get_payment_history_by_customer_id_customers_by_id_customer_id_payment_history_get"
    "request_loan_deferral_by_customer_id_customers_by_id_customer_id_loans_loan_id_defer_post"
    "health_health_get"
)

echo ""
echo "=========================================="
echo "Removing ${#TOOLS_TO_REMOVE[@]} unused tools..."
echo "=========================================="

REMOVED_COUNT=0
FAILED_COUNT=0

for tool in "${TOOLS_TO_REMOVE[@]}"; do
    echo ""
    echo "Removing: $tool"
    if uvx --from ibm-watsonx-orchestrate orchestrate tools remove -n "$tool" 2>&1; then
        echo "  ✓ Removed successfully"
        ((REMOVED_COUNT++))
    else
        echo "  ⚠ Failed to remove (may not exist)"
        ((FAILED_COUNT++))
    fi
done

echo ""
echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo "Successfully removed: $REMOVED_COUNT tools"
echo "Failed/Not found: $FAILED_COUNT tools"
echo ""
echo "Remaining tools are actively used by agents."
echo ""

exit 0

# Made with Bob
