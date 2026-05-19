# Account Opening Implementation - Testing Guide

## Overview
This guide provides step-by-step instructions for testing the new account opening feature with dropdown menu functionality.

## Prerequisites
- IBM watsonx Orchestrate ADK installed
- Access to watsonx Orchestrate environment
- Orchestrate CLI configured

## Deployment Steps

### 1. Import All Assets
Run the import script to deploy all tools and agents:

```bash
cd /Users/kk76/Public/lendyr
./scripts/import_all_assets.sh
```

This will automatically import:
- `show_account_opening_form` tool (Python)
- `process_account_application` tool (Python)
- `account_opening_agent` agent (YAML)

### 2. Verify Import Success
Check that the tools were imported successfully:

```bash
orchestrate tools list | grep -E "show_account_opening_form|process_account_application"
```

Check that the agent was imported:

```bash
orchestrate agents list | grep account_opening_agent
```

## Testing Checklist

### Test 1: Form Display with Dropdown
**Objective:** Verify that the account type dropdown appears immediately when user requests to open an account.

**Steps:**
1. Start a conversation with the `account_opening_agent`
2. Say: "I want to open a new account"
3. **Expected Result:** 
   - Agent immediately calls `show_account_opening_form` tool
   - Form displays with a **dropdown menu** for account type selection
   - Dropdown shows 5 options:
     - Regular Checking
     - Premium Checking
     - Savings
     - Regular Credit Card
     - Travel Credit Card (Fiction Airlines Partnership)

**Success Criteria:**
- ✅ Dropdown appears without agent asking questions first
- ✅ All 5 account types are visible in dropdown
- ✅ Form includes all required fields

### Test 2: Regular Checking Account
**Objective:** Test opening a regular checking account with minimum deposit.

**Test Data:**
- Account Type: Regular Checking
- First Name: John
- Last Name: Doe
- SSN: 123-45-6789
- Date of Birth: 1990-01-15
- Email: john.doe@example.com
- Phone: (555) 123-4567
- Street Address: 123 Main Street
- City: San Francisco
- State: CA
- ZIP Code: 94102
- Initial Deposit: $25.00

**Expected Result:**
- ✅ Application validates successfully
- ✅ SSN is masked as XXX-XX-6789
- ✅ Reference number generated (format: APP-YYYYMMDD-XXXX)
- ✅ Next steps include in-branch verification requirement
- ✅ Agent offers to help find nearest branch

### Test 3: Premium Checking Account
**Objective:** Test premium checking with higher deposit.

**Test Data:**
- Account Type: Premium Checking
- (Use same personal info as Test 2)
- Initial Deposit: $100.00

**Expected Result:**
- ✅ Application validates successfully
- ✅ Premium checking specific features mentioned
- ✅ Minimum deposit requirement met

### Test 4: Savings Account
**Objective:** Test savings account with minimum deposit validation.

**Test Data:**
- Account Type: Savings
- (Use same personal info as Test 2)
- Initial Deposit: $50.00 (below minimum)

**Expected Result:**
- ❌ Validation error: "Savings account requires a minimum initial deposit of $100"
- ✅ User prompted to correct and resubmit

**Then test with correct amount:**
- Initial Deposit: $100.00

**Expected Result:**
- ✅ Application validates successfully

### Test 5: Regular Credit Card
**Objective:** Test credit card application with employment validation.

**Test Data:**
- Account Type: Regular Credit Card
- (Use same personal info as Test 2)
- Initial Deposit: $0 (not required for credit cards)
- Employer: Acme Corporation
- Annual Income: $50,000

**Expected Result:**
- ✅ Application validates successfully
- ✅ Credit check requirement mentioned
- ✅ Employer and income information included in response

### Test 6: Travel Credit Card with Fiction Airlines
**Objective:** Test travel credit card with frequent flyer integration.

**Test Data:**
- Account Type: Travel Credit Card (Fiction Airlines Partnership)
- (Use same personal info as Test 2)
- Employer: Tech Innovations Inc
- Annual Income: $75,000
- Frequent Flyer Number: FA123456789

**Expected Result:**
- ✅ Application validates successfully
- ✅ Frequent flyer number linked
- ✅ Travel benefits listed:
  - 2x miles on Fiction Airlines purchases
  - 1.5x miles on all other purchases
  - Priority boarding
  - Free checked bag

### Test 7: PII Validation - Invalid SSN
**Objective:** Test SSN format validation.

**Test Data:**
- SSN: 123456789 (missing dashes)

**Expected Result:**
- ❌ Validation error: "SSN must be in format XXX-XX-XXXX"

### Test 8: Age Validation
**Objective:** Test minimum age requirement.

**Test Data:**
- Date of Birth: 2010-01-01 (under 18)

**Expected Result:**
- ❌ Validation error: "You must be at least 18 years old to open an account"

### Test 9: Email Validation
**Objective:** Test email format validation.

**Test Data:**
- Email: invalid-email (no @ or domain)

**Expected Result:**
- ❌ Validation error: "Invalid email address format"

### Test 10: Phone Validation
**Objective:** Test phone format validation.

