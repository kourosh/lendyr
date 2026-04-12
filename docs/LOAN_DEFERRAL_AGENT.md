# Loan Deferral Agent Documentation

## Overview

The Loan Deferral Agent is an AI-powered specialist agent that autonomously handles loan payment deferral requests for Lendyr Bank customers. It evaluates eligibility based on credit score and payment history, then automatically approves or denies requests without human intervention.

## Features

- **Autonomous Decision Making**: Automatically approves or denies deferral requests based on predefined criteria
- **Credit Evaluation**: Checks customer credit score and payment history
- **Financial Impact Calculation**: Calculates interest accrual and new payment dates
- **Transparent Communication**: Clearly explains approval/denial reasons and financial impacts

## Agent Configuration

**File**: `agents/loan_agent.yaml`

**LLM**: `watsonx/ibm/granite-3-8b-instruct`

**Tools**:
- `get_customer_customers_email_get` - Retrieve customer profile including credit score
- `get_loans_customers_email_loans_get` - Get loan details
- `get_payment_history_customers_email_payment_history_get` - Check payment history
- `request_loan_deferral_customers_email_loans_loan_id_defer_post` - Submit deferral request

## Approval Criteria

The agent uses the following autonomous decision logic:

### ✅ APPROVED if:
- Credit score ≥ 700 **AND**
- Zero missed payments in payment history

### ❌ DENIED if:
- Credit score < 700 **OR**
- One or more missed payments

## Deferral Process Flow

### 1. Customer Request
Customer asks to defer their loan payment, providing a reason.

### 2. Data Collection
Agent automatically:
- Retrieves customer profile (including credit score)
- Gets loan details (balance, payment amount, interest rate)
- Checks payment history (on-time vs missed payments)

### 3. Eligibility Evaluation
Agent evaluates against approval criteria:
```
IF credit_score >= 700 AND missed_payments == 0:
    APPROVE
ELSE:
    DENY
```

### 4. Financial Impact Calculation (if approved)
- **Deferred Payment Amount**: Current monthly payment
- **Interest Accrued**: One month's interest on the deferred payment
  - Formula: `monthly_payment × (interest_rate / 12 / 100)`
- **New Outstanding Balance**: Original balance + interest accrued
- **New Payment Date**: Original date + 30 days

### 5. Response to Customer
Agent provides:
- **Approval Status**: Approved or Denied
- **Approval Reason**: Explanation based on credit evaluation
- **Deferral Details** (if approved):
  - Deferred payment amount
  - Interest that will be added
  - New outstanding balance
  - Original vs new payment date
- **Credit Evaluation Summary**:
  - Credit score
  - Total payments made
  - On-time payment percentage
  - Missed payments count

### 6. Customer Confirmation (if approved)
Agent asks: "Do you agree to these terms?"
- Customer must explicitly confirm before deferral is finalized

## API Endpoints

### Get Payment History
```
GET /customers/{email}/payment-history
```

**Response**:
```json
{
  "customer_id": 1,
  "credit_score": 750,
  "payment_history": [
    {
      "payment_id": 1,
      "payment_date": "2024-01-15",
      "payment_amount": 500.00,
      "was_late": 0,
      "days_late": 0,
      "auto_pay_used": 1,
      "note": null
    }
  ],
  "statistics": {
    "total_payments": 12,
    "on_time_payments": 12,
    "missed_payments": 0,
    "on_time_percentage": 100.0
  }
}
```

### Request Loan Deferral
```
POST /customers/{email}/loans/{loan_id}/defer
```

**Request Body**:
```json
{
  "reason": "Unexpected medical expenses"
}
```

**Response (Approved)**:
```json
{
  "loan_id": "L001",
  "customer_name": "John Doe",
  "approval_status": "approved",
  "approval_reason": "Approved based on excellent credit score (750) and perfect payment history (12/12 on-time payments)",
  "deferral_details": {
    "reason": "Unexpected medical expenses",
    "deferred_payment_amount": 500.00,
    "interest_accrued": 2.81,
    "new_outstanding_balance": 10502.81,
    "original_next_payment_date": "2024-02-15",
    "new_next_payment_date": "2024-03-16"
  },
  "credit_evaluation": {
    "credit_score": 750,
    "total_payments": 12,
    "on_time_payments": 12,
    "missed_payments": 0,
    "on_time_percentage": 100.0
  }
}
```

**Response (Denied)**:
```json
{
  "loan_id": "L002",
  "customer_name": "Jane Smith",
  "approval_status": "denied",
  "approval_reason": "Denied due to: credit score below threshold (680 < 700), 2 missed payment(s)",
  "deferral_details": {
    "reason": "Temporary financial hardship",
    "deferred_payment_amount": 750.00,
    "interest_accrued": 4.22,
    "new_outstanding_balance": 15754.22,
    "original_next_payment_date": "2024-02-15",
    "new_next_payment_date": "2024-03-16"
  },
  "credit_evaluation": {
    "credit_score": 680,
    "total_payments": 10,
    "on_time_payments": 8,
    "missed_payments": 2,
    "on_time_percentage": 80.0
  }
}
```

