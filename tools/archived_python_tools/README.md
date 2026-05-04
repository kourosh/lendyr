# Archived Python Tools

This directory contains Python tools that have been replaced with OpenAPI tools for improved performance and reduced latency.

## Archived on: 2026-05-04

## Tools Archived

### 1. get_loan_details/
**Reason**: Replaced with OpenAPI tool at `tools/get_loan_details_openapi/`
- **Original latency**: 200-800ms (HTTP requests + Python runtime overhead)
- **New latency**: ~50-150ms (direct HTTP call)
- **Improvement**: 40-60% reduction in latency
- **Replacement**: Uses consolidated API endpoint `/loans/{customer_id}`

### 2. customer_auth_tool.py
**Reason**: Replaced with OpenAPI tool at `tools/customer_auth_tool/customer_auth_openapi.json`
- **Original latency**: 500-2000ms (DB2 connection + query + Python runtime)
- **New latency**: ~100-300ms (API with connection pooling)
- **Improvement**: 70-80% reduction in latency
- **Replacement**: Uses API endpoint `/auth/validate` with connection pooling

### 3. process_invoice_upload/
**Reason**: Not currently used by any agents
- **Status**: Unused tool
- **Action**: Archived for potential future use

### 4. customer_authentication_flow.py
**Reason**: Flow-based tool not currently used by any agents
- **Status**: Unused flow tool
- **Action**: Archived for potential future use

## Why OpenAPI Tools Are Faster

1. **No Runtime Initialization**: No Python interpreter startup overhead
2. **Connection Pooling**: HTTP clients maintain persistent connections
3. **Direct API Calls**: Agents make direct REST calls without serialization overhead
4. **Optimized Serialization**: JSON is natively handled by the platform
5. **Caching**: API responses can be cached at multiple layers

## Migration Impact

### Agents Updated
- `loan_agent`: Now uses OpenAPI `get_loan_details`
- `loan_deferral_agent`: Now uses OpenAPI `get_loan_details`
- `lendyr_customer_care`: Already using OpenAPI `authenticate_customer`

### Expected Performance Improvements
- **Authentication**: 70-80% faster
- **Loan queries**: 40-60% faster
- **Overall agent response time**: 30-50% improvement for loan-related queries

## Restoration

If you need to restore any of these tools:
1. Copy the tool directory back to `tools/`
2. Update the relevant agent YAML files to reference the Python tool
3. Ensure all dependencies in `requirements.txt` are installed

## Reference

See `scripts/PYTHON_TOOLS_ANALYSIS.md` for the complete analysis that led to these changes.