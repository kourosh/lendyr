# Customer Authentication System

## Overview

The Lendyr Bank customer care system now implements a secure two-factor authentication process using Customer ID and PIN before allowing access to any banking services.

## Authentication Flow

### 1. Customer Greeting
- Agent greets the customer and asks what they need help with
- Agent explains that authentication is required for security

### 2. Credential Collection
The agent collects two pieces of information:
- **Customer ID**: A 6-digit number (e.g., 846301, 846302, etc.)
- **PIN**: A 5-digit personal identification number

### 3. Validation
- The `authenticate_customer` tool validates the credentials against the database
- Returns customer email and name if successful
- Returns error message if credentials are invalid

### 4. Retry Logic
- Customers get **2 attempts** to authenticate
- After each failed attempt, the agent informs them and allows retry
- After 2 failed attempts, the customer is directed to call **1-800-LENDYR-1**

### 5. Post-Authentication
- Once authenticated, the customer's email is used for all subsequent API calls
- The agent routes requests to appropriate specialist agents

## Customer Data

### Current Customers with IDs and PINs

| Customer ID | Name              | Email                        | PIN   |
|-------------|-------------------|------------------------------|-------|
| 846301      | Alice Martinez    | alice.martinez@email.com     | 93810 |
| 846302      | Brian Nguyen      | brian.nguyen@email.com       | 24592 |
| 846303      | Carla Thompson    | carla.thompson@email.com     | 13278 |
| 846304      | David Kim         | david.kim@email.com          | 46048 |
| 846305      | Elena Okafor      | elena.okafor@email.com       | 42098 |
| 846306      | Frank Rossi       | frank.rossi@email.com        | 39256 |
| 846307      | Grace Patel       | grace.patel@email.com        | 28289 |
| 846308      | Henry Williams    | henry.williams@email.com     | 23434 |
| 846309      | Isabela Cruz      | isabela.cruz@email.com       | 98696 |
| 846310      | James Holloway    | james.holloway@email.com     | 81482 |

## Technical Implementation

### Authentication Tool
- **File**: `tools/customer_auth_tool.py`
- **Function**: `authenticate_customer()`
- **Input**: CustomerAuthInput (customer_id, pin)
- **Output**: CustomerAuthOutput (success, customer_email, customer_name, message)

### Database Schema
The CUSTOMERS table includes:
- `customer_id` (INTEGER) - Primary key
- `pin` (VARCHAR(5)) - 5-digit PIN
- `email` (VARCHAR) - Customer email
- `first_name`, `last_name` - Customer name

### Agent Configuration
- **Agent**: `lendyr_customer_care`
- **Tool**: `authenticate_customer`
- **Instructions**: Detailed authentication protocol in agent YAML

## Security Features

1. **Two-Factor Authentication**: Requires both Customer ID and PIN
2. **Attempt Limiting**: Maximum 2 authentication attempts
3. **Lockout Protection**: After 2 failed attempts, customer must call support
4. **No Email Exposure**: System uses Customer ID instead of email for initial contact
5. **Secure Database Validation**: Credentials validated against DB2 database

## Usage Example

```
Agent: Welcome to Lendyr Bank. I'm Lena. How can I help you today?
Customer: I'd like to check my account balance.
Agent: To help you securely, I'll need to verify your identity. What is your customer ID number?
Customer: 846301
Agent: Thank you. Now please provide your 5-digit PIN.
Customer: 93810
Agent: [Calls authenticate_customer tool]
Agent: Welcome, Alice Martinez! Authentication successful. Let me help you with your account balance...
```

## Failed Authentication Example

```
Agent: Welcome to Lendyr Bank. I'm Lena. How can I help you today?
Customer: Check my balance
Agent: To help you securely, I'll need to verify your identity. What is your customer ID number?
Customer: 846301
Agent: Thank you. Now please provide your 5-digit PIN.
Customer: 00000
Agent: [Calls authenticate_customer tool]
Agent: I'm sorry, that customer ID or PIN is incorrect. Let's try again. What is your customer ID number?
Customer: 846301
Agent: Thank you. Now please provide your 5-digit PIN.
Customer: 11111
Agent: [Calls authenticate_customer tool]
Agent: I'm sorry, but after 2 unsuccessful attempts, I cannot proceed. For security reasons, please call our support line at 1-800-LENDYR-1 for assistance.
```

## Deployment

### Import the Authentication Tool
```bash
orchestrate tools import -k python -f tools/customer_auth_tool.py
```

### Update the Agent
```bash
orchestrate agents update lendyr_customer_care -f agents/lendyr_customer_care.yaml
```

## Testing

Test the authentication tool locally:
```bash
cd tools
python3 customer_auth_tool.py
```

## Support Contact

For authentication issues or lockouts:
- **Phone**: 1-800-LENDYR-1
- **Support Hours**: 24/7

## Notes

- PINs are stored in the database and validated server-side
- The authentication system is deterministic and follows a strict protocol
- All authentication attempts are tracked within the conversation session
- The system does not use agentic workflows for authentication to ensure deterministic behavior