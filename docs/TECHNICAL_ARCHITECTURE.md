# Watsonx Orchestrate Technical Architecture
## Lendyr Bank Demo Implementation

This document provides technical details about the multi-agent architecture, API integration, and deployment model for the Lendyr Bank customer care demo.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Watsonx Orchestrate Platform                  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Agent Orchestration Layer                    │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │  Customer   │  │   Loan      │  │  Account    │      │  │
│  │  │  Care Agent │◄─┤   Agent     │◄─┤   Agent     │      │  │
│  │  │   (Lena)    │  │             │  │             │      │  │
│  │  └──────┬──────┘  └─────────────┘  └─────────────┘      │  │
│  │         │                                                  │  │
│  │         ├──────────┐                                       │  │
│  │         │          │                                       │  │
│  │  ┌──────▼──────┐  ┌─────▼───────┐                        │  │
│  │  │    Card     │  │  Disputes   │                        │  │
│  │  │    Agent    │  │   Agent     │                        │  │
│  │  └─────────────┘  └─────────────┘                        │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Tool Integration Layer                 │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │get_      │  │get_      │  │get_      │  │update_   │ │  │
│  │  │customer  │  │accounts  │  │loans     │  │card_     │ │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │  │
│  └───────┼─────────────┼─────────────┼─────────────┼────────┘  │
└──────────┼─────────────┼─────────────┼─────────────┼───────────┘
           │             │             │             │
           └─────────────┴─────────────┴─────────────┘
                         │
                    ┌────▼────┐
                    │  HTTPS  │
                    └────┬────┘
                         │
           ┌─────────────▼──────────────┐
           │   Lendyr Bank REST API     │
           │  (IBM Code Engine)         │
           │                             │
           │  FastAPI + CSV Data Layer  │
           └─────────────┬──────────────┘
                         │
                    ┌────▼────┐
                    │   CSV   │
                    │  Files  │
                    └─────────┘
```

---

## 🤖 Agent Architecture

### Agent Hierarchy

**Primary Agent:**
- `lendyr_customer_care` - Main entry point, orchestrates all interactions

**Specialist Agents:**
- `loan_agent` - Loan inquiries and payment information
- `account_agent` - Account balances, transactions, transfers
- `card_agent` - Card management, limits, freeze/unfreeze
- `lendyr_disputes_agent` - Transaction disputes and resolution

### Agent Configuration (YAML)

Each agent is defined using a declarative YAML configuration:

```yaml
spec_version: v1
kind: native
name: loan_agent
description: >
  Specialist agent for loan inquiries
instructions: >
  You are a helpful loan specialist...
  [Detailed instructions for behavior]
llm: watsonx/ibm/granite-3-8b-instruct
style: default
tools:
  - get_customer_customers_email_get
  - get_loans_customers_email_loans_get
  - get_disputes_customers_email_disputes_get
collaborators:
  - account_agent
  - card_agent
```

### Key Configuration Elements

**1. Instructions:**
- Natural language description of agent behavior
- Routing logic (when to hand off to other agents)
- Response formatting guidelines
- Error handling procedures

**2. Tools:**
- List of API operations the agent can invoke
- Each tool maps to an OpenAPI operation
- Tools are invoked automatically based on context

**3. Collaborators:**
- List of other agents this agent can route to
- Enables multi-agent workflows
- Maintains conversation context across handoffs

**4. LLM Selection:**
- Each agent can use a different language model
- Current demo uses IBM Granite 3 8B Instruct
- Can be swapped for other models (GPT-4, Claude, etc.)

---

## 🔧 Tool Integration Architecture

### OpenAPI-Based Tool Definition

Tools are defined using standard OpenAPI 3.x specifications:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Lendyr Bank API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"
    }
  ],
  "paths": {
    "/customers/{email}/loans": {
      "get": {
        "operationId": "get_loans_customers_email_loans_get",
        "summary": "Get loan details",
        "parameters": [
          {
            "name": "email",
            "in": "path",
            "required": true,
            "schema": {"type": "string"}
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    }
  }
}
```