**Test Data:**
- Phone: 5551234567 (missing formatting)

**Expected Result:**
- ❌ Validation error: "Phone must be in format (XXX) XXX-XXXX"

### Test 11: Credit Card - Missing Employment Info
**Objective:** Test required fields for credit card applications.

**Test Data:**
- Account Type: Regular Credit Card
- Employer: (empty)
- Annual Income: $0

**Expected Result:**
- ❌ Validation errors:
  - "Employer name is required for credit card applications"
  - "Annual income is required for credit card applications"

### Test 12: Low Income Warning
**Objective:** Test income warning for credit cards.

**Test Data:**
- Account Type: Regular Credit Card
- Annual Income: $12,000

**Expected Result:**
- ⚠️ Warning: "Annual income below $15,000 may affect credit card approval"
- ✅ Application still processes (warning, not error)

### Test 13: Branch Locator Integration
**Objective:** Test integration with branch locator agent.

**Steps:**
1. Complete an account application successfully
2. When agent asks "Would you like help finding the nearest Lendyr Bank branch?"
3. Respond: "Yes, please"

**Expected Result:**
- ✅ Agent routes to `branch_locator_agent`
- ✅ Branch locator asks for location
- ✅ Returns nearest branch information

### Test 14: Multiple Applications in Same Session
**Objective:** Test opening multiple accounts in one conversation.

**Steps:**
1. Complete first application (e.g., Regular Checking)
2. Say: "I also want to open a savings account"
3. Complete second application

**Expected Result:**
- ✅ Form displays again with dropdown
- ✅ Both applications processed independently
- ✅ Different reference numbers generated

### Test 15: Dropdown Always Appears
**Objective:** Verify dropdown appears every time, not just first time.

**Steps:**
1. Complete an application
2. Say: "Actually, I want to open a different account type"
3. Verify form displays again

**Expected Result:**
- ✅ Dropdown appears again
- ✅ All 5 account types still available
- ✅ Previous form data not pre-filled (fresh form)

## Validation Rules Summary

### Required for All Accounts:
- First Name, Last Name
- SSN (format: XXX-XX-XXXX)
- Date of Birth (must be 18+)
- Email (valid format)
- Phone (format: (XXX) XXX-XXXX)
- Complete address (street, city, state, ZIP)

### Account-Specific Requirements:

**Regular Checking:**
- Minimum deposit: $25

**Premium Checking:**
- Minimum deposit: $25

**Savings:**
- Minimum deposit: $100

**Regular Credit Card:**
- Employer name (required)
- Annual income (required, warning if < $15,000)

**Travel Credit Card:**
- Employer name (required)
- Annual income (required, warning if < $15,000)
- Frequent flyer number (optional, format: FA123456789)

## Security & Compliance Features

### PII Handling:
- ✅ SSN masked in all responses (XXX-XX-1234)
- ✅ No PII stored in database
- ✅ All data validated before processing

### KYC Compliance:
- ✅ All accounts require in-branch verification
- ✅ Required documents listed:
  - Government-issued photo ID
  - Social Security card/document
  - Proof of address
- ✅ Initial deposit required for in-branch visit

## Troubleshooting

### Issue: Dropdown doesn't appear
**Possible Causes:**
1. Agent not calling `show_account_opening_form` immediately
2. Form tool not imported correctly
3. Browser/UI not rendering FormWidget

**Solutions:**
1. Check agent instructions include: "IMMEDIATELY call 'show_account_opening_form'"
2. Verify tool import: `orchestrate tools list | grep show_account_opening_form`
3. Check browser console for errors

### Issue: Validation errors not showing
**Possible Causes:**
1. `process_account_application` tool not imported
2. Form data not being passed correctly

**Solutions:**
1. Verify tool import: `orchestrate tools list | grep process_account_application`
2. Check tool logs for parameter passing issues

### Issue: Agent asks questions instead of showing form
**Possible Causes:**
1. Agent instructions not clear enough
2. Agent trying to gather info before calling tool

**Solutions:**
1. Update agent instructions to emphasize immediate tool call
2. Remove any pre-qualification questions from agent instructions

## Success Metrics

After testing, verify:
- ✅ Dropdown appears 100% of the time when user wants to open account
- ✅ All 5 account types selectable from dropdown
- ✅ All validation rules working correctly
- ✅ SSN masking working in all responses
- ✅ Reference numbers generated uniquely
- ✅ Branch locator integration working
- ✅ KYC requirements clearly communicated

## Next Steps After Testing

1. **If all tests pass:**
   - Deploy to production environment
   - Update user documentation
   - Train customer service staff

2. **If issues found:**
   - Document specific failures
   - Review tool code and agent instructions
   - Re-test after fixes

## Additional Resources

- [Account Opening README](./ACCOUNT_OPENING_README.md) - Complete technical documentation
- [Implementation Summary](./ACCOUNT_OPENING_IMPLEMENTATION_SUMMARY.md) - Development notes
- [Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/) - Official docs

---

**Last Updated:** 2026-05-08  
**Version:** 1.0  
**Author:** Bob (AI Assistant)