# Money Transfer Feature

## Overview
The Money Transfer feature allows customers to safely transfer money between their own accounts with comprehensive validation, balance checking, and special handling for bill payments.

---

## Features

### 1. Regular Transfers
Transfer money between checking and savings accounts:
- **Checking → Savings**: Move money to savings
- **Savings → Checking**: Move money to checking
- Both accounts update normally (decrease source, increase destination)

### 2. Bill Payments
Pay credit cards or loans from checking/savings:
- **Checking/Savings → Credit**: Pay down credit card balance
- **Checking/Savings → Loan**: Make loan payment
- Reduces the debt on the credit/loan account

### 3. Insufficient Funds Handling
Smart handling when customer doesn't have enough money:
- Shows available balance
- Offers to transfer available amount instead
- Allows customer to cancel or adjust amount
- Clear, empathetic messaging

---

## Components

### Backend API Endpoint
**Endpoint**: `POST /customers/by-id/{customer_id}/transfer`

**Request Body**:
```json
{
  "from_account_type": "checking",
  "to_account_type": "savings",
  "amount": 500.00,
  "description": "Monthly savings transfer"
}
```

**Success Response**:
```json
{
  "success": true,
  "transfer_type": "transfer",
  "customer_name": "Alice Martinez",
  "transfer_details": {
    "from_account": {
      "type": "checking",
      "account_number": "CHK-001",
      "previous_balance": 1000.00,
      "new_balance": 500.00
    },
    "to_account": {
      "type": "savings",
      "account_number": "SAV-001",
      "previous_balance": 250.00,
      "new_balance": 750.00
    },
    "amount": 500.00,
    "description": "Monthly savings transfer",
    "timestamp": "2024-01-15 14:30:00"
  },
  "message": "Successfully transferred $500.00 from checking to savings"
}
```

**Insufficient Funds Response**:
```json
{
  "success": false,
  "error": "insufficient_funds",
  "message": "Insufficient funds. You have $300.00 available in your checking account.",
  "available_balance": 300.00,
  "requested_amount": 500.00,
  "suggestion": "Would you like to transfer $300.00 instead?"
}
```

### Transfer Agent
**Agent**: `transfer_agent`

**Responsibilities**:
1. Get customer's account balances
2. Understand transfer intent
3. Validate sufficient funds
4. Confirm with customer before executing
5. Handle insufficient funds gracefully
6. Execute transfer
7. Provide clear confirmation

**Tools Used**:
- `get_accounts_by_customer_id` - View all accounts
- `transfer_money_by_customer_id` - Execute transfer

---

## Usage Examples

### Example 1: Successful Regular Transfer

**Customer**: "Transfer $200 from checking to savings"

**Agent Flow**:
1. Gets accounts: Checking $500, Savings $250
2. Confirms: "I'll transfer $200 from checking to savings. Checking will have $300, savings will have $450. Should I proceed?"
3. Customer: "Yes"
4. Executes transfer
5. Confirms: "Done! $200 transferred. Checking: $300, Savings: $450"

### Example 2: Insufficient Funds

**Customer**: "Transfer $1000 from checking to savings"

**Agent Flow**:
1. Gets accounts: Checking $500, Savings $250
2. Attempts transfer
3. Receives insufficient funds response
4. Informs: "You have $500 available in your checking account. Would you like to transfer $500 instead, or would you like to cancel?"
5. Customer: "Transfer $500"
6. Executes transfer with $500
7. Confirms: "Done! $500 transferred. Checking: $0, Savings: $750"

### Example 3: Bill Payment

**Customer**: "Pay $300 on my credit card from checking"

**Agent Flow**:
1. Gets accounts: Checking $1000, Credit $1500 (owed)
2. Confirms: "I'll pay $300 toward your credit card from checking. This will reduce your credit card balance from $1,500 to $1,200. Should I proceed?"
3. Customer: "Yes"
4. Executes bill payment
5. Confirms: "Done! $300 payment processed. Your credit card balance is now $1,200"

### Example 4: Voice Channel (Concise)

**Customer**: "Move $100 from checking to savings"

**Agent**: "I'll transfer $100 from checking to savings. Your checking will have $400 and savings will have $350. Proceed?"

**Customer**: "Yes"

**Agent**: "Done! Checking: $400, Savings: $350"

---

## Validation Rules

### Pre-Transfer Validation
1. ✅ Customer must exist
2. ✅ Source account must exist and belong to customer
3. ✅ Destination account must exist and belong to customer
4. ✅ Amount must be greater than $0
5. ✅ Source and destination must be different account types
6. ✅ Source account must have sufficient funds

### Transfer Type Detection
- **Regular Transfer**: Both accounts are checking or savings
- **Bill Payment**: Destination is credit or loan

### Balance Updates
- **Regular Transfer**: 
  - Source: balance - amount
  - Destination: balance + amount
