# Bill Payment with Invoice Upload - Testing Guide

## Overview

This guide provides step-by-step instructions for testing the complete bill payment feature with invoice upload capability in the local Orchestrate environment.

## Prerequisites

1. **Local Orchestrate Environment Running**
   ```bash
   cd /Users/kk76/Public/lendyr
   uvx --from ibm-watsonx-orchestrate orchestrate dev
   ```
   Access at: http://localhost:4321

2. **All Components Imported**
   - ✅ `lendyr_customer_care` agent (Lena)
   - ✅ `bill_payment_agent` specialist
   - ✅ `invoice_extraction_flow` tool (agentic workflow)
   - ✅ `create_bill_payment` and `get_bill_payments` tools

## Test Scenario 1: Manual Bill Payment Entry

### Step 1: Start Chat
1. Open http://localhost:4321
2. Select **lendyr_customer_care** agent
3. Start a new conversation

### Step 2: Authenticate
```
User: Hi, I need to pay a bill
Agent: [Requests authentication]
User: My customer ID is 846301 and PIN is 93810
Agent: Welcome, Alice Martinez! How can I help?
```

### Step 3: Manual Payment Entry
```
User: I need to pay my electric bill to ABC Electric Company
Agent: [Transfers to bill_payment_agent]
Agent: I can help you pay that bill. Please provide:
- Payee name
- Payee address
- Amount
- Which account to pay from
```

### Step 4: Provide Payment Details
```
User: 
- Payee: ABC Electric Company
- Address: PO Box 5678, San Francisco, CA 94102
- Amount: $260.50
- Pay from my checking account
```

