# Bill Payment Feature - Testing Guide

## Quick Start

The bill payment feature is now fully implemented and ready for testing. This guide provides step-by-step instructions for testing both manual and document-based bill payment workflows.

## Prerequisites

### 1. Backend API Running
```bash
cd lendyr_code_engine
uvicorn main:app --reload --port 8080
```

Verify API is running:
```bash
curl http://localhost:8080/health
```

### 2. Tools and Agents Imported

All components should already be imported. Verify with:
```bash
uvx --from ibm-watsonx-orchestrate orchestrate tools list | grep -E "(create_bill_payment|extract_invoice_info)"
uvx --from ibm-watsonx-orchestrate orchestrate agents list | grep -E "(lendyr_customer_care|bill_payment_agent)"
```

If not imported, run:
```bash
# Import tools
uvx --from ibm-watsonx-orchestrate orchestrate tools import -k openapi -f tools/create_bill_payment/lendyr_openapi.json
uvx --from ibm-watsonx-orchestrate orchestrate tools import -k python -f tools/extract_invoice_info/extract_invoice_info.py

# Import agents
uvx --from ibm-watsonx-orchestrate orchestrate agents import -f agents/bill_payment_agent.yaml
uvx --from ibm-watsonx-orchestrate orchestrate agents import -f agents/lendyr_customer_care.yaml
```

## Test Scenarios

### Scenario 1: Manual Bill Payment (Happy Path)

**Objective**: Test manual entry of bill payment details

**Steps**:
1. Start chat with Lena (lendyr_customer_care agent)
2. Authenticate as Alice Martinez:
   - Phone: 555-0101
   - PIN: 1234
3. Say: "I need to pay a bill"
4. Provide payment details when prompted:
   - Payee: "ABC Electric Company"
   - Address: "123 Power Street, Energy City, CA 90210"
   - Amount: $150.00
   - Invoice number: "INV-2024-001"
5. Select account: "checking"
6. Confirm payment

**Expected Result**:
- Agent confirms payment processed
- Provides check number (format: CHK-{timestamp})
- Shows estimated delivery date
- Displays new account balance

**Sample Response**:
```
Payment confirmed! Check #CHK-1714234567 for $150.00 to ABC Electric Company 
has been scheduled. The check will be mailed to 123 Power Street, Energy City, 
CA 90210 and should arrive within 5-7 business days.

Your checking account has been debited. New balance: $2,850.00
```

### Scenario 2: Invoice Upload with PDF

**Objective**: Test document extraction from PDF invoice

**Steps**:
1. Authenticate as Alice Martinez (phone: 555-0101, PIN: 1234)
2. Say: "I want to pay this invoice"
3. Click the upload button (📎) in the chat interface
4. Upload a PDF invoice containing:
   ```
   INVOICE
   
   ABC Electric Company
   123 Power Street
   Energy City, CA 90210
   
   Invoice Number: INV-2024-001
   Due Date: February 15, 2024
   
   Amount Due: $150.00
   ```
5. Review the extracted information displayed in markdown table
6. Confirm details are correct
7. Select account: "checking"
8. Confirm payment

**Expected Result**:
- System displays formatted table with extracted data:
  | Item | Details |
  |------|---------|
  | Payee Name | ABC Electric Company |
  | Mailing Address | 123 Power Street, Energy City, CA 90210 |
  | Amount Due | $150.00 |
  | Invoice Number | INV-2024-001 |
  | Due Date | February 15, 2024 |
- Agent asks for confirmation and account selection
- Payment processes successfully with check number

### Scenario 3: Invoice Upload with Image

**Objective**: Test document extraction from image (phone photo)

**Steps**:
1. Authenticate as Alice Martinez
2. Say: "I need to pay this bill"
3. Upload a photo/image of an invoice (JPEG or PNG)
4. Review extracted information
5. Confirm and select account
6. Complete payment

**Expected Result**:
- Same as Scenario 2, but with image input
- Extraction should work with reasonable quality images

### Scenario 4: Insufficient Funds

**Objective**: Test error handling for insufficient balance

**Steps**:
1. Authenticate as Alice Martinez
2. Say: "I need to pay a bill"
3. Provide payment details:
   - Payee: "Large Payment Company"
   - Address: "456 Main St, City, CA 12345"
   - Amount: $50,000.00 (exceeds balance)
   - Account: "checking"
4. Confirm payment

**Expected Result**:
- Agent returns error message
- Shows available balance
- Does not process payment
- Example: "Insufficient funds. You have $3,000.00 available in your checking account."

### Scenario 5: Payment History

**Objective**: Test retrieval of payment history

