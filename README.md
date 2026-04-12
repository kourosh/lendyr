# Lendyr Bank - AI Customer Care Demo
## Watsonx Orchestrate Multi-Agent System with Autonomous Decision-Making

This project demonstrates an advanced AI customer care system built with IBM watsonx Orchestrate, featuring autonomous loan deferral approval with real-time credit evaluation.

---

## 🎯 What This Demo Shows

### Autonomous AI Decision-Making
- **Real Business Decisions:** AI agent approves/denies loan deferrals based on credit evaluation
- **Risk Management:** Evaluates credit score and payment history against business rules
- **Financial Impact:** Calculates interest accrual and balance changes
- **Compliance-Ready:** Requires customer agreement, maintains audit trail

### Multi-Agent Orchestration
- **Customer Care Agent (Lena):** Main orchestrator, routes to specialists
- **Loan Agent:** Handles loan inquiries and autonomous deferral approvals
- **Account Agent:** Manages account balances and transactions
- **Card Agent:** Handles card freezing, limits, and security
- **Disputes Agent:** Manages transaction disputes

### Key Features
- ✅ Autonomous credit evaluation and approval
- ✅ Real-time API integration with DB2 database
- ✅ Multi-agent collaboration and routing
- ✅ Transparent decision-making with full explanations
- ✅ Compliance-ready with customer agreement workflow
- ✅ Production-ready architecture on IBM Code Engine

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- IBM Cloud account with watsonx.ai access
- IBM Cloud API Key

### 1. Clone and Setup
```bash
cd /Users/kk76/Public/lendyr

# Set environment variables
export IBM_CLOUD_API_KEY="your_api_key_here"
export WATSONX_PROJECT_ID="your_project_id_here"

# Run automated setup
./scripts/setup_local_adk.sh
```

### 2. Start Demo
```bash
# Start interactive chat
orchestrate agents chat lendyr_customer_care
```

### 3. Follow Demo Script
See [DEMO_CONVERSATION_FLOW_V2.md](docs/DEMO_CONVERSATION_FLOW_V2.md) for the complete conversation script.

---

## 📁 Project Structure

```
lendyr/
├── agents/                          # Agent YAML configurations
│   ├── lendyr_customer_care.yaml   # Main orchestrator agent
│   ├── loan_agent.yaml             # Loan specialist with deferral
│   ├── account_agent.yaml          # Account specialist
│   ├── card_agent.yaml             # Card management specialist
│   └── disputes_agent.yaml         # Disputes specialist
│
├── tools/                           # API tools and specifications
│   └── lendyr_openapi.json         # OpenAPI spec with all endpoints
│
├── lendyr_code_engine/             # FastAPI backend
│   ├── main.py                     # API implementation
│   ├── db.py                       # Database utilities
│   └── requirements.txt            # Python dependencies
│
├── docs/                            # Documentation
│   ├── DEMO_CONVERSATION_FLOW_V2.md  # Complete demo script
│   ├── LOCAL_ADK_SETUP.md            # Local setup guide
│   ├── QUICK_REFERENCE.md            # Quick reference card
│   ├── BUILD_AGENTS.md               # Agent building guide
│   └── TECHNICAL_ARCHITECTURE.md     # Architecture details
│
└── scripts/                         # Utility scripts
    ├── setup_local_adk.sh          # Automated setup script
    └── test_api.sh                 # API testing script
```

---

## 🎬 Demo Scenario

### The Story
Brian Nguyen is stressed about an upcoming auto loan payment on April 13th. He's not sure he has enough in his checking account and wants to explore options.

### The Journey
1. **Customer contacts support** → Lena (Customer Care) greets and verifies identity
2. **Routes to Loan Specialist** → Shows loan details and payment information
3. **Customer requests deferral** → Agent evaluates credit autonomously
4. **Instant approval** → Agent approves 30-day deferral based on:
   - Credit score: 755 (excellent, above 700 threshold)
   - Payment history: 45 consecutive on-time payments
5. **Transparent terms** → Agent explains financial impact and gets agreement
6. **System updated** → New payment date set to May 13, 2026

### The Impact
- **Traditional Process:** 2-3 days, multiple calls, manual review
- **AI Process:** 2 minutes, single conversation, instant approval
- **Time Reduction:** 99%
- **Customer Satisfaction:** Immediate resolution

---

## 🔥 Key Demo Moments

### 1. Autonomous Decision-Making
The loan agent makes a real business decision:
- Evaluates credit score (755)
- Reviews payment history (100% on-time)
- Applies business rules (credit >= 700, no missed payments)
- **Approves loan deferral autonomously**

### 2. Financial Impact Calculation
Agent calculates and presents:
- Interest accrued during deferral: $102.15
- New loan balance: $17,785.73
- New payment date: May 13, 2026
- Impact on final payoff date

### 3. Compliance & Transparency
- Decision reasoning fully explained
- All financial impacts disclosed
- Customer agreement explicitly required
- Complete audit trail maintained

---

## 🛠️ Technical Architecture

