#!/bin/bash

# Update operationId in all OpenAPI JSON files to use simplified names

set -e

echo "Updating operationId in OpenAPI JSON files..."

# Function to update a single file
update_file() {
    local tool_dir=$1
    local new_operation_id=$2
    local json_file="tools/$tool_dir/lendyr_openapi.json"
    
    if [ -f "$json_file" ]; then
        echo "Updating $json_file..."
        sed -i.bak 's/"operationId": "[^"]*"/"operationId": "'"$new_operation_id"'"/' "$json_file"
        rm "${json_file}.bak"
        echo "✓ Updated $tool_dir"
    else
        echo "✗ File not found: $json_file"
    fi
}

# Update each tool
update_file "get_customer_by_id" "get_customer_by_id"
update_file "get_accounts_by_customer_id" "get_accounts_by_customer_id"
update_file "get_account_by_type_and_customer_id" "get_account_by_type_and_customer_id"
update_file "get_cards_by_customer_id" "get_cards_by_customer_id"
update_file "get_disputes_by_customer_id" "get_disputes_by_customer_id"
update_file "get_loans_by_customer_id" "get_loans_by_customer_id"
update_file "get_payment_history_by_customer_id" "get_payment_history_by_customer_id"
update_file "get_transactions_by_customer_id" "get_transactions_by_customer_id"
update_file "get_transfers_by_customer_id" "get_transfers_by_customer_id"
update_file "request_loan_deferral_by_customer_id" "request_loan_deferral_by_customer_id"

echo ""
echo "✓ All operationIds updated successfully!"

# Made with Bob
