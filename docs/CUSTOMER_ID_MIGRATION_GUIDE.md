# Customer ID Migration Guide

## Overview
This guide documents the migration from email-based to customer_id-based API calls for the Lendyr Bank demo. This change improves the architecture by using customer_id as the primary identifier passed between the orchestrator agent and collaborator agents.

## Changes Made

### 1. API Backend Changes (`lendyr_code_engine/main.py`)

#### Added New Customer ID-Based Endpoints
All existing email-based endpoints now have customer_id equivalents:

- `GET /customers/by-id/{customer_id}` - Get customer profile
- `GET /customers/by-id/{customer_id}/accounts` - Get all accounts
- `GET /customers/by-id/{customer_id}/accounts/{account_type}` - Get specific account type
- `GET /customers/by-id/{customer_id}/transactions` - Get transactions
- `GET /customers/by-id/{customer_id}/cards` - Get cards
- `GET /customers/by-id/{customer_id}/loans` - Get loans
- `GET /customers/by-id/{customer_id}/disputes` - Get disputes
- `GET /customers/by-id/{customer_id}/payment-history` - Get payment history
- `POST /customers/by-id/{customer_id}/loans/{loan_id}/defer` - Request loan deferral

#### Updated Authentication Response
The `/auth/validate` endpoint now returns both `customer_id` and `customer_email`:

```json
{
  "success": true,
  "customer_id": "846301",
  "customer_email": "brian.nguyen@email.com",
  "customer_name": "Brian Nguyen",
  "message": "Welcome, Brian Nguyen! Authentication successful."
}
```

### 2. Tool Definitions

#### Created New Tool Directories
Each customer_id-based endpoint has its own tool directory with an OpenAPI spec:

- `tools/get_customer_by_id_customers_by_id_customer_id_get/`
- `tools/get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get/`
- `tools/get_account_by_type_and_customer_id_customers_by_id_customer_id_accounts_account_type_get/`
- `tools/get_transactions_by_customer_id_customers_by_id_customer_id_transactions_get/`
- `tools/get_loans_by_customer_id_customers_by_id_customer_id_loans_get/`
- `tools/get_payment_history_by_customer_id_customers_by_id_customer_id_payment_history_get/`
- `tools/request_loan_deferral_by_customer_id_customers_by_id_customer_id_loans_loan_id_defer_post/`

#### Consolidated OpenAPI Spec
Created `tools/lendyr_openapi_customer_id.json` containing all customer_id-based endpoints for easy reference.

### 3. Agent Updates

#### Orchestrator Agent (`agents/lendyr_customer_care.yaml`)
**Changes:**
- Now stores and passes `customer_id` instead of `customer_email` to collaborators
- Updated instructions to reference customer_id
- Updated tool reference to use `get_customer_by_id_customers_by_id__customer_id__get`

**Handoff Pattern:**
```
"The customer_id is [customer_id]. Please help them with [request]."
```

#### Loan Deferral Agent (`agents/loan_deferral_agent.yaml`)
**Changes:**
- Updated instructions to expect `customer_id` from session context
- Updated tools to use customer_id-based endpoints:
  - `get_customer_by_id_customers_by_id__customer_id__get`
  - `get_loans_by_customer_id_customers_by_id__customer_id__loans_get`
  - `get_payment_history_by_customer_id_customers_by_id__customer_id__payment_history_get`
  - `request_loan_deferral_by_customer_id_customers_by_id__customer_id__loans__loan_id__defer_post`

#### Account Agent (`agents/account_agent.yaml`)
**Changes:**
- Updated instructions to expect `customer_id` instead of email
- Updated tools to use customer_id-based endpoints:
  - `get_customer_by_id_customers_by_id__customer_id__get`
  - `get_accounts_by_customer_id_customers_by_id__customer_id__accounts_get`
  - `get_account_by_type_and_customer_id_customers_by_id__customer_id__accounts__account_type__get`
  - `get_transactions_by_customer_id_customers_by_id__customer_id__transactions_get`

## Deployment Steps

### Step 1: Deploy Updated API to IBM Cloud

```bash
cd /Users/kk76/Public/lendyr

# Deploy the updated API with new customer_id endpoints
./scripts/deploy-ibm.sh
```

**Expected Output:**
- Docker image built successfully
- Image pushed to IBM Container Registry
- Code Engine application updated
- New API URL displayed

### Step 2: Verify API Endpoints

Test the new customer_id-based endpoints:

```bash
# Test customer lookup by ID
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301

# Test loans by customer ID
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301/loans

# Test payment history by customer ID
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301/payment-history

# Test authentication (should return customer_id)
curl -X POST https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/auth/validate \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 846301, "pin": "12345"}'
```

### Step 3: Update Orchestrate Agents

```bash
# Remove and recreate the orchestrator agent
orchestrate agents remove --name lendyr_customer_care --kind native
orchestrate agents create --file agents/lendyr_customer_care.yaml

# Remove and recreate the loan deferral agent
orchestrate agents remove --name loan_deferral_agent --kind native
orchestrate agents create --file agents/loan_deferral_agent.yaml

# Remove and recreate the account agent
orchestrate agents remove --name account_agent --kind native
orchestrate agents create --file agents/account_agent.yaml
```

