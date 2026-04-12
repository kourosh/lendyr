# Local Orchestrate ADK Setup Guide
## Building AI Agents for Lendyr Customer Care Demo

This guide walks you through setting up and building AI agents locally using the IBM watsonx Orchestrate Agent Development Kit (ADK).

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed
- **IBM watsonx Orchestrate ADK** installed
- **Access to watsonx.ai** (for LLM models)
- **API endpoint running**: https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud
- **IBM Cloud API Key** with access to watsonx.ai

---

## 🔧 Step 1: Install Orchestrate ADK

### Install via pip

```bash
pip install ibm-watsonx-orchestrate-adk
```

### Verify Installation

```bash
orchestrate --version
```

---

## 🔑 Step 2: Configure Authentication

### Set up IBM Cloud credentials

Create a `.env` file in your project root:

```bash
# IBM Cloud Authentication
IBM_CLOUD_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here

# Optional: Specify region
WATSONX_REGION=us-south
```

### Or export environment variables:

```bash
export IBM_CLOUD_API_KEY="your_api_key_here"
export WATSONX_PROJECT_ID="your_project_id_here"
```

---

## 📁 Step 3: Project Structure

Your project should have this structure:

```
lendyr/
├── agents/
│   ├── lendyr_customer_care.yaml
│   ├── loan_agent.yaml
│   ├── account_agent.yaml
│   ├── card_agent.yaml
│   └── disputes_agent.yaml
├── tools/
│   └── lendyr_openapi.json
├── docs/
│   ├── DEMO_CONVERSATION_FLOW_V2.md
│   └── LOCAL_ADK_SETUP.md
└── .env
```

---

## 🛠️ Step 4: Initialize Orchestrate Project

### Create a new Orchestrate project

```bash
cd /Users/kk76/Public/lendyr
orchestrate init
```

This will create the necessary configuration files.

---

## 🔌 Step 5: Import API Tools

### Import the Lendyr Bank API

```bash
orchestrate tools import \
  --file tools/lendyr_openapi.json \
  --name "Lendyr Bank API"
```

### Verify tools were imported

```bash
orchestrate tools list
```

You should see all the Lendyr Bank API operations:
- `get_customer_customers__email__get`
- `get_accounts_customers__email__accounts_get`
- `get_loans_customers__email__loans_get`
- `get_payment_history_customers__email__payment_history_get`
- `request_loan_deferral_customers__email__loans__loan_id__defer_post`
- And more...

---

## 🤖 Step 6: Build Agents (In Order)

**IMPORTANT:** Build agents in this specific order due to dependencies:

### 1. Build Disputes Agent

```bash
orchestrate agents create --file agents/disputes_agent.yaml
```

### 2. Build Account Agent

```bash
orchestrate agents create --file agents/account_agent.yaml
```

### 3. Build Card Agent

```bash
orchestrate agents create --file agents/card_agent.yaml
```

### 4. Build Loan Agent (with Deferral Capability)

```bash
orchestrate agents create --file agents/loan_agent.yaml
```

### 5. Build Customer Care Agent (Main Orchestrator)

```bash
orchestrate agents create --file agents/lendyr_customer_care.yaml
```

### Verify all agents are created

```bash
orchestrate agents list
```

---

## 🧪 Step 7: Test Individual Agents

### Test Loan Agent

```bash
orchestrate agents test loan_agent \
  --message "The customer email is brian.nguyen@email.com. Please show their loan details."
```

Expected output: Loan details for Brian Nguyen including auto loan information.

### Test Customer Care Agent

```bash
orchestrate agents test lendyr_customer_care \
  --message "Hi, I need help with my account"
```

Expected output: Agent asks for email address.

---

## 🎯 Step 8: Run Full Demo Conversation

### Start interactive session with Customer Care Agent

```bash
orchestrate agents chat lendyr_customer_care
```

### Follow the demo script from DEMO_CONVERSATION_FLOW_V2.md:

**Turn 1:**
```
Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th 
and I'm not sure I have enough in my checking account. Can you help me 
figure out my options?
```

**Turn 2:**
```
brian.nguyen@email.com
```

**Turn 3:** (Wait for agent to route to loan_agent and show loan details)

**Turn 4:**
```
Actually, I'm wondering - could I defer this payment by 30 days? That would 
give me more breathing room.
```

**Turn 5:** (Agent evaluates credit and approves/denies)
```
Yes, I understand and agree to those terms. That extra month will really help.
```

---

## 🔍 Step 9: Verify Loan Deferral Feature

