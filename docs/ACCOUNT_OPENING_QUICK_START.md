# Account Opening Feature - Quick Start Guide

## What Was Built

A complete account opening system for Lendyr Bank that demonstrates PII handling using Orchestrate plugins with a **dropdown menu** for account type selection.

## Key Features

✅ **Dropdown Menu** - Account types displayed as dropdown (not table or text)  
✅ **5 Account Types** - Regular Checking, Premium Checking, Savings, Regular Credit Card, Travel Credit Card  
✅ **PII Handling** - SSN masking, validation, no database storage  
✅ **KYC Compliance** - In-branch verification required for all accounts  
✅ **Form Validation** - Age, email, phone, SSN, income checks  
✅ **Branch Integration** - Routes to branch locator after application  

## Files Created

### Tools (Python)
1. **`tools/account_opening_form/account_opening_form.py`** (175 lines)
   - Form tool that displays dropdown immediately
   - Uses `FormWidget` with `ComboBox` for account type selection
   - Collects all required PII fields

2. **`tools/process_account_application/process_account_application.py`** (213 lines)
   - Validates all form data
   - Masks SSN (XXX-XX-1234 format)
   - Generates application reference numbers
   - Returns next steps for KYC verification

### Agent
3. **`agents/account_opening_agent.yaml`** (75 lines)
   - Configured to call form tool immediately
   - Integrates with branch locator
   - Handles all 5 account types

### Documentation
4. **`docs/ACCOUNT_OPENING_README.md`** (348 lines)
   - Complete technical documentation
   - API reference for both tools
   - Deployment instructions

5. **`docs/ACCOUNT_OPENING_TESTING_GUIDE.md`** (400 lines)
   - 15 comprehensive test cases
   - Validation rules summary
   - Troubleshooting guide

6. **`docs/ACCOUNT_OPENING_IMPLEMENTATION_SUMMARY.md`** (Previous session notes)

## How It Works

### User Flow
```
User: "I want to open a new account"
  ↓
Agent: Immediately calls show_account_opening_form
  ↓
User: Sees dropdown with 5 account types + form fields
  ↓
User: Selects account type, fills form, submits
  ↓
Agent: Calls process_account_application
  ↓
Agent: Returns validation results + reference number + next steps
  ↓
Agent: Offers to find nearest branch
```

### Technical Implementation

**Why Form Tools?**
- Form Tools return `FormWidget` that displays **immediately**
- `ComboBox` widget creates the dropdown menu
- Alternative (Literal type) only shows dropdown during parameter collection

**Key Code Pattern:**
```python
@tool(name="show_account_opening_form", ...)
def show_account_opening_form() -> ToolResult:
    form = FormWidget(
        inputs=[
            ComboBox(
                name="account_type",
                options=["regular_checking", "premium_checking", ...],
                option_labels=["Regular Checking", "Premium Checking", ...]
            ),
            # ... other inputs
        ]
    )
    return ToolResult(content=[...], widget=form)
```

## Deploy & Test

### 1. Deploy (2 minutes)
```bash
cd /Users/kk76/Public/lendyr
./scripts/import_all_assets.sh
```

This imports:
- ✅ show_account_opening_form tool
- ✅ process_account_application tool  
- ✅ account_opening_agent

### 2. Verify Import
```bash
orchestrate tools list | grep -E "show_account_opening_form|process_account_application"
orchestrate agents list | grep account_opening_agent
```

### 3. Quick Test
1. Start conversation with `account_opening_agent`
2. Say: **"I want to open a new account"**
3. **Expected:** Form displays with dropdown menu
4. Select "Regular Checking" from dropdown
5. Fill form with test data:
   - Name: John Doe
   - SSN: 123-45-6789
   - DOB: 1990-01-15
   - Email: john.doe@example.com
   - Phone: (555) 123-4567
   - Address: 123 Main St, San Francisco, CA 94102
   - Initial Deposit: $25
6. Submit form
7. **Expected:** 
   - ✅ Validation success
   - ✅ SSN masked as XXX-XX-6789
   - ✅ Reference number generated
   - ✅ Next steps for in-branch verification
   - ✅ Offer to find nearest branch

## Account Types & Requirements

| Account Type | Min Deposit | Additional Requirements |
|--------------|-------------|------------------------|
| Regular Checking | $25 | None |
| Premium Checking | $25 | None |
| Savings | $100 | None |
| Regular Credit Card | N/A | Employer, Annual Income |
| Travel Credit Card | N/A | Employer, Annual Income, Optional: Frequent Flyer # |

## PII Security Features

- **SSN Masking:** Always displayed as XXX-XX-1234
- **No Database Storage:** Application data not persisted
- **Format Validation:** SSN, email, phone validated before processing
- **Age Verification:** Must be 18+ to open account
- **KYC Required:** All accounts require in-branch verification with ID

## Testing Checklist

Use the comprehensive testing guide for full validation:
- [ ] Test 1: Dropdown appears immediately ⭐ **CRITICAL**
- [ ] Test 2-6: All 5 account types work correctly
- [ ] Test 7-12: All validation rules working
- [ ] Test 13: Branch locator integration
- [ ] Test 14-15: Multiple applications, dropdown always appears

See [`docs/ACCOUNT_OPENING_TESTING_GUIDE.md`](./ACCOUNT_OPENING_TESTING_GUIDE.md) for detailed test cases.

## Troubleshooting

### Dropdown doesn't appear?
1. Check agent calls `show_account_opening_form` immediately
2. Verify tool imported: `orchestrate tools list | grep show_account_opening_form`
3. Check browser console for FormWidget rendering errors

### Validation not working?
1. Verify `process_account_application` tool imported
2. Check tool logs for parameter passing issues

### Agent asks questions instead of showing form?
1. Agent instructions must say "IMMEDIATELY call show_account_opening_form"
2. Remove pre-qualification questions from agent

## Next Steps

1. **Run Full Test Suite** - Complete all 15 tests in testing guide
2. **Production Deployment** - Deploy to production environment
3. **Staff Training** - Train customer service on new workflow
4. **Monitor Usage** - Track application submissions and success rates

## Documentation Links

- **[Complete Technical Docs](./ACCOUNT_OPENING_README.md)** - Full API reference, architecture
- **[Testing Guide](./ACCOUNT_OPENING_TESTING_GUIDE.md)** - 15 test cases with expected results
- **[Implementation Summary](./ACCOUNT_OPENING_IMPLEMENTATION_SUMMARY.md)** - Development notes

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review full documentation in `docs/ACCOUNT_OPENING_README.md`
3. Check Orchestrate documentation: https://developer.watson-orchestrate.ibm.com/

---

**Version:** 1.0  
**Last Updated:** 2026-05-08  
**Status:** ✅ Ready for Testing