**Alternative: Update using import**
```bash
# Update agents by re-importing (uses same name to update)
orchestrate agents import --file agents/lendyr_customer_care.yaml
orchestrate agents import --file agents/loan_deferral_agent.yaml
orchestrate agents import --file agents/account_agent.yaml
```

### Step 4: Verify Agent Configuration

```bash
# List all agents
orchestrate agents list

# Check specific agent details
orchestrate agents get loan_deferral_agent
orchestrate agents get lendyr_customer_care
orchestrate agents get account_agent
```

## Testing the Fix

### Test Case 1: Loan Deferral Flow (The Original Bug)

```bash
orchestrate chat ask --agent-name lendyr_customer_care
```

**Test Script:**
1. **User:** "Hi, I need help with my loan payment"
2. **Agent:** Asks for customer ID
3. **User:** "846301"
4. **Agent:** Asks for PIN
5. **User:** "12345"
6. **Agent:** Authenticates and asks how to help
7. **User:** "I need to defer my next loan payment"
8. **Agent:** Routes to loan_deferral_agent
9. **Loan Agent:** Calls tools with customer_id (not email)
10. **Loan Agent:** Shows eligibility and deferral terms
11. **User:** "Yes, I agree"
12. **Loan Agent:** Successfully processes deferral ✅

**Expected Result:** No more "Customer not found" error. The deferral should complete successfully.

### Test Case 2: Account Balance Check

```bash
orchestrate chat ask --agent-name lendyr_customer_care
```

**Test Script:**
1. **User:** "Check my account balances"
2. **Agent:** Asks for customer ID
3. **User:** "846301"
4. **Agent:** Asks for PIN
5. **User:** "12345"
6. **Agent:** Routes to account_agent with customer_id
7. **Account Agent:** Shows all account balances ✅

### Test Case 3: Direct API Test

```bash
# Test the exact endpoint that was failing
curl -X POST \
  https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301/loans/LOAN-001/defer \
  -H "Content-Type: application/json" \
  -d '{"reason": "30-day deferral approved. Credit score and payment history criteria met."}'
```

**Expected Response:**
```json
{
  "loan_id": "LOAN-001",
  "customer_id": "846301",
  "customer_name": "Brian Nguyen",
  "approval_status": "approved",
  "approval_reason": "Approved based on excellent credit score (755) and perfect payment history (45/45 on-time payments)",
  "deferral_details": {
    "reason": "30-day deferral approved...",
    "deferred_payment_amount": 469.35,
    "interest_accrued": 102.15,
    "new_outstanding_balance": 17785.73,
    "original_next_payment_date": "2026-04-13",
    "new_next_payment_date": "2026-05-13"
  },
  "credit_evaluation": {
    "credit_score": 755,
    "total_payments": 45,
    "on_time_payments": 45,
    "missed_payments": 0,
    "on_time_percentage": 100.0
  }
}
```

## Troubleshooting

### Issue: "Customer not found" error persists

**Solution:**
1. Verify the API was deployed successfully
2. Check that the new endpoints exist:
   ```bash
   curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/846301
   ```
3. Verify agents are using the new tool names
4. Check agent logs:
   ```bash
   orchestrate agents logs loan_deferral_agent
   ```

### Issue: Agent still trying to use email

**Solution:**
1. Remove and recreate the agent:
   ```bash
   orchestrate agents remove --name loan_deferral_agent --kind native
   orchestrate agents create --file agents/loan_deferral_agent.yaml
   ```
2. Clear any cached sessions
3. Start a fresh conversation

### Issue: Tool not found error

**Solution:**
1. Verify tool directories exist:
   ```bash
   ls -la tools/ | grep customer_id
   ```
2. Re-import tools if needed:
   ```bash
   orchestrate skills import-api --file tools/lendyr_openapi_customer_id.json --force
   ```

## Benefits of This Change

1. **Cleaner Architecture**: customer_id is the natural primary key
2. **Better Performance**: No need to look up customer_id from email on every call
3. **Consistency**: All collaborator agents use the same identifier
4. **Debugging**: Easier to trace requests through the system
5. **Security**: customer_id is already validated during authentication

## Backward Compatibility

The original email-based endpoints remain functional for backward compatibility:
- `/customers/{email}`
- `/customers/{email}/loans`
- `/customers/{email}/payment-history`
- etc.

However, all new agent implementations should use the customer_id-based endpoints.

## Files Modified

### Backend
- `lendyr_code_engine/main.py` - Added customer_id endpoints and updated auth response

### Tools
- Created 7+ new tool directories with OpenAPI specs
- Created `tools/lendyr_openapi_customer_id.json`

### Agents
- `agents/lendyr_customer_care.yaml` - Updated to pass customer_id
- `agents/loan_deferral_agent.yaml` - Updated to use customer_id tools
- `agents/account_agent.yaml` - Updated to use customer_id tools

## Next Steps

After successful deployment and testing:

1. Update remaining collaborator agents (card_agent, loan_agent, disputes_agent) to use customer_id
2. Update documentation to reflect the new architecture
3. Consider deprecating email-based endpoints in a future release
4. Add monitoring for the new endpoints

## Support

For issues or questions:
- Check agent logs: `orchestrate agents logs <agent_name>`
- Check API logs: `ibmcloud ce app logs --name lendyr-db2-api`
- Review this guide and the original bug report