### Test the autonomous decision-making

The loan agent should:

1. ✅ Call `get_customer` to retrieve credit score (755)
2. ✅ Call `get_payment_history` to check payment record (45 on-time payments)
3. ✅ Evaluate eligibility:
   - Credit score >= 700? ✅ Yes (755)
   - Missed payments = 0? ✅ Yes
4. ✅ Call `request_loan_deferral` API
5. ✅ Present approval with:
   - New payment date (May 13, 2026)
   - Interest accrued ($102.15)
   - New balance ($17,785.73)
   - Terms and conditions
6. ✅ Require customer agreement

### Test denial scenario

To test denial, you would need a customer with:
- Credit score < 700, OR
- Missed payments > 0

---

## 📊 Step 10: Monitor Agent Behavior

### View agent logs

```bash
orchestrate agents logs lendyr_customer_care
```

### View tool calls

```bash
orchestrate agents trace lendyr_customer_care --last-session
```

This shows all API calls made during the conversation.

---

## 🐛 Troubleshooting

### Issue: "Agent not found"

**Solution:**
```bash
# List all agents
orchestrate agents list

# Recreate agent if needed
orchestrate agents create --file agents/loan_agent.yaml --force
```

### Issue: "Tool not found"

**Solution:**
```bash
# Re-import tools
orchestrate tools import --file tools/lendyr_openapi.json --force

# Verify tools
orchestrate tools list | grep lendyr
```

### Issue: "API connection failed"

**Solution:**
```bash
# Test API endpoint
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health

# Expected: {"status":"ok","service":"Lendyr Bank API"}
```

### Issue: "Authentication failed"

**Solution:**
```bash
# Verify API key is set
echo $IBM_CLOUD_API_KEY

# Re-authenticate
orchestrate auth login --api-key $IBM_CLOUD_API_KEY
```

### Issue: "Agent doesn't call tools"

**Solution:**
- Check that tools are properly connected to agent
- Verify agent instructions include "MUST immediately call" language
- Ensure LLM model has tool-calling capability (granite-3-8b-instruct does)

---

## 🎬 Demo Tips

### For Gartner Analysts

1. **Start with the problem**: Customer is stressed about upcoming payment
2. **Show the routing**: Customer Care → Loan Agent
3. **Highlight autonomous decision**: Agent evaluates credit in real-time
4. **Emphasize transparency**: All terms and impacts are explained
5. **Show compliance**: Customer must explicitly agree to terms

### Key Talking Points

- **"This is autonomous AI making real business decisions"**
  - Not just answering questions
  - Evaluating creditworthiness
  - Approving financial transactions

- **"Risk management is built in"**
  - Credit score threshold (700)
  - Payment history check (no missed payments)
  - Configurable business rules

- **"Full transparency and compliance"**
  - Decision reasoning explained
  - Financial impact calculated
  - Customer agreement required
  - Audit trail maintained

---

## 📈 Advanced: Customizing Agents

### Modify agent instructions

Edit the YAML file and update:

```bash
orchestrate agents update --file agents/loan_agent.yaml
```

### Change LLM model

In the agent YAML:
```yaml
llm: watsonx/ibm/granite-3-8b-instruct
# Or use a different model:
# llm: watsonx/meta-llama/llama-3-70b-instruct
```

### Adjust business rules

Modify the API backend (`lendyr_code_engine/main.py`):
```python
# Change credit score threshold
if credit_score >= 700 and missed_payments == 0:
    # Change to 650 for more lenient approval
```

---

## 🚀 Next Steps

1. ✅ Complete local setup
2. ✅ Test all agents individually
3. ✅ Run full demo conversation
4. ✅ Verify loan deferral feature
5. 📝 Practice demo script
6. 🎯 Prepare for Gartner presentation

---

## 📚 Additional Resources

- [Orchestrate ADK Documentation](https://www.ibm.com/docs/en/watsonx/orchestrate)
- [Demo Conversation Flow](./DEMO_CONVERSATION_FLOW_V2.md)
- [Build Agents Guide](./BUILD_AGENTS.md)
- [Technical Architecture](./TECHNICAL_ARCHITECTURE.md)

---

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review agent logs: `orchestrate agents logs <agent_name>`
3. Verify API is running: `curl <api_endpoint>/health`
4. Check authentication: `orchestrate auth status`

---

**Ready to build! 🎉**

Follow the steps above to set up your local Orchestrate ADK environment and build the Lendyr customer care agents for the Gartner demo.