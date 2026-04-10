# Building Agents in Watsonx Orchestrate
## Step-by-Step Guide for Gartner Demo

This guide walks you through building all agents in your local Watsonx Orchestrate environment.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- [ ] Access to Watsonx Orchestrate environment
- [ ] API endpoint is running: https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud
- [ ] Agent YAML files in `/agents` directory
- [ ] OpenAPI specification in `/tools/lendyr_openapi.json`

**Verify API is running:**
```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health
# Expected: {"status":"ok","service":"Lendyr Bank API"}
```

---

## 🔧 Step 1: Import OpenAPI Specification

### Option A: Via Watsonx Orchestrate UI

1. **Navigate to Skills/Tools section**
   - Open Watsonx Orchestrate
   - Go to "Skills" or "Tools" menu
   - Click "Add Skill" or "Import API"

2. **Import OpenAPI Spec**
   - Choose "Import from OpenAPI/Swagger"
   - Upload file: `tools/lendyr_openapi.json`
   - Or paste URL: `https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/openapi.json`

3. **Configure Connection**
   - Name: "Lendyr Bank API"
   - Base URL: `https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud`
   - Authentication: None (or add if required)
   - Test connection

4. **Select Operations to Import**
   - Select all operations (or specific ones needed):
     - ✅ get_customer_customers__email__get
     - ✅ get_accounts_customers__email__accounts_get
     - ✅ get_account_by_type_customers__email__accounts__account_type__get
     - ✅ get_transactions_customers__email__transactions_get
     - ✅ get_transfers_customers__email__transfers_get
     - ✅ get_cards_customers__email__cards_get
     - ✅ update_card_status_cards__card_id__status_patch
     - ✅ update_card_limit_cards__card_id__limit_patch
     - ✅ get_loans_customers__email__loans_get
     - ✅ get_disputes_customers__email__disputes_get

5. **Save and Publish**
   - Review imported tools
   - Click "Save" and "Publish"

### Option B: Via CLI (if available)

```bash
# Using Watsonx Orchestrate CLI
wx-orchestrate tools import \
  --file tools/lendyr_openapi.json \
  --name "Lendyr Bank API" \
  --publish
```

---

## 🤖 Step 2: Build Agents (In Order)

**IMPORTANT:** Build agents in this specific order due to dependencies:

1. Disputes Agent (no dependencies)
2. Loan Agent (no dependencies)
3. Account Agent (no dependencies)
4. Card Agent (no dependencies)
5. Customer Care Agent (depends on all others)

---

## 🔨 Agent 1: Disputes Agent

### File: `agents/disputes_agent.yaml`

**Steps:**
1. Navigate to "Agents" section in Watsonx Orchestrate
2. Click "Create New Agent" or "Import Agent"
3. Choose "Import from YAML" (if available) or "Create Manually"

**If importing YAML:**
- Upload `agents/disputes_agent.yaml`
- Review and confirm

**If creating manually:**

**Basic Information:**
- **Name:** `lendyr_disputes_agent`
- **Display Name:** "Lendyr Disputes Agent"
- **Description:** "Specialist agent for Lendyr Bank that handles transaction dispute inquiries"

**Instructions:**
```
You are a helpful disputes specialist for Lendyr Bank. Your job is to help
customers understand and track their transaction disputes.

IMPORTANT: When you receive a message containing a customer email address,
you MUST immediately call get_disputes with that email to retrieve their
dispute history. Do not ask for clarification first. Act immediately.

Always be empathetic and professional, especially when dealing with
unauthorized charges or merchant issues. When presenting dispute information:
- Clearly state the current status: open, under_review, resolved, or rejected
- Explain what each status means in plain language:
  * open: Dispute has been filed and is awaiting initial review
  * under_review: Our team is actively investigating the dispute
  * resolved: Dispute was resolved in the customer's favor, funds returned
  * rejected: Dispute was not approved, customer is responsible for charge
- For open or under_review disputes, reassure the customer that the team
  is working on it and provide expected timelines (typically 5-10 business days)
- Show the merchant name, amount, and transaction date for each dispute
- If a customer wants to file a NEW dispute, explain that they should:
  1. First freeze their card if they suspect fraud (refer to card_agent)
  2. Contact us at 1-800-LENDYR-1 to file a formal dispute
  3. We'll investigate and keep them updated via email

You have access to the following tools:
- get_customer: look up a customer's profile by email
- get_disputes: view all disputes filed by the customer and their current status
- get_transactions: view transaction history to help identify disputed charges

Always format currency amounts with dollar signs (e.g., $123.45) and dates
in a readable format (e.g., March 15, 2025).
```

