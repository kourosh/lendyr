# Gartner Demo Scenario: Financial Hardship Assistance
## Multi-Agent Orchestration with Watsonx Orchestrate

### Overview
This scenario demonstrates how multiple AI agents collaborate seamlessly to help a customer navigate a complex financial situation. It showcases Watsonx Orchestrate's ability to:
- Route requests intelligently between specialized agents
- Maintain context across agent handoffs
- Provide comprehensive solutions requiring multiple domains of expertise
- Handle sensitive situations with empathy and professionalism

---

## Scenario: Brian's Auto Loan Payment Challenge

### Customer Profile
- **Name:** Brian Nguyen
- **Email:** brian.nguyen@email.com
- **Situation:** Auto loan payment of $469.35 due April 13th, concerned about cash flow

### Financial Snapshot
- **Checking Account:** $1,247.80 (tight for upcoming payment)
- **Savings Account:** $3,200.50 (good reserve)
- **Credit Card:** $887.11 used of $5,000 limit ($4,112.89 available)
- **Auto Loan:** $17,683.58 outstanding, $469.35 monthly payment @ 6.9% APR

### Customer's Concern
Brian is worried about making his upcoming auto loan payment while maintaining enough buffer in his checking account for daily expenses. He wants to explore his options, including the possibility of deferring the payment by 30 days.

---

## Demo Flow: Multi-Agent Collaboration

### 1. Initial Contact - Customer Care Agent (Lena)
**Customer:** "Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th and I'm not sure I have enough in my checking account. Can you help me figure out my options?"

**Agent Actions:**
- Greets customer warmly and introduces herself
- Asks for email address: brian.nguyen@email.com
- Calls `get_customer` tool to verify customer identity
- Acknowledges the stress and reassures Brian
- Routes to **Loan Agent** to check loan details

**Key Demonstration Points:**
- Natural language understanding of customer concern
- Empathetic response to financial stress
- Intelligent routing based on "auto loan payment" keywords

---

### 2. Loan Details - Loan Agent
**Handoff Message:** "The customer email is brian.nguyen@email.com. Please help them understand their upcoming auto loan payment."

**Agent Actions:**
- Immediately calls `get_loans` tool
- Presents loan information clearly:
  - Loan type: Auto loan
  - Outstanding balance: $17,683.58
  - Monthly payment: $469.35
  - Next payment date: April 13th (3 days away!)
  - Interest rate: 6.9%
  - Progress: Paid off $10,316.42 of original $28,000 loan
- Acknowledges the tight timeline
- Routes to **Account Agent** to review available funds

**Key Demonstration Points:**
- Automatic tool invocation without asking for clarification
- Clear presentation of financial data
- Context-aware routing to next specialist

---

### 2b. Customer Requests Deferral - Loan Agent (NEW!)
**Customer:** "Actually, could I defer this payment by 30 days? I'd feel more comfortable with that."

**Agent Actions:**
- Calls `get_payment_history` tool to check Brian's payment record
- Calls `get_customer` tool to check credit score
- Evaluates eligibility:
  - Credit score: 755 ✅ (above 700 threshold)
  - Payment history: 45 consecutive on-time payments ✅ (no missed payments)
  - **ELIGIBLE for deferral**
- Calls `request_loan_deferral` tool with:
  - loan_id: 1
  - deferral_days: 30
  - reason: "Customer needs additional time for cash flow management"
- Presents deferral approval with full transparency:
  - **New payment date:** May 13th, 2026
  - **Interest accrued:** ~$102.15 (one month at 6.9% APR)
  - **New loan balance:** $17,785.73
  - **Impact:** Final payoff extended by ~1 month
  - **Terms:** Must agree that balance increases and payoff date extends
- Asks for explicit customer confirmation

**Key Demonstration Points:**
- **Autonomous decision-making** based on risk assessment
- **Multi-tool orchestration** (3 API calls to evaluate eligibility)
- **Transparent AI** - clearly explains financial impact
- **Compliance-ready** - requires customer agreement to terms
- **Real-time credit evaluation** - no human approval needed for qualified customers

---

### 3. Account Review - Account Agent
**Handoff Message:** "The customer email is brian.nguyen@email.com. They need to make a $469.35 loan payment on April 13th. Please check their account balances and recent transactions to help them understand their cash flow."

