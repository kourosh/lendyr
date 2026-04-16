#!/bin/bash

# Debug script to import tools one by one with verbose output

set -e

echo "=========================================="
echo "Debug: Importing Customer ID Tools to Cloud"
echo "=========================================="

# Check environment
ACTIVE_ENV=$(orchestrate env list | grep "(active)" | awk '{print $1}')
echo "Active environment: $ACTIVE_ENV"

if [ "$ACTIVE_ENV" != "lendyr-cloud" ]; then
    echo "ERROR: lendyr-cloud not active"
    exit 1
fi

echo ""
echo "=========================================="
echo "Test: Import Authentication Tool"
echo "=========================================="

AUTH_TOOL="tools/customer_auth_tool/customer_auth_openapi.json"
echo "File: $AUTH_TOOL"
echo ""
echo "File contents (first 30 lines):"
head -30 "$AUTH_TOOL"
echo ""
echo "Importing..."
orchestrate tools import -f "$AUTH_TOOL" --kind openapi
echo ""
echo "✓ Authentication tool imported"

echo ""
echo "=========================================="
echo "Test: Import ONE Customer ID Tool"
echo "=========================================="

TEST_TOOL="tools/get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get/lendyr_openapi.json"
echo "File: $TEST_TOOL"
echo ""
echo "Checking for x-ibm-context-mapping:"
grep -A 2 "x-ibm-context-mapping" "$TEST_TOOL" || echo "NOT FOUND"
echo ""
echo "Importing..."
orchestrate tools import -f "$TEST_TOOL" --kind openapi
echo ""
echo "✓ Test tool imported"

echo ""
echo "=========================================="
echo "Verify: List All Tools"
echo "=========================================="
orchestrate tools list

echo ""
echo "=========================================="
echo "Check: Does get_accounts_by_customer_id appear?"
echo "=========================================="
orchestrate tools list | grep -i "account" || echo "NOT FOUND in tools list"

echo ""
echo "Done!"

# Made with Bob
