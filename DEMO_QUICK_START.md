# Quick Start Guide: Gartner Demo Setup

## Prerequisites
- Watsonx Orchestrate environment configured
- Access to Lendyr API: https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud

## Step 1: Verify API is Running

```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health
```

Expected response:
```json
{"status": "ok", "service": "Lendyr Bank API"}
```

## Step 2: Verify Test Customer Data

```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com
```

Expected: Customer profile for Brian Nguyen

## Step 3: Deploy Agents to Watsonx Orchestrate

Deploy these agents in order:

1. **disputes_agent** (`agents/disputes_agent.yaml`)
2. **loan_agent** (`agents/loan_agent.yaml`)
3. **account_agent** (`agents/account_agent.yaml`)
4. **card_agent** (`agents/card_agent.yaml`)
5. **lendyr_customer_care** (`agents/lendyr_customer_care.yaml`) - Main entry point

## Step 4: Deploy Tools

Ensure all tools are configured with the correct API endpoint:
- Base URL: `https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud`
- Tools are defined in the OpenAPI spec: `tools/lendyr_openapi.json`

## Step 5: Test the Scenario

### Opening Line (as customer):
```
Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th 
and I'm not sure I have enough in my checking account. Can you help me 
figure out my options?
```

### Expected Flow:
1. **Customer Care Agent** greets and asks for email
2. You provide: `brian.nguyen@email.com`
3. **Customer Care** verifies customer and routes to **Loan Agent**
4. **Loan Agent** shows loan details ($469.35 due April 13th)
5. **Loan Agent** routes to **Account Agent**
6. **Account Agent** shows balances and transactions
7. **Account Agent** routes to **Card Agent**
8. **Card Agent** shows credit card options
9. **Card Agent** routes back to **Customer Care**
10. **Customer Care** summarizes options and asks for preference

### Key Customer Data (Brian Nguyen):
- **Email:** brian.nguyen@email.com
- **Checking:** $1,247.80
- **Savings:** $3,200.50
- **Credit Card:** $887.11 used of $5,000 limit
- **Auto Loan:** $469.35 payment due April 13th

## Troubleshooting

### Agent doesn't call tools automatically
- Check agent instructions include "MUST immediately call" language
- Verify tools are properly connected in Watsonx Orchestrate
- Ensure API endpoint is accessible

### Agent doesn't route to next specialist
- Check collaborators list in agent YAML
- Verify agent instructions include routing logic
- Make sure customer email is passed in handoff message

### API returns 404
- Verify customer email is correct: `brian.nguyen@email.com`
- Check API endpoint is running
- Confirm data is loaded in CSV files

## Demo Tips

1. **Pause at handoffs** - Explain which agent is taking over and why
2. **Show tool calls** - Point out when agents call APIs in real-time
3. **Highlight context** - Note how customer email flows through all agents
4. **Emphasize autonomy** - Agents decide routing, no manual intervention
5. **Be ready to show code** - Have agent YAML files ready to display

## Alternative Test Scenarios

### Scenario 2: Card Freeze (Existing)
Customer: "I think I lost my credit card. Can you help me freeze it?"
Email: `alice.martinez@email.com`

### Scenario 3: Account Balance Check
Customer: "Can you tell me my checking account balance?"
Email: `alice.martinez@email.com`

### Scenario 4: Loan Information
Customer: "When is my next auto loan payment due?"
Email: `brian.nguyen@email.com`

## Success Criteria

✅ Customer Care agent greets and identifies customer
✅ Loan Agent retrieves and presents loan details
✅ Account Agent shows comprehensive financial picture
✅ Card Agent explains credit options
✅ Customer Care agent synthesizes solution
✅ All handoffs are smooth with context maintained
✅ No manual intervention required

## Post-Demo: Show the Architecture

If analysts want technical details, show:

1. **Agent YAML files** - Simple configuration
2. **OpenAPI spec** - Standard REST API integration  
3. **Tool definitions** - How agents connect to APIs
4. **CSV data files** - Simple data layer (can be replaced with real DB2)

## Contact

For issues during demo setup, check:
- Watsonx Orchestrate documentation
- API endpoint health: `/health`
- Agent deployment logs in Watsonx Orchestrate console