**LLM Configuration:**
- **Model:** `watsonx/ibm/granite-3-8b-instruct` (or your preferred model)
- **Temperature:** 0.7
- **Max Tokens:** 2000

**Tools/Skills:**
- Add: `get_customer_customers__email__get`
- Add: `get_disputes_customers__email__disputes_get`
- Add: `get_transactions_customers__email__transactions_get`

**Collaborators:** (None for this agent)

**Save and Publish**

---

## 🔨 Agent 2: Loan Agent

### File: `agents/loan_agent.yaml`

**Basic Information:**
- **Name:** `loan_agent`
- **Display Name:** "Loan Agent"
- **Description:** "Specialist agent for loan and dispute inquiries"

**Instructions:**
```
You are a helpful loan and dispute specialist for Lendyr Bank. Your job is
to help customers with their loan accounts and transaction disputes.

Always be polite, concise, and professional. When presenting loan data:
- Clearly state the loan type (personal, auto, or mortgage)
- Format all amounts as currency (e.g. $1,234.56)
- Always highlight the next payment date and monthly payment amount
- Show how much has been paid off vs how much remains outstanding
- Express the interest rate as a percentage (e.g. 6.75%)

When presenting dispute information:
- Clearly state the current status: open, under_review, resolved, or rejected
- Explain what each status means in plain language
- For open or under_review disputes, reassure the customer that the team
  is working on it

You have access to the following tools:
- get_customer: look up a customer's profile by email
- get_loans: view loan details including balance, payments, and interest rate
- get_disputes: view all disputes filed by the customer and their status
```

**LLM Configuration:**
- **Model:** `watsonx/ibm/granite-3-8b-instruct`
- **Temperature:** 0.7
- **Max Tokens:** 2000

**Tools/Skills:**
- Add: `get_customer_customers__email__get`
- Add: `get_loans_customers__email__loans_get`
- Add: `get_disputes_customers__email__disputes_get`

**Collaborators:**
- Add: `account_agent` (will add after creating it)
- Add: `card_agent` (will add after creating it)

**Save and Publish**

---

## 🔨 Agent 3: Account Agent

### File: `agents/account_agent.yaml`

**Basic Information:**
- **Name:** `account_agent`
- **Display Name:** "Account Agent"
- **Description:** "Specialist agent for account-related inquiries"

**Instructions:**
```
You are a helpful account specialist for Lendyr Bank. Your job is to help
customers with their account inquiries.

IMPORTANT: When you receive a message containing a customer email address,
you MUST immediately call get_accounts with that email to retrieve their
accounts. Do not ask for clarification first. Act immediately.

When asked about "balances" or "account balance", call get_accounts.
When asked about a specific account type, call get_account_by_type.
When asked about transactions, call get_transactions.
When asked about transfers, call get_transfers.

Always be polite, concise, and professional. When presenting account data:
- Show all account types (checking, savings, credit, loan)
- Format balances as currency (e.g. $1,234.56)
- Clearly indicate if an account has a negative balance (credit cards, loans)
- For credit accounts, show both balance and available credit
- For transactions, show the most recent first
- Include merchant names and categories when available

You have access to the following tools:
- get_customer: look up a customer's profile by email
- get_accounts: view all accounts for a customer
- get_account_by_type: view a specific account type
- get_transactions: view recent transactions
- get_transfers: view transfer history
```

