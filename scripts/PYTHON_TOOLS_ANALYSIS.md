# Python Tools Latency Analysis

## Executive Summary

This document identifies all Python tools in the Lendyr project and analyzes their potential impact on agent response times. Python tools typically introduce more latency than OpenAPI tools due to runtime initialization, dependency loading, and execution overhead.

## Python Tools Inventory

### 1. **calculate_deferral_terms**
- **Location**: `tools/calculate_deferral_terms/calculate_deferral_terms.py`
- **Purpose**: Calculates new payment dates, accrued interest, and updated loan balances for 30-day payment deferrals
- **Dependencies**: `datetime`, `dateutil` (from requirements.txt)
- **Used By**: 
  - `loan_deferral_agent` (line 100)
- **Latency Impact**: **LOW** - Pure calculation tool with no external API calls or database connections
- **Recommendation**: Keep as Python tool (calculations are straightforward and fast)

---

### 2. **get_loan_details**
- **Location**: `tools/get_loan_details/get_loan_details.py`
- **Purpose**: Retrieves comprehensive loan information including credit score, payment history, and deferral status
- **Dependencies**: `requests`, `os` (from requirements.txt and code)
- **Used By**:
  - `loan_agent` (line 63)
  - `loan_deferral_agent` (line 99)
- **Latency Impact**: **MEDIUM-HIGH** - Makes HTTP requests to external Lendyr API
- **Recommendation**: **CONVERT TO OPENAPI TOOL** - This is a simple GET request that would be faster as an OpenAPI tool

---

### 3. **customer_auth_tool.py** (authenticate_customer)
- **Location**: `tools/customer_auth_tool.py`
- **Purpose**: Authenticates customers using phone number and PIN against DB2 database
- **Dependencies**: `ibm_db`, `os`, environment variables for DB2 connection
- **Used By**:
  - `lendyr_customer_care` (line 109)
- **Latency Impact**: **HIGH** - Establishes DB2 database connection on every call, performs SQL query
- **Recommendation**: **CRITICAL - OPTIMIZE OR REPLACE**
  - Option 1: Convert to OpenAPI tool that calls a lightweight API endpoint with connection pooling
  - Option 2: Implement connection pooling in Python tool
  - Option 3: Use cached authentication tokens

---

### 4. **process_invoice_upload**
- **Location**: `tools/process_invoice_upload/process_invoice_upload.py`
- **Purpose**: Processes uploaded invoice files for bill payment
- **Dependencies**: Unknown (file needs inspection)
- **Used By**: **NONE** - No agents currently reference this tool
- **Latency Impact**: **UNKNOWN** - Likely HIGH if it processes files
- **Recommendation**: Not currently affecting agent performance (unused)

---

### 5. **extract_invoice_info** (from extract_invoice_info.py)
- **Location**: `tools/extract_invoice_info/extract_invoice_info.py`
- **Purpose**: Extracts structured information from invoice documents
- **Dependencies**: Unknown (file needs inspection)
- **Used By**: **NONE** - No agents currently reference this tool
- **Latency Impact**: **UNKNOWN** - Likely HIGH if it uses OCR or document processing
- **Recommendation**: Not currently affecting agent performance (unused)

---

### 6. **customer_authentication_flow.py**
- **Location**: `tools/customer_authentication_flow.py`
- **Purpose**: Flow-based authentication with retry logic
- **Type**: Flow tool (not a standard Python tool)
- **Used By**: **NONE** - No agents currently reference this tool
- **Latency Impact**: **UNKNOWN**
- **Recommendation**: Not currently affecting agent performance (unused)

---

### 7. **invoice_extraction_flow.py**
- **Location**: `tools/invoice_extraction_flow.py`
- **Purpose**: Flow-based invoice extraction
- **Type**: Flow tool (not a standard Python tool)
- **Used By**: **NONE** - Previously referenced by `lendyr_customer_care` but removed
- **Latency Impact**: **UNKNOWN**
- **Recommendation**: Not currently affecting agent performance (unused)

---

## Agent-to-Python-Tool Mapping