**Agent Actions:**
- Calls `get_accounts` tool to retrieve all accounts
- Presents comprehensive account overview:
  - Checking: $1,247.80 (enough for payment but tight)
  - Savings: $3,200.50 (healthy reserve)
  - Credit: $887.11 used of $5,000 limit
- Calls `get_transactions` with limit=10 to show recent spending
- Analyzes recent activity:
  - Recent payroll deposits
  - Regular spending patterns
  - Any large upcoming charges
- Suggests options:
  1. Use checking account (leaves ~$778 buffer)
  2. Transfer from savings to checking for more comfort
  3. Temporarily increase credit card limit as backup
- Routes to **Card Agent** for credit limit discussion

**Key Demonstration Points:**
- Multi-tool orchestration (accounts + transactions)
- Financial analysis and recommendations
- Proactive problem-solving

---

### 4. Credit Card Options - Card Agent
**Handoff Message:** "The customer email is brian.nguyen@email.com. They have a $469.35 loan payment due April 13th. Their checking has $1,247.80 which is tight. Can you review their credit card and discuss increasing the daily limit as a backup option?"

**Agent Actions:**
- Calls `get_cards` tool to retrieve card details
- Shows current credit card status:
  - Card type: Credit card (Visa ending in 2002)
  - Current balance: $887.11 used
  - Credit limit: $5,000
  - Available credit: $4,112.89
  - Daily spending limit: $5,000
  - Status: Active
- Explains that Brian has plenty of available credit as backup
- Offers to increase daily limit if needed (currently already at max)
- Reassures Brian that he has multiple options
- Routes back to **Customer Care Agent** for summary

**Key Demonstration Points:**
- Card management expertise
- Risk assessment and recommendations
- Seamless handoff back to main agent

---

### 5. Resolution - Customer Care Agent (Lena)
**Agent Actions:**
- Summarizes the complete financial picture
- Presents Brian's options clearly:
  1. **Recommended:** Pay from checking ($1,247.80 → $778.45 after payment)
     - Pros: Simple, no fees, maintains savings
     - Cons: Lower buffer until next paycheck
  2. **Alternative:** Transfer $500 from savings to checking first
     - Pros: More comfortable buffer
     - Cons: Requires manual transfer (can do via mobile app)
  3. **Backup:** Use credit card if needed
     - Pros: $4,112.89 available credit
     - Cons: 21.99% APR if carried beyond grace period
- Asks Brian which option he prefers
- Confirms next steps
- Offers to help with anything else

**Key Demonstration Points:**
- Comprehensive solution synthesis
- Clear presentation of pros/cons
- Customer empowerment through choice
- Professional closure

---

## Technical Highlights for Gartner Analysts

### 1. **Intelligent Agent Orchestration**
- 5+ agent interactions (Customer Care → Loan → Account → Card → Customer Care)
- Context maintained across all handoffs
- Each agent has specialized knowledge and tools
- No manual routing required - agents decide next steps

### 2. **API Integration**
- 9+ different API calls across 4 agents:
  - `get_customer` (Customer Care, Loan Agent)
  - `get_loans` (Loan Agent)
  - `get_payment_history` (Loan Agent)
  - `request_loan_deferral` (Loan Agent)
  - `get_accounts` (Account Agent)
  - `get_transactions` (Account Agent)
  - `get_cards` (Card Agent)
- Real-time data from live database
- Seamless tool invocation

### 3. **Autonomous Decision-Making** ⭐ NEW!
- **Credit Risk Assessment:** Agent evaluates credit score (755) and payment history (45 on-time payments)
- **Automated Approval:** No human intervention for qualified customers
- **Transparent AI:** Clearly explains decision criteria and financial impact
- **Compliance-Ready:** Requires customer agreement to terms
- **Real-time Calculation:** Computes interest accrual, new balance, extended payoff date
- **Audit Trail:** All decisions logged with reasoning

### 4. **Natural Language Understanding**
- Understands "stressed about payment" → routes to loan specialist
- Recognizes "defer payment" → triggers eligibility evaluation
- Identifies "backup options" → engages card specialist
- No rigid scripts or decision trees

