# Account Opening Form Tool Implementation

## Overview

This document describes the implementation of the account opening use case for Lendyr Bank using **Form Tools** with dropdown menus in watsonx Orchestrate. The solution demonstrates how to handle Personally Identifiable Information (PII) securely using Orchestrate's form widget capabilities.

## Problem Statement

The original implementation used Python's `Literal` type for dropdown menus, but this approach only displays the dropdown **when the tool is invoked** (during parameter collection). The requirement was to display the dropdown **immediately** when a customer expresses interest in opening an account.

## Solution: Form Tools

The solution uses **Form Tools** - a specialized type of Python tool that returns a `FormWidget` containing interactive UI components including dropdown menus (ComboBox), text inputs, date pickers, and number inputs.

### Key Difference: Literal vs Form Tool

| Approach | When Dropdown Appears | Use Case |
|----------|----------------------|----------|
| **Literal Type** | During tool parameter collection | When agent decides which parameters to collect |
| **Form Tool** | Immediately when tool is called | When you want to present a form upfront |

## Implementation Components

### 1. Form Tool: `show_account_opening_form`

**Location:** `tools/account_opening_form/account_opening_form.py`

**Purpose:** Displays an interactive form with dropdown for account type selection and all required fields.

**Key Features:**
- **ComboBox** for account type dropdown with 5 options:
  - Regular Checking
  - Premium Checking
  - Savings
  - Regular Credit Card
  - Travel Credit Card (Fiction Airlines Partnership)
- **TextInput** fields for personal information (name, SSN, email, phone, address)
- **DatePicker** for date of birth
- **NumberInput** for initial deposit and annual income
- Returns a `ToolResult` with `FormWidget` that renders in the UI

**API Structure:**
```python
ComboBox(
    name="account_type",
    title="Account Type",
    description="Select the type of account you want to open",
    required=True,
    options=["regular_checking", "premium_checking", "savings", ...],
    option_labels=["Regular Checking", "Premium Checking", "Savings", ...]
)
```

### 2. Processing Tool: `process_account_application`

**Location:** `tools/process_account_application/process_account_application.py`

**Purpose:** Validates submitted form data and prepares application for in-branch verification.

**Validation Rules:**
- **SSN:** Must be in format XXX-XX-XXXX
- **Age:** Must be 18 or older
- **Email:** Valid email format
- **Phone:** Format (XXX) XXX-XXXX
- **State:** 2-letter code
- **ZIP:** 5 digits
- **Account-specific:**
  - Regular/Premium Checking: Minimum $25 initial deposit
  - Savings: Minimum $100 initial deposit
  - Credit Cards: Employer and annual income required

**PII Handling:**
- SSN is masked in responses (XXX-XX-1234)
- All PII is validated but NOT stored in database
- Application prepared for in-branch verification only

**Output:**
- Application reference number (e.g., APP-20260508-1234)
- Validation status (success/failure)
- Next steps for in-branch verification
- Required documents list

### 3. Agent: `account_opening_agent`

**Location:** `agents/account_opening_agent.yaml`

**Critical Workflow:**
1. **Immediately** call `show_account_opening_form` when customer wants to open account
2. Wait for form submission
3. Call `process_account_application` with form data
4. Present validation results and next steps
5. Offer to help find nearest branch

**Key Instructions:**
- DO NOT ask questions before showing form
- DO NOT collect information manually
- DO NOT create accounts directly (KYC compliance requires in-branch verification)
- DO explain why in-branch verification is required

## Account Types and Requirements

### Regular Checking
- No monthly fees
- Minimum $25 initial deposit
- Standard checking features

### Premium Checking
- Enhanced checking with rewards
- Requires $1000 minimum balance
- Minimum $25 initial deposit

### Savings
- High-yield savings account
- Minimum $100 initial deposit

### Regular Credit Card
- Standard credit card with competitive rates
- Requires: employer name, annual income
- Credit check performed at branch

### Travel Credit Card (Fiction Airlines Partnership)
- Earn miles on purchases
- Requires: employer name, annual income
- Optional: Fiction Airlines frequent flyer number (format: FA123456789)
- Benefits:
  - 2x miles on Fiction Airlines purchases
  - 1.5x miles on all other purchases
  - Priority boarding
  - Free checked bag

## KYC Compliance

All accounts require **in-branch verification** for Know Your Customer (KYC) compliance.