## Example Conversations

### Scenario 1: Approved Deferral

**Customer**: "I need to defer my loan payment this month due to unexpected medical expenses."

**Agent**: 
1. Retrieves customer profile (credit score: 750)
2. Gets loan details (monthly payment: $500, balance: $10,500)
3. Checks payment history (12/12 on-time)
4. Processes deferral request

**Agent Response**:
"I've reviewed your loan deferral request. Good news - you're approved!

**Approval Reason**: Your excellent credit score (750) and perfect payment history (12/12 on-time payments) qualify you for this deferral.

**Deferral Details**:
- Deferred payment: $500.00
- Interest to be added: $2.81
- New loan balance: $10,502.81
- Original payment date: February 15, 2024
- New payment date: March 16, 2024

This means your next payment will be due on March 16, 2024, and $2.81 in interest will be added to your loan balance. Your final payoff date will be extended by approximately one month.

Do you agree to these terms?"

### Scenario 2: Denied Deferral

**Customer**: "Can I defer my loan payment? I'm having some temporary financial difficulties."

**Agent**:
1. Retrieves customer profile (credit score: 680)
2. Gets loan details
3. Checks payment history (2 missed payments)
4. Processes deferral request

**Agent Response**:
"I've reviewed your loan deferral request. Unfortunately, your request has been denied.

**Denial Reason**: Your application doesn't meet our criteria due to:
- Credit score below threshold (680 < 700)
- 2 missed payment(s) in your history

**Your Payment Record**:
- Total payments: 10
- On-time payments: 8
- Missed payments: 2
- On-time percentage: 80%

**Alternative Options**:
I recommend speaking with our account specialist who can discuss other assistance programs that might be available to you. Would you like me to connect you with the account agent?"

## Agent Instructions Summary

The loan agent follows these key principles:

1. **Always check payment history** before processing any deferral request
2. **Be transparent** about financial impacts - customers must understand the cost
3. **Explain eligibility criteria** clearly when denying requests
4. **Format financial data** professionally (currency, percentages, dates)
5. **Require explicit confirmation** before finalizing approved deferrals
6. **Suggest alternatives** when denying requests (e.g., account_agent)

## Testing the Agent

### Test Case 1: Eligible Customer
```bash
# Customer with credit score 750, no missed payments
Email: john.doe@example.com
Expected: APPROVED
```

### Test Case 2: Low Credit Score
```bash
# Customer with credit score 680, no missed payments
Email: jane.smith@example.com
Expected: DENIED (credit score < 700)
```

### Test Case 3: Missed Payments
```bash
# Customer with credit score 750, 1 missed payment
Email: bob.johnson@example.com
Expected: DENIED (missed payments > 0)
```

## Integration with Main Agent

The loan agent is integrated into the main Lendyr Customer Care agent as a sub-agent. When customers ask about loan deferrals, the main agent routes the conversation to the loan specialist.

**Main Agent File**: `agents/lendyr_customer_care.yaml`

## Database Schema

### PAYMENT_HISTORY Table
```sql
CREATE TABLE "LENDYR-DEMO".PAYMENT_HISTORY (
    payment_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL,
    was_late SMALLINT DEFAULT 0,
    days_late INTEGER DEFAULT 0,
    auto_pay_used SMALLINT DEFAULT 0,
    note VARCHAR(500),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);
```

## Deployment

The loan deferral functionality is deployed as part of the main Lendyr API on IBM Code Engine:

**API URL**: `https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud`

**Deployment Steps**: See `docs/REDEPLOY_STEPS.md`

## Future Enhancements

Potential improvements for the loan deferral agent:

1. **Flexible Deferral Periods**: Allow 30, 60, or 90-day deferrals
2. **Partial Deferrals**: Defer only a portion of the payment
3. **Multiple Deferrals**: Track and limit number of deferrals per year
4. **Hardship Programs**: Integration with special assistance programs
5. **Payment Plan Restructuring**: Offer alternative payment schedules
6. **Notification System**: Send confirmation emails and reminders
7. **Analytics Dashboard**: Track deferral approval rates and trends

## Support

For questions or issues with the loan deferral agent:
- Review the agent configuration in `agents/loan_agent.yaml`
- Check API logs in IBM Code Engine
- Test endpoints using `scripts/test_api.sh`
- Refer to `docs/QUICK_REFERENCE.md` for common commands

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Maintained by**: Lendyr Bank Development Team