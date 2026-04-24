# Money Transfer Use Case - Backup

This folder contains the complete money transfer use case components for Lendyr Bank.

## Components

### Agent
- **transfer_agent.yaml** - Specialist agent that handles money transfers between customer accounts

### Tools
1. **transfer_money_by_customer_id/** - Executes money transfers
   - API: `POST /customers/by-id/{customer_id}/transfer`
   - Supports regular transfers (checking ↔ savings)
   - Supports bill payments (checking/savings → credit/loan)
   - Validates sufficient funds
   - Returns detailed confirmation with updated balances

2. **get_accounts_by_customer_id/** - Retrieves all customer accounts
   - Returns checking, savings, credit, and loan accounts
   - Shows current balances for validation

3. **get_transfers_by_customer_id/** - Retrieves transfer history
   - Shows all inbound and outbound transfers
   - Useful for transaction history

## Transfer Flow

1. Customer requests transfer via `lendyr_customer_care` agent
2. Routes to `transfer_agent`
3. Agent gets account balances using `get_accounts_by_customer_id`
4. Validates and executes transfer using `transfer_money_by_customer_id`
5. Confirms completion with updated balances

## Transfer Types

- **Regular Transfer**: Move money between checking and savings accounts
- **Bill Payment**: Pay credit card or loan from checking/savings

## API Details

### Transfer Request
```json
{
  "from_account_type": "checking",
  "to_account_type": "savings",
  "amount": 500.00,
  "description": "Monthly savings"
}
```

### Success Response
```json
{
  "success": true,
  "transfer_type": "transfer",
  "customer_name": "John Doe",
  "transfer_details": {
    "from_account": {
      "type": "checking",
      "account_number": "****1234",
      "previous_balance": 1500.00,
      "new_balance": 1000.00
    },
    "to_account": {
      "type": "savings",
      "account_number": "****5678",
      "previous_balance": 2000.00,
      "new_balance": 2500.00
    },
    "amount": 500.00,
    "timestamp": "2024-04-24T15:30:00Z"
  }
}
```

### Insufficient Funds Response
```json
{
  "success": false,
  "error": "insufficient_funds",
  "message": "Insufficient funds in checking account",
  "available_balance": 300.00,
  "requested_amount": 500.00,
  "suggestion": "You can transfer up to $300.00"
}
```

## Backup Date
Created: 2024-04-24