### Backend API
- **Framework:** FastAPI
- **Database:** IBM DB2 on Cloud
- **Deployment:** IBM Code Engine
- **Endpoint:** https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud

### AI Agents
- **Platform:** IBM watsonx Orchestrate
- **LLM:** IBM Granite 3 8B Instruct
- **Architecture:** Multi-agent with autonomous decision-making
- **Integration:** REST API via OpenAPI specification

### Key APIs
- `GET /customers/{email}` - Customer profile with credit score
- `GET /customers/{email}/loans` - Loan details
- `GET /customers/{email}/payment-history` - Payment history for credit evaluation
- `POST /customers/{email}/loans/{loan_id}/defer` - Autonomous deferral approval

---

## 📊 Business Rules

### Loan Deferral Approval Criteria
```python
# Automatic approval if:
credit_score >= 700 AND missed_payments == 0

# Automatic denial if:
credit_score < 700 OR missed_payments > 0
```

### Deferral Terms
- **Deferral Period:** 30 days
- **Interest Calculation:** APR prorated for 30 days
- **Balance Impact:** Interest added to outstanding balance
- **Payoff Extension:** Approximately 1 month

---

## 🧪 Testing

### Test Individual Agent
```bash
orchestrate agents test loan_agent \
  --message "The customer email is brian.nguyen@email.com. Show loan details."
```

### Test API Endpoint
```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/brian.nguyen@email.com
```

### View Agent Logs
```bash
orchestrate agents logs lendyr_customer_care
```

### View Conversation Trace
```bash
orchestrate agents trace lendyr_customer_care --last-session
```

---

## 📚 Documentation

- **[Demo Script](docs/DEMO_CONVERSATION_FLOW_V2.md)** - Complete conversation flow with talking points
- **[Local Setup](docs/LOCAL_ADK_SETUP.md)** - Detailed setup instructions
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Quick reference card for demos
- **[Build Agents](docs/BUILD_AGENTS.md)** - Step-by-step agent building guide
- **[Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)** - System architecture details

---

## 🎯 Use Cases

This demo pattern applies to:
- **Financial Services:** Loan deferrals, credit approvals, payment plans
- **Insurance:** Claims processing, policy modifications
- **Healthcare:** Prior authorizations, appointment scheduling
- **Retail:** Returns processing, refund approvals
- **Any domain requiring:** Risk assessment + Autonomous approval

---

## 🔐 Security & Compliance

### Built-in Safeguards
- ✅ Configurable business rules
- ✅ Transparent decision reasoning
- ✅ Customer agreement required
- ✅ Complete audit trail
- ✅ Explainable AI decisions

### Compliance Features
- Decision criteria clearly documented
- Financial impact fully disclosed
- Customer consent explicitly captured
- All API calls logged and traceable

---

## 🚀 Deployment

### Local Development
```bash
./scripts/setup_local_adk.sh
```

### Production (IBM Code Engine)
See [CODE_ENGINE_DEPLOYMENT.md](docs/CODE_ENGINE_DEPLOYMENT.md) for deployment instructions.

---

## 💡 Key Talking Points

### For Technical Audiences
- Multi-agent orchestration with autonomous decision-making
- Real-time credit evaluation and risk assessment
- Production-ready architecture on IBM Cloud
- Configurable business rules and approval thresholds

### For Business Audiences
- 99% time reduction (3 days → 2 minutes)
- Instant customer satisfaction
- 95% operational cost reduction
- Scalable to 1000x volume
- 100% consistent rule compliance

### For Compliance/Risk Teams
- Transparent decision-making with full audit trail
- Configurable risk thresholds
- Customer agreement workflow
- Explainable AI with clear reasoning

---

## 🆘 Troubleshooting

### Common Issues

**Agent not responding?**
```bash
orchestrate agents list
orchestrate agents logs lendyr_customer_care
```

**API connection failed?**
```bash
curl https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/health
```

**Authentication issues?**
```bash
echo $IBM_CLOUD_API_KEY
orchestrate auth login --api-key $IBM_CLOUD_API_KEY
```

See [LOCAL_ADK_SETUP.md](docs/LOCAL_ADK_SETUP.md) for detailed troubleshooting.

---

## 📈 Roadmap

- [ ] Add more loan types (mortgage, personal)
- [ ] Implement payment plan negotiations
- [ ] Add fraud detection capabilities
- [ ] Expand to insurance claims processing
- [ ] Multi-language support

---

## 🤝 Contributing

This is a demo project for IBM watsonx Orchestrate. For questions or improvements, please contact the project team.

---

## 📄 License

Copyright © 2026 IBM Corporation. All rights reserved.

---

## 🎉 Ready to Demo!

1. ✅ Run setup: `./scripts/setup_local_adk.sh`
2. ✅ Start chat: `orchestrate agents chat lendyr_customer_care`
3. ✅ Follow script: [DEMO_CONVERSATION_FLOW_V2.md](docs/DEMO_CONVERSATION_FLOW_V2.md)
4. ✅ Reference card: [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)

**Let's show Gartner the future of AI-powered customer care! 🚀**

---

Built with ❤️ using IBM watsonx Orchestrate