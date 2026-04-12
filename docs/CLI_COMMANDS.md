# Orchestrate ADK CLI Commands - Step by Step

## ✅ Prerequisites Verified
- API is running: https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud
- Status: {"status":"ok","service":"Lendyr Bank API"}

---

## 🚀 Step-by-Step Commands

### Step 1: Initialize Orchestrate Project (if not done)

```bash
cd /Users/kk76/Public/lendyr
orchestrate init
```

**Expected output:** Project initialized successfully

---

### Step 2: Import API Tools from OpenAPI Specification

```bash
orchestrate skills import-api \
  --file tools/lendyr_openapi.json \
  --name "Lendyr Bank API"
```

**Alternative command (if above doesn't work):**
```bash
orchestrate skills add \
  --openapi tools/lendyr_openapi.json \
  --name "Lendyr Bank API"
```

**Expected output:** Successfully imported X operations from Lendyr Bank API

**Verify tools were imported:**
```bash
orchestrate skills list
```

You should see operations like:
- get_customer_customers__email__get
- get_loans_customers__email__loans_get
- get_payment_history_customers__email__payment_history_get
- request_loan_deferral_customers__email__loans__loan_id__defer_post
- And more...

---

### Step 3: Create Agents (In Order)

#### 3.1 Create Disputes Agent
```bash
orchestrate agents create \
  --file agents/disputes_agent.yaml
```

**Verify:**
```bash
orchestrate agents list | grep disputes
```

#### 3.2 Create Account Agent
```bash
orchestrate agents create \
  --file agents/account_agent.yaml
```

#### 3.3 Create Card Agent
```bash
orchestrate agents create \
  --file agents/card_agent.yaml
```

#### 3.4 Create Loan Agent (with Deferral Capability)
```bash
orchestrate agents create \
  --file agents/loan_agent.yaml
```

#### 3.5 Create Customer Care Agent (Main Orchestrator)
```bash
orchestrate agents create \
  --file agents/lendyr_customer_care.yaml
```

**Verify all agents:**
```bash
orchestrate agents list
```

Expected output:
- lendyr_disputes_agent
- account_agent
- card_agent
- loan_agent
- lendyr_customer_care

---

### Step 4: Test Individual Agents

#### Test Loan Agent
```bash
orchestrate agents run loan_agent \
  --input "The customer email is brian.nguyen@email.com. Please show their loan details."
```

**Expected:** Should show Brian's auto loan details

#### Test Customer Care Agent
```bash
orchestrate agents run lendyr_customer_care \
  --input "Hi, I need help with my account"
```

**Expected:** Agent asks for email address

---

### Step 5: Start Interactive Demo

```bash
orchestrate agents chat lendyr_customer_care
```

**Then follow the demo script:**

**Turn 1:**
```
Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th and I'm not sure I have enough in my checking account. Can you help me figure out my options?
```

**Turn 2:**
```
brian.nguyen@email.com
```

**Turn 3:** (Wait for loan details)

**Turn 4:**
```
Actually, I'm wondering - could I defer this payment by 30 days? That would give me more breathing room.
```

**Turn 5:** (After approval is shown)
```
Yes, I understand and agree to those terms. That extra month will really help.
```

**Turn 6:**
```
No, that covers everything. Thank you so much for all your help!
```

---

## 🔍 Useful Debugging Commands

### View Agent Details
```bash
orchestrate agents get lendyr_customer_care
```

### View Agent Logs
```bash
orchestrate agents logs lendyr_customer_care
```

### View Last Conversation
```bash
orchestrate agents history lendyr_customer_care --last
```

### Test API Directly
```bash
# Test customer lookup
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com

# Test loan details
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com/loans

# Test payment history
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com/payment-history
```

---

## 🐛 Troubleshooting

### Issue: "Command not found: orchestrate"
**Solution:**
```bash
pip install ibm-watsonx-orchestrate-adk
# Or
pip3 install ibm-watsonx-orchestrate-adk
```

### Issue: "Authentication failed"
**Solution:**
```bash
# Set your API key
export IBM_CLOUD_API_KEY="your_api_key_here"

# Login
orchestrate auth login
```

### Issue: "Agent not found"
**Solution:**
```bash
# List all agents
orchestrate agents list

# Recreate if needed
orchestrate agents create --file agents/loan_agent.yaml --force
```

### Issue: "Skill not found"
**Solution:**
```bash
# List all skills
orchestrate skills list

# Re-import if needed
orchestrate skills import-api --file tools/lendyr_openapi.json --force
```

---

## 📊 Expected Demo Results

### Brian Nguyen's Profile
- Email: brian.nguyen@email.com
- Credit Score: 755 (Excellent)
- Payment History: 45 consecutive on-time payments
- Auto Loan Balance: $17,683.58
- Monthly Payment: $469.35
- Next Payment: April 13, 2026

### Deferral Approval
- Status: APPROVED ✅
- Reason: Credit score 755 (>700) + Perfect payment history
- New Payment Date: May 13, 2026
- Interest Accrued: $102.15
- New Balance: $17,785.73

---

## 🎯 Quick Command Reference

```bash
# Import tools
orchestrate skills import-api --file tools/lendyr_openapi.json --name "Lendyr Bank API"

# Create all agents
for agent in disputes_agent account_agent card_agent loan_agent lendyr_customer_care; do
  orchestrate agents create --file agents/${agent}.yaml
done

# List everything
orchestrate skills list
orchestrate agents list

# Start demo
orchestrate agents chat lendyr_customer_care
```

---

## ✅ Success Checklist

- [ ] Orchestrate ADK installed and working
- [ ] API tools imported from OpenAPI spec
- [ ] All 5 agents created successfully
- [ ] Test individual agent (loan_agent) works
- [ ] Interactive chat with customer care agent works
- [ ] Loan deferral approval flow works end-to-end

---

**You're ready to build! Start with Step 2 above. 🚀**