### Tool Invocation Flow

1. **Agent Decision:** LLM determines which tool to call based on context
2. **Parameter Extraction:** Agent extracts required parameters from conversation
3. **API Call:** Watsonx Orchestrate makes HTTP request to backend API
4. **Response Processing:** Agent receives JSON response
5. **Natural Language Generation:** Agent formats response for customer

### Available Tools

| Tool Name | HTTP Method | Endpoint | Purpose |
|-----------|-------------|----------|---------|
| get_customer | GET | /customers/{email} | Verify customer identity |
| get_accounts | GET | /customers/{email}/accounts | Retrieve all accounts |
| get_account_by_type | GET | /customers/{email}/accounts/{type} | Get specific account |
| get_transactions | GET | /customers/{email}/transactions | View transaction history |
| get_transfers | GET | /customers/{email}/transfers | View transfer history |
| get_cards | GET | /customers/{email}/cards | Retrieve card details |
| update_card_status | PATCH | /cards/{card_id}/status | Freeze/unfreeze card |
| update_card_limit | PATCH | /cards/{card_id}/limit | Update spending limit |
| get_loans | GET | /customers/{email}/loans | View loan details |
| get_disputes | GET | /customers/{email}/disputes | View dispute status |

---

## 🗄️ Backend API Architecture

### Technology Stack

**Framework:** FastAPI (Python)
- High-performance async web framework
- Automatic OpenAPI documentation
- Type validation with Pydantic

**Data Layer:** CSV Files
- Simple, portable data storage
- Loaded into memory at startup
- No database drivers or connection strings required

**Deployment:** IBM Code Engine
- Serverless container platform
- Auto-scaling based on demand
- Built-in HTTPS and load balancing

### API Implementation

```python
# FastAPI application structure
app = FastAPI(
    title="Lendyr Bank API",
    description="Customer care REST API",
    version="1.0.0"
)

# Data loaded at startup
DB = {
    "customers": load("customers.csv"),
    "accounts": load("accounts.csv"),
    "cards": load("cards.csv"),
    "transactions": load("transactions.csv"),
    "transfers": load("transfers.csv"),
    "loans": load("loans.csv"),
    "disputes": load("disputes.csv"),
}

# Example endpoint
@app.get("/customers/{email}/loans")
def get_loans(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(404, "Customer not found")
    # Filter loans for this customer
    return [loan for loan in DB["loans"] 
            if loan["customer_id"] == cid]
```

### Data Model

**Customers:**
- customer_id, first_name, last_name, email, phone
- date_of_birth, ssn_last4, address, city, state, zip
- created_at, kyc_status

**Accounts:**
- account_id, customer_id, account_number, account_type
- status, balance, credit_limit, interest_rate
- opened_at, currency

**Cards:**
- card_id, account_id, customer_id, card_number
- card_type, network, expiry_date, status
- daily_limit, issued_at

**Loans:**
- loan_id, account_id, original_amount, outstanding_balance
- monthly_payment, next_payment_date, term_months
- loan_type (auto, mortgage, personal)

**Transactions:**
- transaction_id, account_id, transaction_type, amount
- merchant_name, merchant_category, description
- status, created_at, reference_id

**Disputes:**
- dispute_id, customer_id, transaction_id, reason
- status (open, under_review, resolved, rejected)
- filed_at, resolved_at, notes

---

## 🔄 Agent Orchestration Flow

### Conversation State Management

**Context Preservation:**
- Customer email maintained across all agent handoffs
- Conversation history available to all agents
- Previous tool results accessible for reference

**Routing Logic:**
```
Customer Request
    ↓
Customer Care Agent (analyzes intent)
    ↓
Determines specialist needed
    ↓
Routes to specialist with context
    ↓
Specialist invokes tools
    ↓
Specialist returns results
    ↓
Routes back to Customer Care or next specialist
    ↓
Customer Care synthesizes final response
```

### Example Multi-Agent Flow

**Scenario:** Customer asks about loan payment with tight cash flow