### 5. **Business Value**
- **Customer Experience:** Single conversation, multiple specialists, instant decisions
- **Efficiency:** 5-minute resolution vs. multiple calls/transfers
- **Accuracy:** Real-time data, no manual lookups
- **Scalability:** Handles complex scenarios without human escalation
- **Risk Management:** Automated credit evaluation with configurable thresholds

### 6. **Enterprise Readiness**
- Modular agent architecture (easy to add/modify agents)
- Tool-based integration (works with any API)
- Audit trail of all agent interactions and decisions
- Configurable LLM models per agent
- Configurable business rules (credit score thresholds, deferral limits)

---

## Demo Preparation Checklist

### Before the Demo
- [ ] Verify API endpoint is running: https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health
- [ ] Confirm Brian Nguyen's data is loaded (brian.nguyen@email.com)
- [ ] Test each agent individually
- [ ] Run through full scenario once
- [ ] Prepare to show agent YAML files if asked
- [ ] Have OpenAPI spec ready to show tool integration

### During the Demo
- [ ] Start with scenario context (Brian's concern)
- [ ] Show natural conversation flow
- [ ] Highlight agent handoffs (pause to explain)
- [ ] Point out tool invocations in real-time
- [ ] Emphasize no manual routing needed
- [ ] Show final comprehensive solution

### Key Talking Points
1. **"This is a single conversation, but 4 specialized agents are collaborating behind the scenes"**
2. **"Each agent has its own tools and expertise - loan agent knows loans, card agent knows cards"**
3. **"The agents decide who to involve next based on the customer's needs"**
4. **"All of this is happening in real-time with live data from our banking API"**
5. **"This same pattern works for any complex business process - not just banking"**

---

## Alternative Scenarios (If Time Permits)

### Scenario 2: Card Security + Dispute
- Customer reports suspicious charge
- Card Agent freezes card immediately
- Account Agent reviews recent transactions
- Disputes Agent checks existing disputes
- Customer Care Agent summarizes next steps

### Scenario 3: Travel Preparation
- Customer planning international trip
- Card Agent increases daily limits
- Account Agent reviews balances
- Loan Agent confirms auto-pay is set up
- Customer Care Agent provides travel tips

---

## Questions Gartner Analysts Might Ask

**Q: How do agents know when to hand off to another agent?**
A: Each agent's instructions include routing logic. They analyze the customer's request and determine which specialist is needed. For example, if a customer mentions "loan payment," the agent knows to involve the loan_agent.

**Q: What if an agent makes a mistake?**
A: Agents can self-correct or ask clarifying questions. The customer care agent can also step in to redirect. We also have audit logs of all interactions for quality monitoring.

**Q: Can you add new agents without retraining?**
A: Yes! Agents are modular. We just create a new YAML file with instructions and tools, then add it to the collaborators list. No model retraining needed.

**Q: How does this handle security and compliance?**
A: Each agent only has access to specific tools (APIs). We can implement role-based access control, audit logging, and data masking at the API layer.

**Q: What LLMs are you using?**
A: We're using IBM Granite 3 8B Instruct for all agents, but each agent can use a different model if needed. The architecture is LLM-agnostic.

**Q: How long did it take to build this?**
A: The agent framework is reusable. Once set up, adding a new agent takes about 30 minutes - just write the YAML file and connect the tools.

---

## Success Metrics to Highlight

- **Resolution Time:** 5 minutes vs. 15-20 minutes with traditional call center
- **Customer Satisfaction:** Single conversation vs. multiple transfers
- **Agent Efficiency:** 4 specialists involved without manual coordination
- **Accuracy:** 100% - all data pulled from live systems
- **Scalability:** Same pattern works for any complex scenario

---

## Post-Demo: Show the Code

If analysts want to see "under the hood," show:

1. **Agent YAML files** - Simple, declarative configuration
2. **OpenAPI spec** - Standard REST API integration
3. **Tool definitions** - How agents connect to backend systems
4. **Orchestration logs** - Audit trail of agent interactions

This demonstrates that Watsonx Orchestrate is:
- **Enterprise-ready** (not just a demo)
- **Standards-based** (OpenAPI, YAML)
- **Extensible** (easy to add agents/tools)
- **Transparent** (full audit trail)