- **Bill Payment**:
  - Source: balance - amount
  - Destination (credit/loan): balance - amount (reduces debt)

---

## Error Handling

### Insufficient Funds
- **Detection**: Source balance < requested amount
- **Response**: Show available balance and offer alternatives
- **User Options**: Transfer available amount, cancel, or specify different amount

### Invalid Accounts
- **Missing Account**: "Your [account_type] account was not found"
- **Same Account**: "Cannot transfer to the same account type"

### System Errors
- **API Failure**: "I apologize, but I'm having trouble processing your transfer right now. Please try again in a moment, or call us at 1-800-LENDYR-1 for immediate assistance."

---

## Testing Scenarios

### Test Case 1: Regular Transfer - Success
- **Setup**: Alice has $500 in checking, $250 in savings
- **Action**: Transfer $200 from checking to savings
- **Expected**: Success, checking=$300, savings=$450

### Test Case 2: Insufficient Funds - Offer Alternative
- **Setup**: Alice has $500 in checking, $250 in savings
- **Action**: Transfer $1000 from checking to savings
- **Expected**: Insufficient funds message, offer to transfer $500

### Test Case 3: Bill Payment - Credit Card
- **Setup**: Alice has $1000 in checking, $1500 credit card balance
- **Action**: Pay $300 on credit card from checking
- **Expected**: Success, checking=$700, credit=$1200

### Test Case 4: Bill Payment - Loan
- **Setup**: Alice has $1000 in checking, $15000 loan balance
- **Action**: Pay $500 on loan from checking
- **Expected**: Success, checking=$500, loan=$14500

### Test Case 5: Same Account Transfer
- **Setup**: Alice has $500 in checking
- **Action**: Transfer $100 from checking to checking
- **Expected**: Error - cannot transfer to same account

---

## Integration Points

### Main Customer Care Agent
The transfer agent is integrated into the main customer care flow:

**Routing Logic**:
```yaml
- Call transfer_agent when customer wants to:
  - Transfer money between accounts
  - Move money from checking to savings
  - Pay credit card or loan from checking/savings
  - Move funds between their accounts
```

### Context Variables
- **Input**: `customer_id` (from authentication)
- **Automatic**: Customer ID flows through context to all tools

---

## Voice Channel Optimization

The transfer agent is optimized for voice interactions:

### Concise Responses
- ✅ "I'll transfer $200 from checking to savings. Checking will have $300, savings $450. Proceed?"
- ❌ "I will now initiate a transfer of two hundred dollars from your checking account..."

### Natural Language
- ✅ "You have $500 available"
- ❌ "Your available balance is five hundred dollars and zero cents"

### Clear Confirmations
- ✅ "Done! Checking: $300, Savings: $450"
- ❌ "The transfer has been successfully completed. Your new checking account balance is..."

---

## Security Considerations

1. **Authentication Required**: Customer must be authenticated before any transfer
2. **Own Accounts Only**: Can only transfer between own accounts
3. **Balance Validation**: Always checks sufficient funds
4. **Confirmation Required**: Agent confirms before executing
5. **Audit Trail**: Creates transaction records for both accounts
6. **No External Transfers**: Cannot transfer to other customers

---

## Future Enhancements

Potential future improvements:
1. **Scheduled Transfers**: Set up recurring transfers
2. **Transfer Limits**: Daily/monthly transfer limits
3. **Transfer History**: View past transfers
4. **External Transfers**: Transfer to other banks (ACH)
5. **Split Transfers**: Transfer to multiple accounts at once
6. **Transfer Templates**: Save common transfer patterns

---

## Files Modified/Created

### New Files
1. `lendyr_code_engine/main.py` - Added transfer endpoint
2. `tools/transfer_money_by_customer_id/lendyr_openapi.json` - Tool definition
3. `agents/transfer_agent.yaml` - Transfer specialist agent
4. `docs/MONEY_TRANSFER_FEATURE.md` - This documentation

### Modified Files
1. `agents/lendyr_customer_care.yaml` - Added transfer_agent to collaborators
2. `scripts/import_local_with_context_fix.sh` - Added new tool and agent

---

## Quick Start

### Deploy to Local Environment
```bash
cd /Users/kk76/Public/lendyr
bash scripts/import_local_with_context_fix.sh
```

### Test the Feature
```bash
orchestrate agents run lendyr_customer_care --input 'Hi, I need help'
```

Then:
1. Authenticate with customer ID 846301 and PIN 12345
2. Say: "Transfer $200 from checking to savings"
3. Confirm the transfer
4. Verify the new balances

---

## Support

For issues or questions:
- **Technical Issues**: Check logs in lendyr_code_engine
- **Agent Behavior**: Review transfer_agent.yaml instructions
- **API Issues**: Test endpoint directly with curl/Postman
- **Emergency**: Call 1-800-LENDYR-1

---

*Last Updated: 2024-01-15*
*Version: 1.0.0*