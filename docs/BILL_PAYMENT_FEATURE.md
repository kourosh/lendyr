# Bill Payment via Check Feature

## Overview

The Bill Payment feature allows Lendyr Bank customers to pay bills to external companies or individuals via check mailing service. The system includes document extraction capabilities that can automatically extract payment information from uploaded invoices (PDF or images).

## Architecture

### Components

1. **Customer Care Agent** (`agents/lendyr_customer_care.yaml`)
   - Main entry point with document upload capability via `chat_with_docs`
   - Calls `extract_invoice_info` Python tool to process uploaded documents
   - Routes to bill_payment_agent after customer confirmation
   - Maintains customer authentication context

2. **Bill Payment Agent** (`agents/bill_payment_agent.yaml`)
   - Handles bill payment processing
   - Validates payment details with customers
   - Verifies sufficient funds
   - Processes payments through the bill payment tool

3. **Invoice Extraction Tool** (`tools/extract_invoice_info/extract_invoice_info.py`)
   - Python tool with @tool decorator
   - Extracts payment information from raw document text
   - Returns formatted markdown table
   - Handles missing or incomplete data gracefully

4. **Bill Payment Tool** (`tools/create_bill_payment/lendyr_openapi.json`)
   - OpenAPI specification for bill payment endpoints
   - Supports creating and retrieving bill payments
   - Integrates with customer accounts via `customer_id` context

5. **Backend API Endpoints** (`lendyr_code_engine/main.py`)
   - `POST /customers/by-id/{customer_id}/bill-payments` - Create bill payment
   - `GET /customers/by-id/{customer_id}/bill-payments` - Get payment history

## Features

### 1. Manual Bill Payment

Customers can manually provide payment details:
- Payee name
- Payee address (street, city, state, ZIP)
- Payment amount
- Account to pay from (checking or savings)
- Optional: Invoice number, memo, delivery date

### 2. Invoice Document Extraction

Customers can upload invoices in PDF or image format, and the system will:
- Extract payee name and address
- Extract payment amount
- Extract invoice/account number
- Extract due date (if available)
- Present extracted information for customer confirmation

### 3. Payment Processing

The system:
- Validates sufficient funds in the customer's account
- Debits the payment amount from the specified account
- Generates a unique payment ID and check number
- Provides estimated delivery date (5-7 business days)
- Creates transaction records for audit trail

## Document Extraction Implementation

The system uses a two-stage approach for document processing:

### Stage 1: Document Upload (chat_with_docs)
The customer care agent has `chat_with_docs` enabled for document upload:

```yaml
chat_with_docs:
  enabled: true
  generation:
    enabled: false  # Generation disabled - we use Python tool instead
```

This provides the upload button in the UI and extracts raw text from PDFs and images.

### Stage 2: Information Extraction (Python Tool)
The `extract_invoice_info` Python tool processes the raw text:

```python
@tool
def extract_invoice_info(document_text: str) -> str:
    """
    Extracts payment information from invoice text.
    
    Uses regex patterns to extract:
    - Payee name (company name)
    - Mailing address (street, city, state, zip)
    - Amount due
    - Invoice number
    - Due date
    
    Returns formatted markdown table with extracted data.
    """
```

**Key Design Decision**: We disabled `chat_with_docs` generation and use a Python tool instead because:
- Full control over output formatting
- Consistent markdown table structure
- Better error handling for missing fields
- Easier to test and debug extraction logic

### Supported Document Formats
- PDF files
- Image files (JPEG, PNG)
- Photos taken by phone

### Extraction Fields
- **Payee Name**: Company or person to pay
- **Payee Address**: Full mailing address (street, city, state, ZIP)
- **Amount Due**: Payment amount
- **Invoice Number**: Account or invoice number
- **Due Date**: Payment due date (if available)

## API Endpoints

### Create Bill Payment

**Endpoint**: `POST /customers/by-id/{customer_id}/bill-payments`

**Request Body**:
```json
{
  "payee_name": "Electric Company",
  "payee_address": {
    "street": "123 Power St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94102"
  },
  "amount": 150.00,
  "account_type": "checking",
  "invoice_number": "INV-2024-001",
  "memo": "January electricity bill",
  "delivery_date": "2024-02-15"
}
```

**Response**:
```json
{
  "success": true,
  "payment_id": "BP123456",
  "status": "processing",
  "check_number": "CHK12345",
  "estimated_delivery": "2024-02-15",
  "amount": 150.00,
  "payee_name": "Electric Company",
  "account_debited": {
    "account_type": "checking",
    "account_number": "****1234",
    "new_balance": 2850.00
  },
  "message": "Bill payment of $150.00 to Electric Company has been scheduled. Check #CHK12345 will be mailed and should arrive by 2024-02-15.",
  "created_at": "2024-02-08 10:30:00"
}
```

### Get Bill Payment History

**Endpoint**: `GET /customers/by-id/{customer_id}/bill-payments?status=processing`

**Response**:
```json
[
  {
    "payment_id": "BP123456",
    "payee_name": "Electric Company",
    "amount": 150.00,
    "status": "processing",
    "check_number": "CHK12345",
    "created_at": "2024-02-08 10:30:00",
    "estimated_delivery": "2024-02-15"
  }
]
```

## User Workflows

### Workflow 1: Manual Bill Payment

1. Customer authenticates with Lendyr customer care agent
2. Customer requests to pay a bill
3. Customer care agent routes to bill_payment_agent
4. Bill payment agent asks for payment details:
   - Payee name
   - Payee address
   - Amount
   - Account to pay from
