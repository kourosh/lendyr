# Account Opening Implementation Guide

## Overview

This implementation provides a streamlined account opening process for Lendyr Bank with a **dropdown menu for account type selection**. The solution uses a single Python tool with `Literal` type hints to display account types as a dropdown during parameter collection.

## Solution Architecture

### Approach: Single Tool with Literal Type

Instead of using Form Tools (which are in preview with known bugs), this implementation uses a standard Python tool with `Literal` type hints. This approach:

- ✅ Shows dropdown menu during parameter collection
- ✅ More reliable than preview FormWidget feature
- ✅ Simpler implementation and maintenance
- ✅ Handles all validation and PII masking
- ✅ Provides clear next steps for KYC compliance

## Files Created

### 1. Tool: `tools/open_account/open_account.py`
**Purpose**: Single tool that collects all account opening information with dropdown for account type

**Key Features**:
- Dropdown menu for 5 account types using `Literal` type
- Comprehensive validation (SSN, age, email, phone, address)
- Account-specific validation (deposits, employment, income)
- PII masking (SSN displayed as XXX-XX-1234)
- Application reference number generation
- KYC compliance messaging

**Account Types**:
1. `regular_checking` - Regular Checking
2. `premium_checking` - Premium Checking  
3. `savings` - Savings
4. `regular_credit_card` - Regular Credit Card
5. `travel_credit_card` - Travel Credit Card (Fiction Airlines Partnership)

### 2. Agent: `agents/account_opening_agent_v2.yaml`
**Purpose**: Orchestrates the account opening workflow

**Configuration**:
- Model: `groq/gpt-oss-120b` (GPT-OSS 120B via Groq)
- Tools: `open_account`
- Collaborators: `branch_locator_agent`

## How the Dropdown Works

When the agent calls the `open_account` tool, Orchestrate's UI automatically renders a dropdown menu for the `account_type` parameter because it uses `Literal` type:

```python
def open_account(
    account_type: Literal[
        "regular_checking", 
        "premium_checking", 
        "savings", 
        "regular_credit_card", 
        "travel_credit_card"
    ],
    # ... other parameters
)
```

The dropdown displays user-friendly labels:
- Regular Checking
- Premium Checking
- Savings
- Regular Credit Card
- Travel Credit Card with Fiction Airlines Partnership

## Information Collected

### Required for All Accounts
- **Personal Information**:
  - First name, last name
  - Social Security Number (XXX-XX-XXXX format)
  - Date of birth (YYYY-MM-DD, must be 18+)
  
- **Contact Information**:
  - Email address
  - Phone number ((XXX) XXX-XXXX format)
  
- **Address**:
  - Street address
  - City
  - State (2-letter code)
  - ZIP code (5 digits)

### Account-Specific Requirements

#### Checking Accounts (Regular & Premium)
- Initial deposit: Minimum $25

#### Savings Account
- Initial deposit: Minimum $100

#### Credit Cards (Regular & Travel)
- Employer name (required)
- Annual income (required, minimum $15,000 recommended)

#### Travel Credit Card Only
- Fiction Airlines frequent flyer number (optional, format: FA123456789)

## Validation Rules

### Format Validation
- **SSN**: Must match `XXX-XX-XXXX` pattern
- **Date of Birth**: Must be valid date in `YYYY-MM-DD` format
- **Age**: Must be 18 or older
- **Email**: Must be valid email format
- **Phone**: Must match `(XXX) XXX-XXXX` pattern
- **State**: Must be 2-letter code
- **ZIP Code**: Must be 5 digits
- **Frequent Flyer**: Must match `FA123456789` pattern (if provided)

### Business Rules
- Checking accounts: Minimum $25 initial deposit
- Savings accounts: Minimum $100 initial deposit
- Credit cards: Employer and income required
- Credit cards: Income below $15,000 triggers warning
- All accounts: In-branch verification required for KYC compliance

## Response Structure

### Success Response
```json
{
  "status": "pending_verification",
  "reference_number": "APP-20260508-1234",
  "account_type": "Regular Checking",
  "applicant_name": "John Doe",
  "masked_ssn": "XXX-XX-1234",
  "email": "john.doe@example.com",
  "phone": "(555) 123-4567",
  "address": "123 Main St, San Francisco, CA 94102",
  "initial_deposit": "$100.00",
  "warnings": [],
  "message": "Application submitted successfully! Reference number: APP-20260508-1234",
  "next_steps": [
    "Your application has been received and validated",
    "For security and compliance, account opening requires in-branch verification",
    "Please visit a Lendyr Bank branch with:",
    "  - Valid government-issued photo ID (driver's license or passport)",
    "  - Social Security card or official document with your SSN",
    "  - Proof of address (utility bill, lease agreement, or bank statement)",
    "  - Initial deposit of $100.00",
    "Branch staff will complete your application and activate your account",
    "Would you like help finding the nearest Lendyr Bank branch?"
  ],
  "kyc_required": true,
  "documents_needed": [
    "Government-issued photo ID",
    "Social Security card or document",
    "Proof of address"
  ]
}
```

