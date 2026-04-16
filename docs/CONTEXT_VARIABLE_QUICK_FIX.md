# Quick Fix: Context Variable Mapping

## The Problem
```
Error: {"path_customer_id": "unknown"}  // or ""
Status: 404/500 Internal Server Error
```

## The Solutions

### 1. Fix Authentication Tool Schema
Add `customer_id` to the output schema

### 2. Add Context Output Mapping (CRITICAL)
Add `"x-ibm-context-output"` to automatically populate context variables from tool responses

### 3. Add Context Input Mapping
Add `"x-ibm-context-mapping"` to path parameters that should use context variables

## What Changed

### Change 1: Authentication Tool Output Schema
**File:** `tools/customer_auth_tool/customer_auth_openapi.json`

Added `customer_id` field to the response schema:

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

### Change 2: Context Output Mapping (CRITICAL)
**File:** `tools/customer_auth_tool/customer_auth_openapi.json`

Added `x-ibm-context-output` to automatically populate context variable:

```json
{
  "post": {
    "summary": "Authenticate customer",
    "operationId": "authenticate_customer",
    "x-ibm-context-output": {
      "customer_id": "customer_id"
    },  // ← ADDED - Auto-populates context from response
    "requestBody": { ... }
  }
}
```

**Why this is critical:** Agents cannot programmatically set context variables. Context variables must be automatically populated from tool responses using `x-ibm-context-output`.

### Change 3: Path Parameter Context Mapping
**Files:** All 10 tools with `customer_id` path parameters

**Before (Broken):**
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

**After (Fixed):**
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

## Files Updated
✅ **1 authentication tool** (3 changes) + **10 customer ID tools** (1 change each) = **11 total files**

## Next Steps

1. **Re-import tools to watsonx Orchestrate:**
   ```bash
   ./scripts/import_all_to_lendyr_cloud.sh
   ```

2. **Test the flow:**
   - Authenticate with customer ID and PIN
   - Ask for account information
   - Verify collaborator agents work correctly

## Why This Happened

1. **Missing schema field**: OpenAPI spec didn't declare `customer_id` in output
2. **No context output mapping**: Tool didn't specify to populate context variable from response
3. **No context input mapping**: Path parameters didn't specify to use context variable

## Key Takeaways

**For tools that SET context variables:**
- Add the field to the output schema
- Use `x-ibm-context-output` to map response fields to context variables
- Agents CANNOT set context variables programmatically

**For tools that USE context variables:**
- Use `x-ibm-context-mapping` on path parameters
- Context variables are NOT automatically substituted into paths

---

For detailed explanation, see [`CONTEXT_VARIABLE_FIX.md`](./CONTEXT_VARIABLE_FIX.md)