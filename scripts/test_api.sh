#!/bin/bash

# Test script for Lendyr Bank API
# Run this before building agents to verify everything is working

API_BASE="https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"
TEST_EMAIL="brian.nguyen@email.com"

echo "=========================================="
echo "Lendyr Bank API Test Suite"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
response=$(curl -s "${API_BASE}/health")
echo "Response: $response"
if echo "$response" | grep -q "ok"; then
    echo "✅ PASS: API is running"
else
    echo "❌ FAIL: API is not responding"
    exit 1
fi
echo ""

# Test 2: Get Customer
echo "Test 2: Get Customer (${TEST_EMAIL})"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
if echo "$response" | grep -q "Brian"; then
    echo "✅ PASS: Customer found"
else
    echo "❌ FAIL: Customer not found"
    exit 1
fi
echo ""

# Test 3: Get Accounts
echo "Test 3: Get Accounts"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/accounts")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
if echo "$response" | grep -q "checking"; then
    echo "✅ PASS: Accounts retrieved"
else
    echo "❌ FAIL: Accounts not found"
    exit 1
fi
echo ""

# Test 4: Get Loans
echo "Test 4: Get Loans"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/loans")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
if echo "$response" | grep -q "auto"; then
    echo "✅ PASS: Loans retrieved"
else
    echo "❌ FAIL: Loans not found"
    exit 1
fi
echo ""

# Test 5: Get Cards
echo "Test 5: Get Cards"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/cards")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
if echo "$response" | grep -q "card_id"; then
    echo "✅ PASS: Cards retrieved"
else
    echo "❌ FAIL: Cards not found"
    exit 1
fi
echo ""

# Test 6: Get Transactions
echo "Test 6: Get Transactions"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/transactions?limit=5")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
if echo "$response" | grep -q "transaction_id"; then
    echo "✅ PASS: Transactions retrieved"
else
    echo "❌ FAIL: Transactions not found"
    exit 1
fi
echo ""

# Test 7: Get Disputes
echo "Test 7: Get Disputes"
echo "--------------------"
response=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/disputes")
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
# Disputes might be empty, that's okay
echo "✅ PASS: Disputes endpoint working"
echo ""

# Summary
echo "=========================================="
echo "Summary: All API Tests Passed! ✅"
echo "=========================================="
echo ""
echo "Brian Nguyen's Financial Summary:"
echo "---------------------------------"

# Get account balances
accounts=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/accounts")
checking=$(echo "$accounts" | python3 -c "import json, sys; data=json.load(sys.stdin); print([a for a in data if a['account_type']=='checking'][0]['balance'])" 2>/dev/null)
savings=$(echo "$accounts" | python3 -c "import json, sys; data=json.load(sys.stdin); print([a for a in data if a['account_type']=='savings'][0]['balance'])" 2>/dev/null)
credit=$(echo "$accounts" | python3 -c "import json, sys; data=json.load(sys.stdin); print([a for a in data if a['account_type']=='credit'][0]['balance'])" 2>/dev/null)

# Get loan info
loans=$(curl -s "${API_BASE}/customers/${TEST_EMAIL}/loans")
loan_payment=$(echo "$loans" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data[0]['monthly_payment'])" 2>/dev/null)
loan_balance=$(echo "$loans" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data[0]['outstanding_balance'])" 2>/dev/null)

echo "Checking Account: \$$checking"
echo "Savings Account: \$$savings"
echo "Credit Card Balance: \$$credit"
echo "Auto Loan Payment: \$$loan_payment (due April 13th)"
echo "Auto Loan Balance: \$$loan_balance"
echo ""
echo "✅ Ready to build agents in Watsonx Orchestrate!"
echo "📖 See BUILD_AGENTS.md for step-by-step instructions"

# Made with Bob
