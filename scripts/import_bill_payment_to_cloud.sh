#!/bin/bash

# Script to import bill payment tools and agents to lendyr-cloud environment
# This includes the bill payment feature with document extraction capability

set -e  # Exit on error

echo "=========================================="
echo "Importing Bill Payment Feature to lendyr-cloud"
echo "=========================================="

# Ensure we're in the correct directory
cd "$(dirname "$0")/.."

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

# Import bill payment OpenAPI tool
echo ""
echo "=========================================="
echo "Importing Bill Payment Tool (OpenAPI)"
echo "=========================================="

if [ -f "tools/create_bill_payment/lendyr_openapi.json" ]; then
    echo "Importing create_bill_payment tool..."
    if uvx --from ibm-watsonx-orchestrate orchestrate tools import -f "tools/create_bill_payment/lendyr_openapi.json" --kind openapi 2>&1 | tee /tmp/import_output.txt; then
        if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
            echo "  ✓ Bill payment tool imported successfully"
            TOOL_SUCCESS=1
        else
            echo "  ⚠ Warning: Unexpected output"
            TOOL_SUCCESS=0
        fi
    else
        echo "  ✗ Failed to import bill payment tool"
        TOOL_SUCCESS=0
    fi
else
    echo "  ✗ Error: tools/create_bill_payment/lendyr_openapi.json not found"
    TOOL_SUCCESS=0
fi

# Import invoice extraction Python tool
echo ""
echo "=========================================="
echo "Importing Invoice Extraction Tool (Python)"
echo "=========================================="

if [ -f "tools/extract_invoice_info/extract_invoice_info.py" ]; then
    echo "Importing extract_invoice_info tool..."
    if uvx --from ibm-watsonx-orchestrate orchestrate tools import -f "tools/extract_invoice_info/extract_invoice_info.py" --kind python 2>&1 | tee /tmp/import_output.txt; then
        if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
            echo "  ✓ Invoice extraction tool imported successfully"
            PYTHON_TOOL_SUCCESS=1
        else
            echo "  ⚠ Warning: Unexpected output"
            PYTHON_TOOL_SUCCESS=0
        fi
    else
        echo "  ✗ Failed to import invoice extraction tool"
        PYTHON_TOOL_SUCCESS=0
    fi
else
    echo "  ✗ Error: tools/extract_invoice_info/extract_invoice_info.py not found"
    PYTHON_TOOL_SUCCESS=0
fi

# Import bill payment agent
echo ""
echo "=========================================="
echo "Importing Bill Payment Agent"
echo "=========================================="

if [ -f "agents/bill_payment_agent.yaml" ]; then
    echo "Importing bill_payment_agent..."
    if uvx --from ibm-watsonx-orchestrate orchestrate agents import -f "agents/bill_payment_agent.yaml" 2>&1 | tee /tmp/import_output.txt; then
        if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
            echo "  ✓ Bill payment agent imported successfully"
            AGENT_SUCCESS=1
        else
            echo "  ⚠ Warning: Unexpected output"
            AGENT_SUCCESS=0
        fi
    else
        echo "  ✗ Failed to import bill payment agent"
        AGENT_SUCCESS=0
    fi
else
    echo "  ✗ Error: agents/bill_payment_agent.yaml not found"
    AGENT_SUCCESS=0
fi

# Update customer care agent (Lena) with bill payment routing
echo ""
echo "=========================================="
echo "Updating Customer Care Agent"
echo "=========================================="

if [ -f "agents/lendyr_customer_care.yaml" ]; then
    echo "Updating lendyr_customer_care agent..."
    if uvx --from ibm-watsonx-orchestrate orchestrate agents import -f "agents/lendyr_customer_care.yaml" 2>&1 | tee /tmp/import_output.txt; then
        if grep -q "imported successfully\|updated successfully" /tmp/import_output.txt; then
            echo "  ✓ Customer care agent updated successfully"
            LENA_SUCCESS=1
        else
            echo "  ⚠ Warning: Unexpected output"
            LENA_SUCCESS=0
        fi
    else
        echo "  ✗ Failed to update customer care agent"
        LENA_SUCCESS=0
    fi
else
    echo "  ✗ Error: agents/lendyr_customer_care.yaml not found"
    LENA_SUCCESS=0
fi

# Final summary
echo ""
echo "=========================================="
echo "Import Complete!"
echo "=========================================="

TOTAL_SUCCESS=$((TOOL_SUCCESS + PYTHON_TOOL_SUCCESS + AGENT_SUCCESS + LENA_SUCCESS))
TOTAL_ITEMS=4

echo "Results:"
echo "  ✓ Bill Payment Tool (OpenAPI): $([ $TOOL_SUCCESS -eq 1 ] && echo 'Success' || echo 'Failed')"
echo "  ✓ Invoice Extraction Tool (Python): $([ $PYTHON_TOOL_SUCCESS -eq 1 ] && echo 'Success' || echo 'Failed')"
echo "  ✓ Bill Payment Agent: $([ $AGENT_SUCCESS -eq 1 ] && echo 'Success' || echo 'Failed')"
echo "  ✓ Customer Care Agent Update: $([ $LENA_SUCCESS -eq 1 ] && echo 'Success' || echo 'Failed')"
echo ""
echo "Summary: $TOTAL_SUCCESS/$TOTAL_ITEMS successful"
echo ""

if [ $TOTAL_SUCCESS -eq $TOTAL_ITEMS ]; then
    echo "✓ All bill payment components imported successfully!"
    echo ""
    echo "Next Steps:"
    echo "1. Verify backend API is deployed with bill payment endpoints"
    echo "2. Test the bill payment feature in the cloud environment"
    echo "3. Upload a test invoice to verify document extraction"
    echo ""
    exit 0
else
    echo "⚠ Some imports failed. Please review the output above."
    echo ""
    echo "Troubleshooting:"
    echo "- Ensure you're connected to the correct environment"
    echo "- Check that all file paths are correct"
    echo "- Verify you have proper permissions"
    echo ""
    exit 1
fi

# Made with Bob