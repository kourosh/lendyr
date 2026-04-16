# Local Testing Guide - Context Variable Fix

## Quick Start

### 1. Import Everything Locally

```bash
./scripts/import_local_with_context_fix.sh
```

This imports:
- ✅ Authentication tool with `x-ibm-context-output`
- ✅ All 10 customer ID tools with `x-ibm-context-mapping`
- ✅ All 6 agents

### 2. Start Agent Interaction

```bash
orchestrate agents run lendyr_customer_care --input "Hi, I need help with my account"
```

### 3. Test the Context Variable Flow

**Test with multiple runs:**

```bash
# First interaction - greeting
orchestrate agents run lendyr_customer_care --input "Hi"

# Provide customer ID
orchestrate agents run lendyr_customer_care --input "846301"

# Provide PIN
orchestrate agents run lendyr_customer_care --input "12345"

# Request account info (this should use context variable)
orchestrate agents run lendyr_customer_care --input "Show me my account balances"
```

**Note:** The `orchestrate agents run` command doesn't maintain conversation state between calls. For a full conversation flow, you may need to provide all information in one input or use the cloud deployment.

## What to Watch For

### ✅ Success Indicators
- Authentication succeeds
- Account agent is called
- Account data is returned
- No "path_customer_id" errors

### ❌ Failure Indicators
- `"path_customer_id": "unknown"` or `"UNKNOWN"` or `""`
- 404/500 errors from API
- "Failed to execute open api tool" messages

## Debugging

### Check Tool Import
```bash
orchestrate tools list
```

Should show:
- Customer Authentication
- get_accounts_by_customer_id
- get_loans_by_customer_id
- etc.

### Check Agent Status
```bash
orchestrate agents list
```

Should show all 6 agents.

### View Agent Details
```bash
orchestrate agents get lendyr_customer_care
```

Check that `context_variables: [customer_id]` is present.

### Test Individual Tool
```bash
orchestrate tools test get_accounts_by_customer_id \
  --input '{"customer_id": "846301"}'
```

## Common Issues

### Issue: "Orchestrate ADK not found"
**Solution:**
```bash
pip install ibm-watsonx-orchestrate-adk
```

### Issue: "Authentication tool not found"
**Solution:** Re-run the import script:
```bash
./scripts/import_local_with_context_fix.sh
```

### Issue: Still getting "path_customer_id: UNKNOWN"
**Possible causes:**
1. Tools not re-imported after adding `x-ibm-context-output`
2. Agent cache - try recreating the agent
3. Context variable name mismatch

**Debug steps:**
```bash
# 1. Delete and recreate agents
orchestrate agents delete lendyr_customer_care
orchestrate agents delete account_agent
./scripts/import_local_with_context_fix.sh

# 2. Check the authentication tool spec
cat tools/customer_auth_tool/customer_auth_openapi.json | grep -A 3 "x-ibm-context-output"

# 3. Check a customer ID tool spec  
cat tools/get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get/lendyr_openapi.json | grep -A 1 "x-ibm-context-mapping"
```

## Viewing Logs

Enable verbose logging:
```bash
export ORCHESTRATE_LOG_LEVEL=DEBUG
orchestrate agents chat lendyr_customer_care
```

## Test Customers

Valid test credentials:
- Customer ID: `846301`, PIN: `12345`
- Customer ID: `846302`, PIN: `67890`
- Customer ID: `846303`, PIN: `11111`

## Expected Flow

1. **Authentication Phase:**
   - User provides customer_id and PIN
   - Main agent calls `authenticate_customer_auth_validate_post`
   - Tool returns: `{"success": true, "customer_id": "846301", ...}`
   - **Context variable automatically set** via `x-ibm-context-output`

2. **Delegation Phase:**
   - User asks for account info
   - Main agent calls `account_agent`
   - **Context variable automatically passed** to collaborator

3. **Tool Execution Phase:**
   - Account agent calls `get_accounts_by_customer_id`
   - **Context variable automatically mapped** to path parameter via `x-ibm-context-mapping`
   - API receives: `GET /customers/by-id/846301/accounts`
   - Success!

## Next Steps

Once working locally:
1. Deploy to cloud: `./scripts/import_all_to_lendyr_cloud.sh`
2. Test in production environment
3. Update documentation with findings

## Related Documentation

- [Context Variable Fix](./CONTEXT_VARIABLE_FIX.md) - Technical details
- [Quick Fix Guide](./CONTEXT_VARIABLE_QUICK_FIX.md) - Summary
- [Demo Flow](./DEMO_CONVERSATION_FLOW_V2.md) - Full demo script