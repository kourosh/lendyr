# Lendyr Demo - Quick Reference Card

## 🚀 Quick Start Commands

### Setup (One-time)
```bash
# Set environment variables
export IBM_CLOUD_API_KEY="your_api_key_here"
export WATSONX_PROJECT_ID="your_project_id_here"

# Run setup script
./scripts/setup_local_adk.sh
```

### Start Demo
```bash
# Start interactive chat with Customer Care agent
orchestrate agents chat lendyr_customer_care
```

---

## 💬 Demo Script (Copy-Paste Ready)

### Turn 1: Customer Opens Conversation
```
Hi, I'm a bit stressed. I have an auto loan payment coming up on April 13th and I'm not sure I have enough in my checking account. Can you help me figure out my options?
```

### Turn 2: Provide Email
```
brian.nguyen@email.com
```

### Turn 3: Wait for loan details, then request deferral
```
Actually, I'm wondering - could I defer this payment by 30 days? That would give me more breathing room.
```

### Turn 4: Accept terms
```
Yes, I understand and agree to those terms. That extra month will really help.
```

### Turn 5: Close conversation
```
No, that covers everything. Thank you so much for all your help!
```

---

## 🎯 Key Demo Moments

### 1. Empathy & Routing (Turn 1-2)
**What to highlight:**
- Agent acknowledges customer stress
- Asks for email to verify identity
- Routes to appropriate specialist

### 2. Loan Details (Turn 3)
**What to highlight:**
- Automatic data retrieval
- Clear presentation of loan information
- Next payment date prominently shown

### 3. 🔥 AUTONOMOUS DECISION (Turn 4)
**What to highlight:**
- Agent evaluates credit score (755)
- Checks payment history (45 on-time payments)
- Makes approval decision autonomously
- Calculates financial impact ($102.15 interest)
- Presents transparent terms

**Key talking point:**
> "This is the money shot! The AI just made a real business decision with financial impact - approving a loan deferral that changes payment dates and balances. It evaluated credit risk, calculated interest, and presented full transparency - all in seconds."

### 4. Compliance & Agreement (Turn 5)
**What to highlight:**
- Customer must explicitly agree to terms
- All impacts clearly explained
- Audit trail maintained

---

## 📊 Expected Results

### Brian Nguyen's Profile
- **Email:** brian.nguyen@email.com
- **Credit Score:** 755 (Excellent)
- **Payment History:** 45 consecutive on-time payments
- **Auto Loan Balance:** $17,683.58
- **Monthly Payment:** $469.35
- **Next Payment:** April 13, 2026

### Deferral Approval Details
- **Status:** APPROVED ✅
- **Reason:** Credit score 755 (>700) + Perfect payment history
- **New Payment Date:** May 13, 2026
- **Interest Accrued:** $102.15
- **New Balance:** $17,785.73

---

## 🎪 Alternative Scenarios

### Scenario A: Denial (Low Credit)
If customer had credit score of 650:
- Status: DENIED ❌
- Reason: Credit score below 700 threshold
- Agent offers alternatives

### Scenario B: Denial (Missed Payments)
If customer had missed payments:
- Status: DENIED ❌
- Reason: Payment history requirement not met
- Agent maintains empathy, offers alternatives

---

## 🔍 Useful Commands

### View Agent Logs
```bash
orchestrate agents logs lendyr_customer_care
```

### View Last Conversation Trace
```bash
orchestrate agents trace lendyr_customer_care --last-session
```

### Test Individual Agent
```bash
orchestrate agents test loan_agent \
  --message "The customer email is brian.nguyen@email.com. Show loan details."
```

### List All Agents
```bash
orchestrate agents list
```

### List All Tools
```bash
orchestrate tools list
```

### Verify API Health
```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health
```

---

## 🐛 Quick Troubleshooting

### Agent not responding?
```bash
# Check agent status
orchestrate agents list

# View logs
orchestrate agents logs lendyr_customer_care
```

### API not working?
```bash
# Test API endpoint
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com
```

### Authentication issues?
```bash
# Verify API key is set
echo $IBM_CLOUD_API_KEY

# Re-authenticate
orchestrate auth login --api-key $IBM_CLOUD_API_KEY
```

---

## 💡 Key Talking Points for Gartner

### 1. Autonomous Decision-Making
> "This isn't just a chatbot - it's making real business decisions with financial impact. The agent evaluated creditworthiness and approved a loan deferral autonomously."

### 2. Risk Management
> "Risk is built in. The agent checked credit score (755) and payment history (100% on-time) against configurable business rules before approving."

### 3. Transparency & Compliance
> "Every decision is explainable. The agent showed why it approved, calculated the financial impact, and required explicit customer agreement."

### 4. Real-Time Integration
> "All of this happened in real-time - credit lookup, payment history analysis, interest calculation, and system update - in a single conversation."

### 5. Business Impact
> "Traditional process: 2-3 days, multiple calls, manual review. AI process: 2 minutes, single conversation, instant approval."

---

## 📈 Success Metrics

- **Time Reduction:** 99% (3 days → 2 minutes)
- **Customer Satisfaction:** Instant resolution
- **Operational Cost:** 95% reduction
- **Scalability:** Handle 1000x volume
- **Consistency:** 100% rule compliance

---

## 🎬 Closing Statement

> "What you just saw is the future of financial services - AI agents that don't just answer questions, but make real business decisions with full transparency and compliance. Brian got instant approval for a loan deferral that would have taken days through traditional channels. The agent evaluated his creditworthiness, calculated the financial impact, and updated the system - all in a single conversation. This same pattern works for insurance claims, healthcare authorizations, mortgage applications, and any process requiring risk assessment and approval. Watsonx Orchestrate makes it possible to deploy this level of sophistication in weeks, not years."

---

## 📞 Support Contacts

- **Technical Issues:** Check docs/LOCAL_ADK_SETUP.md
- **Demo Questions:** See docs/DEMO_CONVERSATION_FLOW_V2.md
- **Architecture:** See docs/TECHNICAL_ARCHITECTURE.md

---

**Print this page and keep it handy during your demo! 📄**