**Required Documents:**
1. Government-issued photo ID (driver's license or passport)
2. Social Security card or official document with SSN
3. Proof of address (utility bill, lease agreement, or bank statement)
4. Initial deposit (for checking/savings accounts)

**Why In-Branch?**
- Identity verification
- Document authentication
- Regulatory compliance
- Fraud prevention
- Customer protection

## Deployment Instructions

### 1. Import Tools

```bash
# Import form tool
orchestrate tools import python \
  --file tools/account_opening_form/account_opening_form.py \
  --requirements tools/account_opening_form/requirements.txt

# Import processing tool
orchestrate tools import python \
  --file tools/process_account_application/process_account_application.py \
  --requirements tools/process_account_application/requirements.txt
```

### 2. Import Agent

```bash
orchestrate agents import \
  --file agents/account_opening_agent.yaml
```

### 3. Update Main Agent

Ensure `lendyr_customer_care` agent includes `account_opening_agent` in collaborators and has routing logic for account opening requests.

## Testing Checklist

- [ ] Form displays immediately when customer says "I want to open an account"
- [ ] Dropdown shows all 5 account types
- [ ] All form fields are present and properly labeled
- [ ] Form validation works (required fields, format validation)
- [ ] SSN is masked in responses
- [ ] Application reference number is generated
- [ ] Next steps are clearly explained
- [ ] Branch locator integration works
- [ ] Different account types show appropriate requirements

## Technical Notes

### Form Widget API

The Form Tool uses Orchestrate's form widget system:

```python
from ibm_watsonx_orchestrate.run.widgets.forms.types import (
    FormWidget,
    TextInput,
    ComboBox,
    DatePicker,
    NumberInput
)
from ibm_watsonx_orchestrate.run.tool_result import ToolResult
```

### ComboBox Parameters
- `name`: Field identifier
- `title`: Label displayed in UI
- `description`: Help text
- `required`: Boolean for required field
- `options`: List of internal values
- `option_labels`: List of display labels (must match options length)

### NumberInput Parameters
- `name`: Field identifier
- `title`: Label displayed in UI
- `description`: Help text
- `required`: Boolean for required field
- `minimum`: Minimum allowed value
- `maximum`: Maximum allowed value (optional)
- `default_value`: Default value

### ToolResult Structure
```python
ToolResult(
    content=[
        TextContent(text="...", annotations=Annotations(audience=[Role.USER])),
        TextContent(text="...", annotations=Annotations(audience=[Role.ASSISTANT]))
    ],
    widget=form
)
```

## Comparison with Previous Approach

### Previous: Literal Type Approach
```python
@tool
def collect_account_info(
    account_type: Literal["Regular Checking", "Premium Checking", ...],
    ...
):
    # Dropdown appears during parameter collection
```

**Issue:** Agent must decide to call the tool first, then dropdown appears during parameter collection. Agent was showing a table instead.

### Current: Form Tool Approach
```python
@tool
def show_account_opening_form() -> ToolResult:
    form = FormWidget(
        inputs=[
            ComboBox(name="account_type", options=[...], ...)
        ]
    )
    return ToolResult(widget=form)
```

**Advantage:** Form with dropdown displays immediately when tool is called. Agent instructions explicitly call this tool when customer wants to open account.

## Files Created/Modified

### New Files
- `tools/account_opening_form/account_opening_form.py`
- `tools/account_opening_form/requirements.txt`
- `tools/process_account_application/process_account_application.py`
- `tools/process_account_application/requirements.txt`

### Modified Files
- `agents/account_opening_agent.yaml` - Updated to use form tool approach

### Deprecated Files (can be removed after testing)
- `tools/collect_account_info/` - Old Literal type approach
- `tools/collect_account_info_form/` - Intermediate attempt

## Next Steps

1. Deploy the new tools and agent
2. Test the form display and dropdown functionality
3. Verify PII handling and validation
4. Test integration with branch locator
5. Remove deprecated tools after successful testing
6. Update main customer care agent routing if needed

## References

- [Orchestrate Form Tools Documentation](https://developer.watson-orchestrate.ibm.com/tools/create_tool#creating-a-form-tool)
- [Orchestrate Tool Response Structure](https://developer.watson-orchestrate.ibm.com/tools/tool_response_structure)
- [Python Tools Documentation](https://developer.watson-orchestrate.ibm.com/tools/create_tool)