5. Agent verifies sufficient funds
6. Agent confirms details with customer
7. Agent processes payment
8. Customer receives confirmation with check number and delivery date

### Workflow 2: Invoice Upload Payment

1. Customer authenticates with Lendyr customer care agent
2. Customer uploads invoice (PDF or image) via upload button
3. Orchestrate's `chat_with_docs` extracts raw text from document
4. Customer care agent calls `extract_invoice_info` tool with raw text
5. Python tool extracts and formats payment information:
   - Payee name
   - Payee address
   - Amount due
   - Invoice number
   - Due date
6. Agent displays formatted markdown table to customer
7. Customer confirms or corrects details and selects account
8. Customer care agent routes to bill_payment_agent with payment details
9. Bill payment agent verifies sufficient funds
10. Bill payment agent processes payment
11. Customer receives confirmation with check number and delivery date

## Error Handling

### Insufficient Funds
```json
{
  "success": false,
  "error": "insufficient_funds",
  "message": "Insufficient funds. You have $100.00 available in your checking account.",
  "available_balance": 100.00
}
```

### Missing Document Information
If the agent cannot extract required information from an uploaded document, it will:
1. Display the `idk_message`: "I was unable to extract that information from the document."
2. Ask the customer to provide the missing information manually

### Invalid Address
The system validates that all required address fields are present:
- street
- city
- state (2-letter code)
- zip

## Security Considerations

1. **Authentication Required**: All bill payment operations require customer authentication via customer_id context
2. **Account Validation**: System verifies customer owns the account before debiting
3. **Sufficient Funds Check**: Validates available balance before processing payment
4. **Transaction Audit Trail**: All payments create transaction records
5. **Document Session Scope**: Uploaded documents are only available during the chat session and are not stored permanently

## Testing

### Test Scenarios

1. **Manual Payment - Success**
   - Provide valid payment details
   - Verify sufficient funds
   - Confirm payment creation

2. **Manual Payment - Insufficient Funds**
   - Attempt payment exceeding account balance
   - Verify error message with available balance

3. **Invoice Upload - PDF**
   - Upload sample invoice PDF
   - Verify extraction of all fields
   - Confirm payment after extraction

4. **Invoice Upload - Image**
   - Upload photo of invoice
   - Verify extraction works with image format
   - Confirm payment after extraction

5. **Invoice Upload - Missing Information**
   - Upload document with incomplete information
   - Verify agent asks for missing details
   - Complete payment with manual input

## Deployment

### Prerequisites
- Orchestrate ADK installed
- Backend API deployed with bill payment endpoints
- Customer authentication configured

### Import Steps

1. **Import Bill Payment Tool**:
   ```bash
   uvx --from ibm-watsonx-orchestrate orchestrate tools import -k openapi -f tools/create_bill_payment/lendyr_openapi.json
   ```

2. **Import Invoice Extraction Tool**:
   ```bash
   uvx --from ibm-watsonx-orchestrate orchestrate tools import -k python -f tools/extract_invoice_info/extract_invoice_info.py
   ```

3. **Import Bill Payment Agent**:
   ```bash
   uvx --from ibm-watsonx-orchestrate orchestrate agents import -f agents/bill_payment_agent.yaml
   ```

4. **Update Customer Care Agent**:
   ```bash
   uvx --from ibm-watsonx-orchestrate orchestrate agents import -f agents/lendyr_customer_care.yaml
   ```

4. **Deploy Backend API**:
   - Ensure bill payment endpoints are deployed
   - Verify database connectivity
   - Test API endpoints

### Verification

1. Test authentication flow
2. Test manual bill payment
3. Test invoice upload and extraction
4. Verify transaction records in database
5. Check payment history retrieval

## Future Enhancements

1. **Payment Scheduling**: Allow customers to schedule future payments
2. **Recurring Payments**: Set up automatic recurring bill payments
3. **Payment Tracking**: Real-time tracking of check delivery status
4. **Multiple Payees**: Batch payment to multiple payees
5. **Payment Templates**: Save frequently used payee information
6. **Electronic Payments**: Add ACH/wire transfer options alongside checks
7. **Payment Reminders**: Notify customers of upcoming due dates
8. **Payment History Analytics**: Spending insights by payee category

## Support

For issues or questions:
- Check the Orchestrate documentation: https://developer.watson-orchestrate.ibm.com
- Review agent logs for debugging
- Verify API endpoint connectivity
- Ensure customer authentication is working correctly

## Technical Notes

### Why Python Tool Instead of chat_with_docs Generation?

During development, we discovered that `chat_with_docs` generation feature:
- Returns raw JSON text instead of following generation prompt instructions
- Designed primarily for Q&A, not structured data extraction
- Limited control over output formatting

The Python tool approach provides:
- Full control over extraction logic and output format
- Consistent markdown table formatting
- Better error handling for edge cases
- Easier testing and debugging
- Ability to use regex patterns for precise extraction

### Tool Import Warning

When importing the Python tool, you may see:
```
[WARNING] - Unable to properly parse parameter descriptions due to missing or incorrect type hints.
```

This warning is non-critical. The tool will function correctly. It occurs because the tool uses a simple string parameter without complex type hints.

## Changelog

### Version 1.0.0 (2024-02-08)
- Initial release
- Manual bill payment support
- Invoice document extraction (PDF and images) via Python tool
- Integration with customer care agent
- Payment history tracking
- Custom extraction tool with regex-based parsing