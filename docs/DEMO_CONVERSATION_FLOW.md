# Gartner Demo: Conversation Flow Script
## Financial Hardship Assistance Scenario

This is a detailed conversation script showing exactly what to say and what to expect from each agent.

---

## 🎬 Scene Setup

**Context:** You are demonstrating Watsonx Orchestrate to Gartner analysts. You'll play the role of Brian Nguyen, a customer concerned about an upcoming loan payment.

**Key Message:** "Watch how multiple AI agents collaborate seamlessly to solve a complex financial problem - all in a single conversation."

---

## 💬 Conversation Script

### Turn 1: Customer Opens Conversation

**YOU (as Brian):**
```
Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th 
and I'm not sure I have enough in my checking account. Can you help me 
figure out my options?
```

**CUSTOMER CARE AGENT (Lena):**
```
Hello! I'm Lena, your customer care agent at Lendyr Bank. I completely 
understand your concern about the upcoming payment - let's work through 
this together.

To help you, I'll need to look up your account. Could you please provide 
your email address?
```

**💡 DEMO TALKING POINT:**
*"Notice how the agent immediately acknowledges the customer's stress and responds with empathy. This is configured in the agent's instructions."*

---

### Turn 2: Customer Provides Email

**YOU (as Brian):**
```
brian.nguyen@email.com
```

**CUSTOMER CARE AGENT (Lena):**
```
Thank you, Brian! I've verified your account. I can see you're concerned 
about your auto loan payment. Let me connect you with our loan specialist 
who can review your loan details and help us understand exactly what you're 
working with.

[Routing to loan_agent...]
```

**💡 DEMO TALKING POINT:**
*"The agent just called the get_customer API to verify Brian's identity. Now it's intelligently routing to the loan specialist because the customer mentioned 'auto loan payment'. No manual intervention needed."*

---

### Turn 3: Loan Agent Takes Over

**LOAN AGENT:**
```
Hello Brian, I'm here to help with your auto loan. Let me pull up your 
loan details.

[Calling get_loans API...]

I can see your auto loan information:
- Loan Type: Auto Loan
- Original Amount: $28,000.00
- Outstanding Balance: $17,683.58
- Monthly Payment: $469.35
- Next Payment Due: April 13th, 2026 (that's in 3 days!)
- Interest Rate: 6.9%
- Progress: You've paid off $10,316.42 - great progress!

I understand the timing is tight with the payment coming up so soon. Let me 
connect you with our account specialist to review your available funds and 
explore your options.

[Routing to account_agent...]
```

**💡 DEMO TALKING POINT:**
*"The loan agent automatically called the API and presented the data in a customer-friendly format. Notice how it calculated the progress and acknowledged the tight timeline. Now it's routing to the account specialist because we need to check available funds."*

---

### Turn 4: Account Agent Reviews Finances

**ACCOUNT AGENT:**
```
Hi Brian, I'm your account specialist. Let me review your accounts to see 
what you're working with for this $469.35 payment.

[Calling get_accounts API...]

Here's your current financial picture:

**Checking Account** (****1004)
- Balance: $1,247.80
- Status: Active

**Savings Account** (****2005)
- Balance: $3,200.50
- Status: Active

**Credit Card** (****3006)
- Balance: $887.11 used
- Credit Limit: $5,000.00
- Available Credit: $4,112.89

Let me also check your recent transactions to understand your cash flow...

[Calling get_transactions API...]

I can see your recent activity includes:
- Regular payroll deposits
- Normal spending patterns
- No unusual large charges pending

So here's the situation: Your checking account has $1,247.80, which is 
enough to cover the $469.35 payment. However, that would leave you with 
about $778 as a buffer, which might feel tight.

You have some good options here. Let me connect you with our card specialist 
to discuss your credit card as a potential backup option.

[Routing to card_agent...]
```

**💡 DEMO TALKING POINT:**
*"Notice the account agent made TWO API calls - one for accounts, one for transactions. It's analyzing the complete financial picture and already thinking ahead about solutions. This is the power of AI agents with access to real-time data."*

---

### Turn 5: Card Agent Explains Options

**CARD AGENT:**
```
Hi Brian, I'm your card management specialist. Let me review your credit 
card to see what backup options you have.

[Calling get_cards API...]

Here's your credit card information:

**Visa Credit Card** (ending in 2002)
- Card Type: Credit
- Status: Active
- Current Balance: $887.11 used
- Credit Limit: $5,000.00
- Available Credit: $4,112.89
- Daily Spending Limit: $5,000.00
- Interest Rate: 21.99% APR

The good news is you have plenty of available credit - $4,112.89 - which 
is more than enough to cover your loan payment if needed. Your daily limit 
is already at the maximum, so you have full access to your available credit.

This gives you a solid backup option if you want more flexibility. Let me 
send you back to our customer care team to summarize all your options.

[Routing to lendyr_customer_care...]
```

**💡 DEMO TALKING POINT:**
*"The card agent provided a complete picture of the credit card options. Now watch how the customer care agent synthesizes everything we've learned from three different specialists into a clear set of recommendations."*

---

### Turn 6: Customer Care Agent Synthesizes Solution