### Step 5: Verify Payment
Agent should:
1. Retrieve customer's accounts
2. Verify sufficient funds in checking account
3. Create bill payment with check number (CHK#####)
4. Confirm payment details and estimated delivery (5-7 business days)

**Expected Result:**
```
✅ Payment created successfully
✅ Check number: CHK12345
✅ Amount: $260.50 debited from checking
✅ Payee: ABC Electric Company
✅ Delivery: 5-7 business days
```

## Test Scenario 2: Invoice Upload with Automatic Extraction

### Step 1: Authenticate (Same as Scenario 1)
```
User: My customer ID is 846301 and PIN is 93810
```

### Step 2: Request Invoice Upload
```
User: I have an invoice I'd like to upload to pay a bill
```

### Step 3: Upload Invoice
**Expected Behavior:**
- Agent should recognize the request involves document upload
- Agent should call `invoice_extraction_flow` tool
- UI should display **file upload button** or prompt

**Upload Test Invoice:**
Use the test invoice at: `/Users/kk76/Public/lendyr/test_invoice.txt`

Or create a PDF with this content:
```
INVOICE

ABC Electric Company
123 Power Street
San Francisco, CA 94102

Invoice Number: INV-2026-04-001
Due Date: May 15, 2026
TOTAL AMOUNT DUE: $260.50

Payment Address:
ABC Electric Company
PO Box 5678
San Francisco, CA 94102
```

### Step 4: Review Extracted Information
The `invoice_extraction_flow` should extract:
- **Payee Name**: ABC Electric Company
- **Payee Address**: PO Box 5678, San Francisco, CA 94102
- **Amount Due**: $260.50
- **Invoice Number**: INV-2026-04-001
- **Due Date**: May 15, 2026

**Human-in-the-Loop Review:**
- If confidence < 0.7 for any field, user will be prompted to verify/correct
- User can edit any extracted values before proceeding

### Step 5: Select Payment Account
```
Agent: I've extracted the payment information. Which account would you like to pay from?
User: My checking account
```

### Step 6: Confirm Payment
Agent should:
1. Display extracted payment details
2. Verify sufficient funds
3. Request final confirmation
4. Create payment with check number

**Expected Result:**
```
✅ Invoice processed successfully
✅ Extracted information verified
✅ Payment created: CHK12346
✅ Amount: $260.50 to ABC Electric Company
✅ Check will be mailed in 5-7 business days
```

## Test Scenario 3: View Payment History

### After Creating Payments
```
User: Show me my recent bill payments
Agent: [Calls get_bill_payments]
```

**Expected Result:**
```
Recent Bill Payments:
1. CHK12345 - $260.50 to ABC Electric Company (Pending)
2. CHK12346 - $260.50 to ABC Electric Company (Pending)
```

## Test Customer Credentials

| Customer ID | Name              | PIN   | Email                        |
|-------------|-------------------|-------|------------------------------|
| 846301      | Alice Martinez    | 93810 | alice.martinez@email.com     |
| 846302      | Brian Nguyen      | 24592 | brian.nguyen@email.com       |
| 846303      | Carla Thompson    | 13278 | carla.thompson@email.com     |
| 846304      | David Kim         | 46048 | david.kim@email.com          |

## Verification Checklist

### Invoice Upload Feature
- [ ] Upload button appears when invoice upload is requested
- [ ] PDF files are accepted
- [ ] Image files (JPG, PNG) are accepted
- [ ] Document is processed by AI extraction
- [ ] All 5 fields are extracted (payee_name, payee_address, amount_due, invoice_number, due_date)
- [ ] Review form appears for low-confidence fields
- [ ] User can edit extracted values
- [ ] Corrected values are used for payment

### Bill Payment Processing
- [ ] Customer authentication works
- [ ] Agent transfers to bill_payment_agent specialist
- [ ] Account selection works correctly
- [ ] Funds validation occurs
- [ ] Check number is generated (CHK#####)
- [ ] Payment is recorded in database
- [ ] Confirmation message includes all details
- [ ] Payment history retrieval works

### Error Handling
- [ ] Insufficient funds error is handled gracefully
- [ ] Invalid file format shows appropriate error
- [ ] Failed extraction allows manual entry fallback
- [ ] Authentication failures are handled (2 attempts)

## Database Verification

Check payments were created:
```bash
cd /Users/kk76/Public/lendyr
python3 scripts/check_payments.py
```

## Troubleshooting

### Issue: Upload Button Not Appearing
**Cause:** Agent not recognizing document upload request
**Solution:** Use explicit language: "I want to upload an invoice" or "I have a PDF invoice to upload"

### Issue: Document Extraction Fails
**Cause:** File format not supported or content unclear
**Solution:** 
1. Verify file is PDF or image format
2. Ensure text is clear and readable
3. Fall back to manual entry if needed

### Issue: Payment Creation Fails
**Cause:** Insufficient funds or invalid account
**Solution:**
1. Check account balance
2. Verify customer has checking/savings account
3. Review error message from API

### Issue: Agent Not Transferring to bill_payment_agent
**Cause:** Context not properly set or collaborator not configured
**Solution:**
1. Verify `bill_payment_agent` is in collaborators list
2. Check context mapping includes `customer_id`
3. Re-import agents if needed

## Success Criteria

✅ **Feature Complete When:**
1. User can authenticate successfully
2. User can manually enter bill payment details
3. User can upload invoice (PDF or image)
4. AI extracts payment information accurately
5. User can review and correct extracted data
6. Payment is created with check number
7. User receives confirmation with delivery estimate
8. Payment appears in history

## Next Steps After Testing

1. **Document any issues found**
2. **Capture screenshots of successful flows**
3. **Test with various invoice formats**
4. **Verify database records**
5. **Test error scenarios**
6. **Prepare for cloud deployment** (if local tests pass)

## Notes

- Local environment has full document processing support
- Cloud environment may have limitations with binary file handling
- The `invoice_extraction_flow` uses Groq LLM for extraction
- Human-in-the-loop review threshold is set to 0.7 confidence
- Check numbers are auto-generated in format CHK##### (5 digits)
- Estimated delivery is always 5-7 business days