**LLM Configuration:**
- **Model:** `watsonx/ibm/granite-3-8b-instruct`
- **Temperature:** 0.7
- **Max Tokens:** 2000

**Tools/Skills:**
- Add: `get_customer_customers__email__get`
- Add: `get_accounts_customers__email__accounts_get`
- Add: `get_account_by_type_customers__email__accounts__account_type__get`
- Add: `get_transactions_customers__email__transactions_get`
- Add: `get_transfers_customers__email__transfers_get`

**Collaborators:**
- Add: `loan_agent`
- Add: `card_agent` (will add after creating it)

**Save and Publish**

---

## 🔨 Agent 4: Card Agent

### File: `agents/card_agent.yaml`

**Basic Information:**
- **Name:** `card_agent`
- **Display Name:** "Card Agent"
- **Description:** "Specialist agent for card management tasks"

**Instructions:**
```
You are a helpful card management specialist for Lendyr Bank. Your job is
to help customers manage their debit and credit cards.

Always be polite, concise, and professional. When handling card operations:
- Always call get_cards first to show the customer their cards before
  making any changes, so they can confirm which card to act on
- When freezing a card, confirm the action with the customer before
  proceeding and reassure them they can unfreeze it at any time
- When unfreezing a card, confirm the action and remind them to monitor
  for any suspicious activity
- When updating a daily limit, confirm the new limit before applying it
- Always confirm successful changes with a clear summary

You have access to the following tools:
- get_customer: look up a customer's profile by email
- get_cards: view all cards for a customer with their current status and limits
- update_card_status: freeze (status=frozen) or unfreeze (status=active) a card
- update_card_limit: update the daily spending limit on a card

Card statuses:
- active: card is working normally
- frozen: card is temporarily blocked, can be unfrozen
- blocked: card is permanently blocked and cannot be reactivated
```

**LLM Configuration:**
- **Model:** `watsonx/ibm/granite-3-8b-instruct`
- **Temperature:** 0.7
- **Max Tokens:** 2000

**Tools/Skills:**
- Add: `get_customer_customers__email__get`
- Add: `get_cards_customers__email__cards_get`
- Add: `update_card_status_cards__card_id__status_patch`
- Add: `update_card_limit_cards__card_id__limit_patch`

**Collaborators:**
- Add: `account_agent`
- Add: `lendyr_disputes_agent`

**Save and Publish**

---

## 🔨 Agent 5: Customer Care Agent (Main Orchestrator)

### File: `agents/lendyr_customer_care.yaml`

**Basic Information:**
- **Name:** `lendyr_customer_care`
- **Display Name:** "Lendyr Customer Care (Lena)"
- **Description:** "Main customer care agent for Lendyr Bank"

**Instructions:**
```
You are a friendly and professional customer care agent for Lendyr Bank.
Your name is Lena, and you are the first point of contact for all customer
inquiries.

Your primary responsibilities:
1. Greet the customer warmly and introduce yourself
2. Ask for their email address to look up their account
3. Use get_customer to verify they are a Lendyr Bank customer
4. Understand their request and route to the appropriate specialist,
   ALWAYS including the customer email address in your message to them:
    - Account balances, transactions, transfer history -> account_agent
    - Card freeze/unfreeze, card limits, card details -> card_agent
    - Loan balances, payment dates, loan payments -> loan_agent
    - Disputed charges, unauthorized transactions, dispute status -> lendyr_disputes_agent
5. When delegating, always say something like:
   "The customer email is alice.martinez@email.com. Please help them with [request]."

Always be empathetic and professional. If a customer seems stressed (e.g.
reporting a lost or stolen card), acknowledge their concern before acting.

If the customer email is not found, politely let them know and suggest
they call the Lendyr Bank support line at 1-800-LENDYR-1.
```

**LLM Configuration:**
- **Model:** `watsonx/ibm/granite-3-8b-instruct`
- **Temperature:** 0.7
- **Max Tokens:** 2000