```
1. Customer Care Agent
   - Receives: "I'm worried about my loan payment"
   - Action: Verifies customer identity
   - Routes to: Loan Agent with email

2. Loan Agent
   - Receives: Customer email + loan inquiry
   - Action: Calls get_loans API
   - Routes to: Account Agent (needs balance check)

3. Account Agent
   - Receives: Customer email + loan amount
   - Action: Calls get_accounts + get_transactions
   - Routes to: Card Agent (explore backup options)

4. Card Agent
   - Receives: Customer email + financial context
   - Action: Calls get_cards API
   - Routes to: Customer Care Agent (for synthesis)

5. Customer Care Agent
   - Receives: All specialist insights
   - Action: Synthesizes recommendations
   - Returns: Comprehensive solution to customer
```

---

## 🔐 Security & Compliance

### Authentication & Authorization

**API Security:**
- HTTPS encryption for all communications
- API key authentication (can be added)
- Rate limiting and throttling
- CORS configuration for web clients

**Data Privacy:**
- PII masking in logs
- Card numbers partially masked (****1234)
- SSN last 4 digits only
- Audit trail of all data access

**Agent Access Control:**
- Each agent has specific tool permissions
- Tools scoped to customer's own data
- No cross-customer data access
- Role-based access control (RBAC) ready

### Compliance Considerations

**GDPR/CCPA:**
- Customer data access logging
- Right to be forgotten (delete customer)
- Data portability (export customer data)
- Consent management ready

**Financial Regulations:**
- Audit trail of all transactions
- Dispute tracking and resolution
- Card security (freeze/unfreeze)
- Fraud detection hooks ready

---

## 📊 Monitoring & Observability

### Metrics to Track

**Agent Performance:**
- Average conversation length
- Agent handoff frequency
- Tool invocation success rate
- Response time per agent

**API Performance:**
- Request latency (p50, p95, p99)
- Error rate by endpoint
- Throughput (requests per second)
- Cache hit rate

**Business Metrics:**
- Customer satisfaction scores
- Resolution rate (first contact)
- Escalation rate to human agents
- Cost per conversation

### Logging & Debugging

**Agent Logs:**
```json
{
  "timestamp": "2026-04-10T17:00:00Z",
  "agent": "loan_agent",
  "customer_email": "brian.nguyen@email.com",
  "action": "tool_invocation",
  "tool": "get_loans",
  "parameters": {"email": "brian.nguyen@email.com"},
  "response_time_ms": 145,
  "status": "success"
}
```

**API Logs:**
```json
{
  "timestamp": "2026-04-10T17:00:00Z",
  "method": "GET",
  "path": "/customers/brian.nguyen@email.com/loans",
  "status_code": 200,
  "response_time_ms": 12,
  "user_agent": "watsonx-orchestrate/1.0"
}
```

---

## 🚀 Deployment Architecture

### IBM Code Engine Deployment

**Container Configuration:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Environment Variables:**
```bash
PORT=8080
LOG_LEVEL=info
CORS_ORIGINS=*
```

**Resource Allocation:**
- CPU: 0.5 vCPU per instance
- Memory: 1 GB per instance
- Min instances: 0 (scale to zero)
- Max instances: 10 (auto-scale)
- Concurrency: 100 requests per instance

### Scaling Characteristics

**Auto-Scaling Triggers:**
- CPU utilization > 70%
- Memory utilization > 80%
- Request queue depth > 50

**Cold Start Performance:**
- Container startup: ~2 seconds
- CSV data loading: ~500ms
- First request latency: ~2.5 seconds
- Warm request latency: ~50ms

---

## 🔧 Development & Testing

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/kourosh/lendyr.git
cd lendyr

# Start API server
cd lendyr_code_engine
pip install -r requirements.txt
uvicorn main:app --reload --port 8080

