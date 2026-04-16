#!/bin/bash

# Script to verify tools are correctly imported in cloud with context mapping

echo "=========================================="
echo "Verifying Cloud Tool Configuration"
echo "=========================================="

# Check active environment
echo ""
echo "Active environment:"
orchestrate env list | grep "(active)"

echo ""
echo "=========================================="
echo "Checking Authentication Tool"
echo "=========================================="

# Check if authentication tool has x-ibm-context-output
echo ""
echo "Looking for x-ibm-context-output in authentication tool..."
if grep -q "x-ibm-context-output" tools/customer_auth_tool/customer_auth_openapi.json; then
    echo "✓ Local file has x-ibm-context-output"
else
    echo "✗ Local file MISSING x-ibm-context-output"
fi

echo ""
echo "=========================================="
echo "Checking Customer ID Tools"
echo "=========================================="

# Check a sample tool for x-ibm-context-mapping
SAMPLE_TOOL="tools/get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get/lendyr_openapi.json"
echo ""
echo "Checking: $SAMPLE_TOOL"
if grep -q "x-ibm-context-mapping" "$SAMPLE_TOOL"; then
    echo "✓ Local file has x-ibm-context-mapping"
    echo ""
    echo "Context mapping configuration:"
    grep -A 1 "x-ibm-context-mapping" "$SAMPLE_TOOL"
else
    echo "✗ Local file MISSING x-ibm-context-mapping"
fi

echo ""
echo "=========================================="
echo "Listing Imported Tools in Cloud"
echo "=========================================="
orchestrate tools list | head -20

echo ""
echo "=========================================="
echo "Recommendation"
echo "=========================================="
echo ""
echo "If tools are listed above but still getting 'unknown' errors:"
echo "1. The cloud may be caching old tool definitions"
echo "2. Try deleting and re-importing tools:"
echo ""
echo "   # Delete all tools (if supported)"
echo "   orchestrate tools list | while read tool; do"
echo "     orchestrate tools delete \"\$tool\""
echo "   done"
echo ""
echo "   # Then re-import"
echo "   ./scripts/import_all_to_lendyr_cloud.sh"
echo ""
echo "3. Or check if there's a 'force update' or 'refresh' command"
echo ""

# Made with Bob