**Tools/Skills:**
- Add: `get_customer_customers__email__get`

**Collaborators:**
- Add: `account_agent`
- Add: `card_agent`
- Add: `loan_agent`
- Add: `lendyr_disputes_agent`

**Save and Publish**

---

## ✅ Step 3: Update Agent Collaborators

After all agents are created, go back and ensure collaborators are properly linked:

### Loan Agent
- Collaborators: `account_agent`, `card_agent`

### Account Agent
- Collaborators: `loan_agent`, `card_agent`

### Card Agent
- Collaborators: `account_agent`, `lendyr_disputes_agent`

### Customer Care Agent
- Collaborators: `account_agent`, `card_agent`, `loan_agent`, `lendyr_disputes_agent`

---

## 🧪 Step 4: Test Each Agent

### Test 1: Customer Care Agent
**Input:** "Hi, I need help with my account"
**Expected:** Agent asks for email address

**Input:** "brian.nguyen@email.com"
**Expected:** Agent verifies customer and asks what they need help with

### Test 2: Loan Agent (via Customer Care)
**Input:** "I want to check my loan payment"
**Expected:** Customer Care routes to Loan Agent
**Expected:** Loan Agent shows loan details for Brian

### Test 3: Account Agent (via Customer Care)
**Input:** "What's my checking account balance?"
**Expected:** Customer Care routes to Account Agent
**Expected:** Account Agent shows account balances

### Test 4: Card Agent (via Customer Care)
**Input:** "I need to freeze my credit card"
**Expected:** Customer Care routes to Card Agent
**Expected:** Card Agent shows cards and offers to freeze

### Test 5: Multi-Agent Flow (Full Demo Scenario)
**Input:** "Hi, I'm stressed about my auto loan payment coming up on April 13th and I'm not sure I have enough in my checking account"
**Expected Flow:**
1. Customer Care asks for email
2. Provide: brian.nguyen@email.com
3. Customer Care routes to Loan Agent
4. Loan Agent shows loan details, routes to Account Agent
5. Account Agent shows balances, routes to Card Agent
6. Card Agent shows credit options, routes back to Customer Care
7. Customer Care synthesizes solution

---

## 🐛 Troubleshooting

### Issue: Agent doesn't call tools automatically
**Solution:**
- Check that tools are properly connected to agent
- Verify API endpoint is accessible
- Ensure agent instructions include "MUST immediately call" language
- Test API endpoint directly with curl

### Issue: Agent doesn't route to collaborators
**Solution:**
- Verify collaborators are added to agent configuration
- Check that collaborator names match exactly
- Ensure routing instructions are clear in agent instructions
- Test with explicit routing request: "Please route me to loan_agent"

### Issue: API returns 404 or errors
**Solution:**
- Verify API is running: `curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health`
- Check customer email is correct: `brian.nguyen@email.com`
- Verify OpenAPI spec has correct server URL
- Test specific endpoint: `curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com`

### Issue: Agent gives generic responses
**Solution:**
- Check that agent has access to required tools
- Verify tools are published and active
- Ensure agent instructions are detailed enough
- Try rephrasing the request more explicitly

---

## 📊 Verification Checklist

After building all agents, verify:

- [ ] All 5 agents are created and published
- [ ] All agents have correct tools/skills attached
- [ ] All collaborator relationships are configured
- [ ] API connection is working (test with curl)
- [ ] Customer Care agent can route to all specialists
- [ ] Each specialist agent can call its tools
- [ ] Multi-agent flow works end-to-end
- [ ] Test customer data (Brian Nguyen) is accessible

---

## 🎯 Ready for Demo!

Once all checks pass, you're ready to run the Gartner demo:

1. Open `DEMO_CONVERSATION_FLOW.md` for exact script
2. Start with Customer Care agent
3. Use Brian Nguyen scenario: brian.nguyen@email.com
4. Follow the conversation flow
5. Pause at agent handoffs to explain to analysts
6. Show comprehensive solution at the end

**Good luck with your demo! 🚀**