# Test API
curl http://localhost:8080/health
curl http://localhost:8080/customers/brian.nguyen@email.com
```

### Testing Strategy

**Unit Tests:**
- Individual agent instruction validation
- Tool parameter extraction
- Response formatting

**Integration Tests:**
- Agent-to-agent handoffs
- Tool invocation with mock API
- Error handling and recovery

**End-to-End Tests:**
- Complete conversation flows
- Multi-agent scenarios
- Real API integration

**Load Tests:**
- Concurrent conversations
- API throughput limits
- Agent response times under load

---

## 🎯 Extension Points

### Adding New Agents

1. Create agent YAML file
2. Define instructions and routing logic
3. Specify tools and collaborators
4. Deploy to Watsonx Orchestrate
5. Add to customer care agent's collaborators list

**Example: Adding a "Fraud Detection Agent"**
```yaml
spec_version: v1
kind: native
name: fraud_detection_agent
description: Analyzes transactions for fraud
instructions: >
  Review transaction patterns and flag suspicious activity...
tools:
  - get_transactions
  - get_cards
  - flag_suspicious_transaction
collaborators:
  - card_agent
  - disputes_agent
```

### Adding New Tools

1. Implement API endpoint
2. Add to OpenAPI specification
3. Deploy API update
4. Add tool to agent configuration
5. Update agent instructions

**Example: Adding "Transfer Money" Tool**
```json
{
  "paths": {
    "/transfers": {
      "post": {
        "operationId": "create_transfer",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "from_account": {"type": "string"},
                  "to_account": {"type": "string"},
                  "amount": {"type": "number"}
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Integrating with Real Databases

**Replace CSV with DB2:**
```python
# Instead of loading CSV files
DB = load_csv_files()

# Connect to DB2
import ibm_db
conn = ibm_db.connect(
    "DATABASE=lendyr;HOSTNAME=db2.example.com;...",
    "", ""
)

# Query database
def get_loans(email: str):
    sql = "SELECT * FROM loans WHERE customer_id = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt, (get_customer_id(email),))
    return ibm_db.fetch_assoc(stmt)
```

---

## 📈 Performance Optimization

### Caching Strategy

**Agent Response Caching:**
- Cache frequently asked questions
- TTL: 5 minutes for account data
- Invalidate on data updates

**API Response Caching:**
- Cache customer profiles (rarely change)
- Cache account balances (5-minute TTL)
- No caching for transactions (real-time)

### Database Optimization

**Indexing:**
- customer_id on all tables
- email on customers table
- created_at on transactions (for sorting)

**Query Optimization:**
- Limit transaction queries (default 10)
- Paginate large result sets
- Use database views for complex joins

---

## 🎓 Best Practices

### Agent Design

✅ **DO:**
- Keep instructions clear and concise
- Specify routing logic explicitly
- Include error handling guidance
- Test with edge cases

❌ **DON'T:**
- Make instructions too long (>500 words)
- Assume agent knowledge not in instructions
- Create circular routing loops
- Forget to handle API errors

### Tool Design

✅ **DO:**
- Follow REST API conventions
- Use standard HTTP status codes
- Provide clear error messages
- Document all parameters

❌ **DON'T:**
- Return raw database errors
- Use non-standard response formats
- Expose internal implementation details
- Skip input validation

### Security

✅ **DO:**
- Validate all inputs
- Mask sensitive data in logs
- Use HTTPS everywhere
- Implement rate limiting

❌ **DON'T:**
- Log full credit card numbers
- Return stack traces to clients
- Trust client-side validation
- Skip authentication

---

## 📚 Additional Resources

### Documentation
- Watsonx Orchestrate: https://www.ibm.com/products/watsonx-orchestrate
- IBM Code Engine: https://www.ibm.com/cloud/code-engine
- FastAPI: https://fastapi.tiangolo.com
- OpenAPI Specification: https://swagger.io/specification/

### Sample Code
- GitHub Repository: https://github.com/kourosh/lendyr
- Agent Configurations: `/agents/*.yaml`
- API Implementation: `/lendyr_code_engine/main.py`
- Tool Definitions: `/tools/lendyr_openapi.json`

### Support
- Watsonx Orchestrate Support: support@ibm.com
- Demo Questions: Contact your IBM representative