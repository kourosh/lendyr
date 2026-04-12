#!/bin/bash

# Test script for Loan Deferral API endpoints
# Tests both payment history and loan deferral request endpoints

API_URL="https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"

echo "=========================================="
echo "Lendyr Bank - Loan Deferral API Tests"
echo "=========================================="
echo ""

# Test 1: Get Payment History
echo "Test 1: Get Payment History"
echo "----------------------------"
echo "GET /customers/john.doe@lendyrbank.com/payment-history"
echo ""
curl -s -X GET "${API_URL}/customers/john.doe@lendyrbank.com/payment-history" \
  -H "Content-Type: application/json" | jq '.'
echo ""
echo ""

# Test 2: Get Loan Details
echo "Test 2: Get Loan Details"
echo "------------------------"
echo "GET /customers/john.doe@lendyrbank.com/loans"
echo ""
curl -s -X GET "${API_URL}/customers/john.doe@lendyrbank.com/loans" \
  -H "Content-Type: application/json" | jq '.'
echo ""
echo ""

# Test 3: Request Loan Deferral (Eligible Customer)
echo "Test 3: Request Loan Deferral - Eligible Customer"
echo "--------------------------------------------------"
echo "POST /customers/john.doe@lendyrbank.com/loans/L001/defer"
echo ""
curl -s -X POST "${API_URL}/customers/john.doe@lendyrbank.com/loans/L001/defer" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Unexpected medical expenses"
  }' | jq '.'
echo ""
echo ""

# Test 4: Request Loan Deferral (Low Credit Score)
echo "Test 4: Request Loan Deferral - Low Credit Score"
echo "-------------------------------------------------"
echo "POST /customers/jane.smith@lendyrbank.com/loans/L002/defer"
echo ""
curl -s -X POST "${API_URL}/customers/jane.smith@lendyrbank.com/loans/L002/defer" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Temporary financial hardship"
  }' | jq '.'
echo ""
echo ""

# Test 5: Get Customer Profile (Check Credit Score)
echo "Test 5: Get Customer Profile"
echo "----------------------------"
echo "GET /customers/john.doe@lendyrbank.com"
echo ""
curl -s -X GET "${API_URL}/customers/john.doe@lendyrbank.com" \
  -H "Content-Type: application/json" | jq '.credit_score, .first_name, .last_name'
echo ""
echo ""

echo "=========================================="
echo "Tests Complete"
echo "=========================================="
echo ""
echo "Expected Results:"
echo "- Test 1: Should return payment history with statistics"
echo "- Test 2: Should return loan details with balance and payment info"
echo "- Test 3: Should APPROVE (credit score >= 700, no missed payments)"
echo "- Test 4: Should DENY (credit score < 700 or missed payments)"
echo "- Test 5: Should return customer credit score"
echo ""

# Made with Bob
