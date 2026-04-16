#!/bin/bash

# Script to add x-ibm-context-mapping to all customer_id path parameters
# This fixes the "path_customer_id: unknown" error in watsonx Orchestrate

TOOLS_DIR="tools"

# List of tool directories that need updating
TOOLS=(
  "get_customer_by_id_customers_by_id_customer_id_get"
  "get_payment_history_by_customer_id_customers_by_id_customer_id_payment_history_get"
  "get_account_by_type_and_customer_id_customers_by_id_customer_id_accounts_account_type_get"
  "get_cards_by_customer_id_customers_by_id_customer_id_cards_get"
  "get_disputes_by_customer_id_customers_by_id_customer_id_disputes_get"
  "get_transactions_by_customer_id_customers_by_id_customer_id_transactions_get"
  "get_transfers_by_customer_id_customers_by_id_customer_id_transfers_get"
)

echo "Adding x-ibm-context-mapping to customer_id path parameters..."

for tool in "${TOOLS[@]}"; do
  file="$TOOLS_DIR/$tool/lendyr_openapi.json"
  
  if [ -f "$file" ]; then
    echo "Processing: $file"
    
    # Use sed to add the x-ibm-context-mapping line after the customer_id parameter definition
    # This adds it right after the closing brace of the schema object
    sed -i.bak '/"name": "customer_id"/,/}/ {
      /}/a\
            ,\
            "x-ibm-context-mapping": "customer_id"
    }' "$file"
    
    # Clean up the backup file
    rm -f "$file.bak"
    
    echo "  ✓ Updated $file"
  else
    echo "  ✗ File not found: $file"
  fi
done

echo ""
echo "Done! All tools have been updated with context mapping."
echo ""
echo "Next steps:"
echo "1. Review the changes in the modified files"
echo "2. Re-import the tools to watsonx Orchestrate"
echo "3. Test the agent collaboration flow"

# Made with Bob