**CUSTOMER CARE AGENT (Lena):**
```
Alright Brian, I've worked with our loan, account, and card specialists to 
understand your complete situation. Here's what we found:

**Your Situation:**
- Auto loan payment: $469.35 due April 13th (3 days away)
- Checking account: $1,247.80 available
- Savings account: $3,200.50 available
- Credit card: $4,112.89 available credit

**Your Options:**

**Option 1: Pay from Checking (Recommended)**
✓ Pros: Simple, no fees, maintains your savings
✗ Cons: Leaves you with ~$778 buffer until next paycheck
- After payment: $1,247.80 - $469.35 = $778.45 remaining

**Option 2: Transfer from Savings First**
✓ Pros: More comfortable buffer in checking
✗ Cons: Requires a manual transfer (easy to do in mobile app)
- Suggestion: Transfer $500 from savings to checking
- After transfer and payment: $1,278.45 in checking

**Option 3: Use Credit Card as Backup**
✓ Pros: Keep full checking balance, $4,112.89 available
✗ Cons: 21.99% APR if you carry a balance beyond grace period
- Best used only if unexpected expenses arise

**My Recommendation:**
Given that you have 3 days until the payment, I'd suggest Option 1 - pay 
directly from checking. You have enough funds, and $778 should be sufficient 
until your next paycheck. However, if you'd feel more comfortable with a 
larger buffer, Option 2 is also excellent.

Which option feels right for you?
```

**💡 DEMO TALKING POINT:**
*"This is the power of multi-agent orchestration. We had FOUR different specialists collaborate - loan, account, card, and customer care - but the customer experienced it as one seamless conversation. The final agent synthesized insights from all the specialists into clear, actionable recommendations."*

---

### Turn 7: Customer Chooses Option

**YOU (as Brian):**
```
Thank you so much! This really helps. I think I'll go with Option 1 - 
paying from my checking account. The $778 buffer should be fine until 
my next paycheck. I feel much better about this now.
```

**CUSTOMER CARE AGENT (Lena):**
```
Perfect choice, Brian! You're all set then. Your auto loan payment of 
$469.35 will be automatically deducted from your checking account on 
April 13th, leaving you with $778.45.

Just as a reminder:
- Your next payroll deposit typically comes in around the 17th
- You have $3,200.50 in savings if any unexpected expenses come up
- Your credit card has $4,112.89 available as a backup

Is there anything else I can help you with today?
```

**YOU (as Brian):**
```
No, that covers everything. Thank you so much for walking through all 
the options with me. I really appreciate it!
```

**CUSTOMER CARE AGENT (Lena):**
```
You're very welcome, Brian! I'm glad we could ease your concerns. Have a 
great day, and remember - we're always here if you need anything else.
```

---

## 🎯 Demo Debrief for Gartner Analysts

### What Just Happened?

**Single Conversation, Multiple Specialists:**
- 1 conversation from customer perspective
- 5 agent interactions behind the scenes
- 4 different areas of expertise (customer care, loans, accounts, cards)

**Real-Time API Integration:**
- 6 API calls to live banking system
- get_customer (identity verification)
- get_loans (loan details)
- get_accounts (account balances)
- get_transactions (spending analysis)
- get_cards (credit card options)
- All data pulled in real-time, no static responses

**Intelligent Orchestration:**
- Agents decided routing autonomously
- Context maintained across all handoffs
- Customer email passed seamlessly between agents
- No manual intervention or decision trees

**Business Value:**
- **Time:** 5-minute resolution vs. 15-20 minutes with traditional call center
- **Experience:** No transfers, holds, or repeated information
- **Accuracy:** Real-time data, no human lookup errors
- **Scalability:** Same pattern works for any complex scenario

### Technical Architecture Highlights

**Agent-Based Design:**
- Each agent has specialized knowledge and tools
- Modular architecture - easy to add/modify agents
- LLM-agnostic (can use different models per agent)

**API-First Integration:**
- Standard OpenAPI specifications
- Works with any REST API
- Tool-based architecture for easy extension

**Enterprise Ready:**
- Full audit trail of all interactions
- Role-based access control at API level
- Configurable routing and escalation rules

---

## 🔧 Technical Deep Dive (If Requested)

### Show the Agent Configuration

**Customer Care Agent YAML:**
```yaml
collaborators:
  - account_agent
  - card_agent  
  - loan_agent
  - lendyr_disputes_agent

instructions: >
  Route based on customer request:
  - Loan payments -> loan_agent
  - Account balances -> account_agent
  - Card issues -> card_agent
```

**Loan Agent Tools:**
```yaml
tools:
  - get_customer_customers_email_get
  - get_loans_customers_email_loans_get
  - get_disputes_customers_email_disputes_get
```

### Show the API Integration

**OpenAPI Tool Definition:**
```json
{
  "operationId": "get_loans_customers__email__loans_get",
  "parameters": [
    {
      "name": "email",
      "in": "path",
      "required": true,
      "schema": {"type": "string"}
    }
  ]
}
```

---

## 📊 Success Metrics

**Quantitative:**
- Resolution time: 5 minutes vs. 15-20 minutes traditional
- Agent handoffs: 4 seamless transitions
- API calls: 6 successful real-time data retrievals
- Customer satisfaction: Single conversation, no transfers

**Qualitative:**
- Natural conversation flow
- Empathetic responses to customer stress
- Comprehensive solution with multiple options
- Professional closure with clear next steps

---

## 🎪 Alternative Demo Scenarios (If Time Permits)

### Quick Scenario 2: Card Security
**Customer:** "I think I lost my credit card. Can you help me freeze it?"
**Flow:** Customer Care → Card Agent (freeze card) → Customer Care (confirmation)
**Time:** 2 minutes

### Quick Scenario 3: Balance Check
**Customer:** "What's my checking account balance?"
**Flow:** Customer Care → Account Agent → Customer Care
**Time:** 1 minute

**Demo Tip:** Use these to show the system handles simple requests just as well as complex ones.

---

## 🎬 Closing Statement

*"This is the future of customer service - AI agents that collaborate like human specialists, but with the speed and accuracy of automation. The same orchestration pattern works for any industry: insurance claims, technical support, financial planning, healthcare coordination. Watsonx Orchestrate makes it possible to deploy this level of sophistication in weeks, not months."*