### Validation Error Response
```json
{
  "status": "validation_failed",
  "account_type": "Regular Checking",
  "errors": [
    "SSN must be in format XXX-XX-XXXX",
    "You must be at least 18 years old to open an account"
  ],
  "warnings": [],
  "message": "Please correct the following errors and try again."
}
```

## Security & Compliance

### PII Handling
- **SSN Masking**: SSN is masked in all responses as `XXX-XX-XXXX` (only last 4 digits shown)
- **Validation Only**: Tool validates format but doesn't store or transmit full SSN
- **Secure Display**: Masked SSN used in all user-facing messages

### KYC Compliance
All account openings require **in-branch verification** with:
1. Government-issued photo ID (driver's license or passport)
2. Social Security card or official document with SSN
3. Proof of address (utility bill, lease, or bank statement)
4. Initial deposit (if applicable)

This ensures compliance with:
- Bank Secrecy Act (BSA)
- USA PATRIOT Act
- Customer Identification Program (CIP) requirements

## Deployment

### 1. Import the Tool
```bash
orchestrate tools import \
  -k python \
  -f tools/open_account/open_account.py
```

### 2. Import the Agent
```bash
orchestrate agents import \
  -f agents/account_opening_agent_v2.yaml
```

### 3. Verify Deployment
```bash
# List tools
orchestrate tools list

# List agents
orchestrate agents list

# Test the agent
orchestrate agents test account_opening_agent_v2
```

## Testing Scenarios

### Test Case 1: Regular Checking Account
**Input**:
- Account type: Regular Checking
- Name: John Doe
- SSN: 123-45-6789
- DOB: 1990-01-15
- Email: john.doe@example.com
- Phone: (555) 123-4567
- Address: 123 Main St, San Francisco, CA 94102
- Initial deposit: $100

**Expected**: Success with reference number and next steps

### Test Case 2: Validation Errors
**Input**:
- Account type: Savings
- SSN: 12345678 (invalid format)
- DOB: 2010-01-01 (under 18)
- Initial deposit: $50 (below minimum)

**Expected**: Validation errors for SSN format, age, and deposit amount

### Test Case 3: Travel Credit Card
**Input**:
- Account type: Travel Credit Card
- Complete personal info
- Employer: Tech Corp
- Annual income: $75,000
- Frequent flyer: FA123456789

**Expected**: Success with travel benefits listed

### Test Case 4: Credit Card - Low Income Warning
**Input**:
- Account type: Regular Credit Card
- Annual income: $12,000

**Expected**: Warning about income below $15,000

### Test Case 5: Branch Locator Integration
**Input**: Successful application
**Expected**: Agent offers to find nearest branch using branch_locator_agent

## Integration with Branch Locator

After successful application submission, the agent offers to help find the nearest Lendyr Bank branch:

```
Agent: "Would you like help finding the nearest Lendyr Bank branch?"
User: "Yes, I'm in San Francisco"
Agent: [Calls branch_locator_agent collaborator]
```

The branch locator agent will:
1. Get user's location
2. Find nearest branches
3. Provide addresses and directions

## Advantages of This Approach

### vs. Form Tools
- ✅ **More Reliable**: No preview feature bugs
- ✅ **Simpler**: Single tool instead of form + processor
- ✅ **Better UX**: Dropdown appears during natural parameter collection
- ✅ **Easier Maintenance**: One file to update

### vs. Manual Collection
- ✅ **Dropdown Menu**: Account types shown as dropdown
- ✅ **Validation**: All validation in one place
- ✅ **Consistency**: Same validation logic for all account types
- ✅ **Error Handling**: Clear error messages

## Troubleshooting

### Dropdown Not Appearing
**Issue**: Account type not showing as dropdown
**Solution**: Verify `Literal` type is used correctly in function signature

### Validation Errors
**Issue**: Valid data rejected
**Solution**: Check regex patterns match expected formats

### Agent Not Calling Tool
**Issue**: Agent describes process instead of calling tool
**Solution**: Update agent instructions to emphasize tool usage

### Branch Locator Not Working
**Issue**: Can't find branches after application
**Solution**: Verify branch_locator_agent is deployed and listed as collaborator

## Future Enhancements

1. **Database Integration**: Store applications in database
2. **Email Notifications**: Send confirmation emails
3. **Document Upload**: Allow document pre-upload
4. **Appointment Scheduling**: Integrate with branch scheduling system
5. **Credit Check Integration**: Real-time credit checks for credit cards
6. **Fraud Detection**: Add fraud detection rules
7. **Multi-language Support**: Support multiple languages

## Support

For issues or questions:
1. Check agent logs: `orchestrate agents logs account_opening_agent_v2`
2. Verify tool deployment: `orchestrate tools list`
3. Test tool directly: `orchestrate tools test open_account`
4. Review validation errors in tool response

## Summary

This implementation provides a production-ready account opening solution with:
- ✅ Dropdown menu for account type selection
- ✅ Comprehensive validation and PII handling
- ✅ KYC compliance messaging
- ✅ Integration with branch locator
- ✅ Clear next steps for customers
- ✅ Reliable, maintainable code

The solution handles all 5 account types with appropriate validation and provides a smooth user experience from initial inquiry to branch visit scheduling.