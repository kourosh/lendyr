# Context Variable Mapping Fix

## Problem

When collaborator agents tried to call tools with `customer_id` as a path parameter, errors occurred:

```json
{
  "path_customer_id": "unknown"  // or ""
}
```

This resulted in 404/500 errors from the API.

## Root Causes

### Issue 1: Missing OpenAPI Schema Field
The authentication tool's OpenAPI spec was missing the `customer_id` field in the output schema, even though the API returns it.

### Issue 2: Missing Context Output Mapping
The authentication tool didn't specify that its `customer_id` output should populate the context variable. Agents cannot programmatically set context variables - they must be populated automatically from tool responses.

### Issue 3: Missing Context Input Mapping
**watsonx Orchestrate ADK does not automatically map context variables to OpenAPI path parameters.**

While context variables are successfully shared between agents when using `context_access_enabled: true` and declaring `context_variables: [customer_id]`, the ADK does NOT automatically substitute these context values into tool path parameters like `{customer_id}` in API paths.

## Solutions Applied

### Fix 1: Add customer_id to Authentication Response Schema

Updated [`tools/customer_auth_tool/customer_auth_openapi.json`](../tools/customer_auth_tool/customer_auth_openapi.json) to include `customer_id` in the `CustomerAuthOutput` schema:

```json
"CustomerAuthOutput": {
  "properties": {
    "success": { "type": "boolean" },
    "customer_id": { "type": "string" },  // ← ADDED
    "customer_email": { "type": "string" },
    "customer_name": { "type": "string" },
    "message": { "type": "string" }
  }
}
```

### Fix 2: Add Context Output Mapping to Authentication Tool

**CRITICAL FIX**: Added `x-ibm-context-output` to the authentication operation to automatically populate the context variable from the tool response:

```json
{
  "post": {
    "summary": "Authenticate customer",
    "operationId": "authenticate_customer",
    "x-ibm-context-output": {
      "customer_id": "customer_id"
    },  // ← ADDED - Maps response field to context variable
    "requestBody": { ... }
  }
}
```

This tells watsonx Orchestrate: "When this tool returns successfully, take the `customer_id` field from the response and automatically set it as the `customer_id` context variable."

**Without this**, agents cannot set context variables - they have no API to do so. Context variables must be populated automatically from tool responses.

### Fix 3: Add Context Input Mapping to Path Parameters

Added the `x-ibm-context-mapping` extension to all OpenAPI tool path parameters:

**Before:**
```json
{
  "name": "customer_id",
  "in": "path",
  "required": true,
  "schema": {
    "type": "string",
    "title": "Customer Id"
  }
}
```

**After:**
```json
{
  "name": "customer_id",
  "in": "path",
  "required": true,
  "schema": {
    "type": "string",
    "title": "Customer Id"
  },
  "x-ibm-context-mapping": "customer_id"  // ← ADDED
}
```

This tells watsonx Orchestrate to automatically substitute the context variable value into the path parameter.

## Files Updated

### Authentication Tool
✅ [`tools/customer_auth_tool/customer_auth_openapi.json`](../tools/customer_auth_tool/customer_auth_openapi.json) - Added `customer_id` to output schema

### All Customer ID Tools (Context Mapping Added)
1. ✅ `get_accounts_by_customer_id_customers_by_id_customer_id_accounts_get/lendyr_openapi.json`
2. ✅ `get_loans_by_customer_id_customers_by_id_customer_id_loans_get/lendyr_openapi.json`
3. ✅ `request_loan_deferral_by_customer_id_customers_by_id_customer_id_loans_loan_id_defer_post/lendyr_openapi.json`
4. ✅ `get_customer_by_id_customers_by_id_customer_id_get/lendyr_openapi.json`
5. ✅ `get_payment_history_by_customer_id_customers_by_id_customer_id_payment_history_get/lendyr_openapi.json`
6. ✅ `get_account_by_type_and_customer_id_customers_by_id_customer_id_accounts_account_type_get/lendyr_openapi.json`
7. ✅ `get_cards_by_customer_id_customers_by_id_customer_id_cards_get/lendyr_openapi.json`
8. ✅ `get_disputes_by_customer_id_customers_by_id_customer_id_disputes_get/lendyr_openapi.json`
9. ✅ `get_transactions_by_customer_id_customers_by_id_customer_id_transactions_get/lendyr_openapi.json`
10. ✅ `get_transfers_by_customer_id_customers_by_id_customer_id_transfers_get/lendyr_openapi.json`

## How It Works

### Agent Flow

1. **Main Agent** ([`lendyr_customer_care`](../agents/lendyr_customer_care.yaml)):
   - Authenticates customer with ID and PIN
   - Extracts `customer_id` from authentication response
   - Sets context variable: `customer_id = "846301"` (example)
   - Calls collaborator agent

2. **Collaborator Agent** (e.g., [`account_agent`](../agents/account_agent.yaml)):
   - Receives `customer_id` in context automatically
   - Calls tool like `get_accounts_by_customer_id`
   - **With `x-ibm-context-mapping`**: The ADK automatically maps the context variable value to the path parameter
   - API receives: `GET /customers/by-id/846301/accounts`

### Without the Fix

Without `x-ibm-context-mapping`, the ADK would:
- Not know to use the context variable for the path parameter
- Send the literal string "unknown" or fail to substitute the value
- Result in API errors

## Deployment Steps

1. **Re-import all updated tools** to watsonx Orchestrate:
   ```bash
   # Use the import script
   ./scripts/import_all_to_lendyr_cloud.sh
   ```

2. **Test the flow**:
   - Authenticate with a valid customer ID and PIN
   - Request account information
   - Verify the collaborator agent successfully retrieves data

3. **Verify in logs**:
   - Check that API calls show the correct customer_id in the path
   - Confirm no more "path_customer_id: unknown" errors

## Key Learnings

### Context Variables in watsonx Orchestrate ADK

1. **Declaration**: Use `context_variables: [variable_name]` in agent YAML
2. **Access**: Enable with `context_access_enabled: true`
3. **Sharing**: Context variables are automatically passed to collaborator agents
4. **Mapping**: Use `x-ibm-context-mapping` to map context to tool parameters

### Best Practices

- Always use `x-ibm-context-mapping` for path parameters that should come from context
- Test agent collaboration flows thoroughly after authentication
- Monitor API logs for parameter substitution issues
- Document context variable flow in agent instructions

## Related Documentation

- [Authentication Implementation](./AUTHENTICATION_IMPLEMENTATION_SUMMARY.md)
- [Customer ID Migration Guide](./CUSTOMER_ID_MIGRATION_GUIDE.md)
- [Agent Collaboration](./BUILD_AGENTS.md)

## References

- watsonx Orchestrate ADK Documentation: Context Variables
- OpenAPI 3.x Specification Extensions
- IBM-specific OpenAPI extensions (`x-ibm-*`)