| Agent | Python Tools Used | Latency Risk |
|-------|------------------|--------------|
| `loan_deferral_agent` | `get_loan_details`, `calculate_deferral_terms` | **MEDIUM-HIGH** |
| `loan_agent` | `get_loan_details` | **MEDIUM-HIGH** |
| `lendyr_customer_care` | `authenticate_customer` (customer_auth_tool.py) | **HIGH** |
| All other agents | None | **NONE** |

---

## Latency Impact Analysis

### High Priority (Immediate Action Recommended)

**1. authenticate_customer (customer_auth_tool.py)**
- **Current Impact**: Every customer interaction with `lendyr_customer_care` requires DB2 connection
- **Estimated Latency**: 500ms - 2000ms per authentication (DB connection + query)
- **Solution Options**:
  - Create OpenAPI endpoint with connection pooling: `/api/auth/customer`
  - Implement JWT tokens with 15-minute expiry to avoid repeated DB calls
  - Use Redis cache for recently authenticated customers

**2. get_loan_details**
- **Current Impact**: Called by 2 agents, makes HTTP request to external API
- **Estimated Latency**: 200ms - 800ms per call
- **Solution**: Convert to OpenAPI tool specification pointing to existing Lendyr API
  - Already have OpenAPI specs in `tools/lendyr_openapi_v2.json`
  - Check if loan details endpoint exists in that spec

### Medium Priority

**3. calculate_deferral_terms**
- **Current Impact**: Pure calculation, minimal latency
- **Estimated Latency**: 10ms - 50ms
- **Solution**: Keep as-is (not a significant contributor to latency)

### Low Priority (Unused Tools)

- `process_invoice_upload` - Not currently used
- `extract_invoice_info` - Not currently used
- `customer_authentication_flow.py` - Not currently used
- `invoice_extraction_flow.py` - Not currently used

---

## Recommendations Summary

### Immediate Actions (High Impact)

1. **Replace `authenticate_customer` with OpenAPI tool**
   - Create REST API endpoint: `POST /api/auth/customer`
   - Implement connection pooling in the API service
   - Return JWT token for subsequent requests
   - **Expected Improvement**: 70-80% reduction in authentication latency

2. **Replace `get_loan_details` with OpenAPI tool**
   - Check if endpoint exists in `tools/lendyr_openapi_v2.json`
   - If not, add it to the OpenAPI specification
   - Update `loan_agent` and `loan_deferral_agent` to use OpenAPI version
   - **Expected Improvement**: 40-60% reduction in loan query latency

### Medium-Term Actions

3. **Audit unused Python tools**
   - Remove or archive: `process_invoice_upload`, `extract_invoice_info`
   - Clean up flow tools if not needed

### Monitoring

4. **Add latency tracking**
   - Instrument tool calls to measure actual execution time
   - Set up alerts for tools exceeding 500ms response time
   - Track P50, P95, P99 latencies for each tool

---

## Technical Details

### Why Python Tools Are Slower

1. **Runtime Initialization**: Python interpreter must load for each tool execution
2. **Dependency Loading**: Libraries like `ibm_db`, `requests` must be imported
3. **No Connection Pooling**: Each call creates new database/HTTP connections
4. **Serialization Overhead**: Data must be serialized/deserialized between agent and tool
5. **Cold Start**: First execution after idle period is significantly slower

### Why OpenAPI Tools Are Faster

1. **Direct HTTP Calls**: Agent makes direct REST API calls
2. **Connection Reuse**: HTTP clients maintain connection pools
3. **No Runtime Overhead**: No Python interpreter initialization
4. **Optimized Serialization**: JSON is natively handled by the platform
5. **Caching**: API responses can be cached at multiple layers

---

## Next Steps

1. Review `tools/lendyr_openapi_v2.json` to identify existing endpoints
2. Create OpenAPI specification for customer authentication endpoint
3. Implement API service with connection pooling for DB2
4. Update agent YAML files to use OpenAPI tools instead of Python tools
5. Test and measure latency improvements
6. Document the migration process

---

**Document Created**: 2026-05-04  
**Last Updated**: 2026-05-04  
**Author**: Bob (AI Assistant)