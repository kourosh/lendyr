# Authentication Quick Reference Card

## Test Credentials

### Valid Customer Credentials (Use for Testing)

| Customer ID | PIN   | Name              | Email                        |
|-------------|-------|-------------------|------------------------------|
| **846301**  | 93810 | Alice Martinez    | alice.martinez@email.com     |
| **846302**  | 24592 | Brian Nguyen      | brian.nguyen@email.com       |
| **846303**  | 13278 | Carla Thompson    | carla.thompson@email.com     |
| **846304**  | 46048 | David Kim         | david.kim@email.com          |
| **846305**  | 42098 | Elena Okafor      | elena.okafor@email.com       |
| **846306**  | 39256 | Frank Rossi       | frank.rossi@email.com        |
| **846307**  | 28289 | Grace Patel       | grace.patel@email.com        |
| **846308**  | 23434 | Henry Williams    | henry.williams@email.com     |
| **846309**  | 98696 | Isabela Cruz      | isabela.cruz@email.com       |
| **846310**  | 81482 | James Holloway    | james.holloway@email.com     |

## Quick Test Scripts

### Test 1: Successful Authentication
```
You: "I need to check my account balance"
Agent: "What is your customer ID number?"
You: "846301"
Agent: "Please provide your 5-digit PIN"
You: "93810"
Expected: ✅ Authentication successful, proceeds with balance check
```

### Test 2: Retry Logic
```
You: "Help with my card"
Agent: "What is your customer ID number?"
You: "846302"
Agent: "Please provide your 5-digit PIN"
You: "00000"
Expected: ❌ "Incorrect, let's try again"
Agent: "What is your customer ID number?"
You: "846302"
Agent: "Please provide your 5-digit PIN"
You: "24592"
Expected: ✅ Authentication successful
```

### Test 3: Lockout
```
You: "Check my loan"
Agent: "What is your customer ID number?"
You: "846303"
Agent: "Please provide your 5-digit PIN"
You: "11111"
Expected: ❌ "Incorrect, let's try again"
Agent: "What is your customer ID number?"
You: "846303"
Agent: "Please provide your 5-digit PIN"
You: "22222"
Expected: 🚫 "Please call 1-800-LENDYR-1"
```

## Support Number
**1-800-LENDYR-1**

## Common Issues

| Issue | Solution |
|-------|----------|
| "Tool not found" | Import tool: `orchestrate tools import -k python -f tools/customer_auth_tool.py` |
| "Agent not updated" | Update agent: `orchestrate agents update lendyr_customer_care -f agents/lendyr_customer_care.yaml` |
| "Database connection error" | Check .env file in lendyr_code_engine/ |
| "PIN not working" | Verify PIN was added: `python3 scripts/show_customers.py` |

## Deployment Commands

```bash
# Import authentication tool
orchestrate tools import -k python -f tools/customer_auth_tool.py

# Update main agent
orchestrate agents update lendyr_customer_care -f agents/lendyr_customer_care.yaml

# Verify tool is imported
orchestrate tools list | grep authenticate

# Verify agent is updated
orchestrate agents get lendyr_customer_care
```

## Expected Agent Behavior

1. ✅ Always greets customer first
2. ✅ Always asks for Customer ID before PIN
3. ✅ Always validates credentials before proceeding
4. ✅ Tracks attempts (max 2)
5. ✅ Uses customer email from auth response for API calls
6. ✅ Routes to specialist agents after authentication
7. ✅ Directs to 1-800-LENDYR-1 after 2 failed attempts

## Testing Checklist

- [ ] Test successful authentication on first attempt
- [ ] Test successful authentication on second attempt
- [ ] Test lockout after 2 failed attempts
- [ ] Test with different customer IDs
- [ ] Test routing to account_agent after auth
- [ ] Test routing to card_agent after auth
- [ ] Test routing to loan_agent after auth
- [ ] Test routing to disputes_agent after auth
- [ ] Test routing to loan_deferral_agent after auth
- [ ] Verify customer email is passed to specialist agents