**Steps**:
1. Authenticate as Alice Martinez
2. After making one or more payments, say: "Show me my bill payment history"

**Expected Result**:
- Agent displays list of previous bill payments
- Each entry shows:
  - Payee name
  - Amount
  - Check number
  - Status (processing/completed)
  - Date created

### Scenario 6: Incomplete Invoice Data

**Objective**: Test handling of documents with missing information

**Steps**:
1. Authenticate as Alice Martinez
2. Upload an invoice with incomplete information (e.g., missing address)
3. Review extracted data

**Expected Result**:
- Tool extracts available information
- Shows "Not found" for missing fields
- Agent asks customer to provide missing information manually
- Customer can provide missing details
- Payment proceeds normally

## Test Data

### Test Customer Accounts

**Alice Martinez (customer_id: 1)**
- Phone: 555-0101
- PIN: 1234
- Checking Account: ~$3,000 balance
- Savings Account: ~$5,000 balance

**Brian Nguyen (customer_id: 2)**
- Phone: 555-0102
- PIN: 5678
- Checking Account: ~$2,500 balance
- Savings Account: ~$10,000 balance

### Sample Invoice Content

Create a text file or PDF with this content for testing:

```
INVOICE

ABC Electric Company
123 Power Street
Energy City, CA 90210

Invoice Number: INV-2024-001
Account Number: 987654321
Due Date: February 15, 2024

Service Period: January 1-31, 2024

Amount Due: $150.00

Please remit payment to the address above.
```

## Verification Checklist

After each test scenario, verify:

- [ ] Authentication works correctly
- [ ] Agent routing (Lena → bill_payment_agent) is seamless
- [ ] Document upload button appears in UI
- [ ] Extraction tool returns formatted markdown table
- [ ] All extracted fields are displayed correctly
- [ ] Customer can confirm or correct information
- [ ] Account balance is checked before payment
- [ ] Payment creates transaction record
- [ ] Check number is generated (CHK-{timestamp} format)
- [ ] Confirmation message includes all details
- [ ] Error messages are clear and helpful

## Troubleshooting

### Issue: Upload button not visible
**Solution**: Verify `chat_with_docs.enabled: true` in lendyr_customer_care.yaml

### Issue: Extraction returns raw text instead of table
**Solution**: Verify extract_invoice_info tool is imported and Lena's instructions call it

### Issue: Tool not found error
**Solution**: 
```bash
uvx --from ibm-watsonx-orchestrate orchestrate tools list
# If missing, re-import the tool
```

### Issue: Agent not routing to bill_payment_agent
**Solution**: Check Lena's collaborators list includes bill_payment_agent

### Issue: API connection error
**Solution**: 
- Verify backend is running on port 8080
- Check API health endpoint: `curl http://localhost:8080/health`
- Review backend logs for errors

### Issue: Insufficient funds error when balance should be sufficient
**Solution**: 
- Check customer's actual account balance in database
- Verify correct account_type (checking vs savings) is being used

## API Testing (Optional)

Test backend endpoints directly:

### Create Bill Payment
```bash
curl -X POST http://localhost:8080/customers/by-id/1/bill-payments \
  -H "Content-Type: application/json" \
  -d '{
    "payee_name": "Test Company",
    "payee_address": "123 Test St, Test City, CA 12345",
    "amount": 100.00,
    "account_type": "checking",
    "invoice_number": "TEST-001"
  }'
```

### Get Payment History
```bash
curl http://localhost:8080/customers/by-id/1/bill-payments
```

## Success Criteria

The feature is working correctly when:

1. ✅ Manual bill payments process successfully
2. ✅ Document upload extracts information accurately
3. ✅ Extracted data displays in formatted markdown table
4. ✅ Insufficient funds errors are caught and reported
5. ✅ Payment history retrieves correctly
6. ✅ Check numbers are generated uniquely
7. ✅ Account balances update after payment
8. ✅ Agent routing works seamlessly
9. ✅ Error messages are clear and actionable
10. ✅ Both PDF and image uploads work

## Next Steps

After successful testing:

1. **Document any issues found** in GitHub issues or project tracker
2. **Gather user feedback** on the extraction accuracy
3. **Consider enhancements**:
   - Improve regex patterns for more invoice formats
   - Add support for recurring payments
   - Implement payment scheduling
   - Add payment status tracking
4. **Deploy to production** following deployment guide in BILL_PAYMENT_FEATURE.md

## Support

For questions or issues:
- Review main documentation: `docs/BILL_PAYMENT_FEATURE.md`
- Check agent logs: `orchestrate agents logs lendyr_customer_care`
- Review backend logs in terminal running uvicorn
- Test API endpoints directly to isolate issues