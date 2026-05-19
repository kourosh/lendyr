"""
Account Opening Tool
Collects information to open a new account with dropdown for account type selection.
"""

from typing import Literal, Dict, Any
from datetime import datetime
import re
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    name="open_account",
    display_name="Open New Account",
    description="Opens a new bank account. Collects customer information and validates eligibility. Shows a dropdown menu for account type selection."
)
def open_account(
    account_type: Literal["regular_checking", "premium_checking", "savings", "regular_credit_card", "travel_credit_card"],
    first_name: str,
    last_name: str,
    ssn: str,
    date_of_birth: str,
    email: str,
    phone: str,
    street_address: str,
    city: str,
    state: str,
    zip_code: str,
    initial_deposit: float = 0.0,
    employer: str = "",
    annual_income: float = 0.0,
    frequent_flyer_number: str = ""
) -> Dict[str, Any]:
    """
    Opens a new bank account with the provided information.
    
    Args:
        account_type: Type of account - regular_checking (Regular Checking), premium_checking (Premium Checking), savings (Savings), regular_credit_card (Regular Credit Card), travel_credit_card (Travel Credit Card with Fiction Airlines Partnership)
        first_name: Customer's legal first name
        last_name: Customer's legal last name
        ssn: Social Security Number in format XXX-XX-XXXX
        date_of_birth: Date of birth in format YYYY-MM-DD (must be 18 or older)
        email: Email address for account notifications
        phone: Phone number in format (XXX) XXX-XXXX
        street_address: Residential street address
        city: City
        state: Two-letter state code (e.g., CA, NY)
        zip_code: 5-digit ZIP code
        initial_deposit: Initial deposit amount (minimum $25 for checking, $100 for savings, optional for credit cards)
        employer: Employer name (required for credit card applications)
        annual_income: Annual income in dollars (required for credit card applications)
        frequent_flyer_number: Fiction Airlines frequent flyer number in format FA123456789 (optional, for travel credit card only)
    
    Returns:
        Dictionary containing validation results, application reference number, and next steps
    """
    
    # Account type mapping
    account_type_names = {
        "regular_checking": "Regular Checking",
        "premium_checking": "Premium Checking",
        "savings": "Savings",
        "regular_credit_card": "Regular Credit Card",
        "travel_credit_card": "Travel Credit Card (Fiction Airlines Partnership)"
    }
    
    account_name = account_type_names.get(account_type, account_type)
    
    # Validation results
    validation_errors = []
    warnings = []
    
    # Validate SSN format
    ssn_pattern = r'^\d{3}-\d{2}-\d{4}$'
    if not re.match(ssn_pattern, ssn):
        validation_errors.append("SSN must be in format XXX-XX-XXXX")
    
    # Validate age (must be 18+)
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = (datetime.now() - dob).days // 365
        if age < 18:
            validation_errors.append("You must be at least 18 years old to open an account")
    except ValueError:
        validation_errors.append("Invalid date of birth format. Use YYYY-MM-DD")
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        validation_errors.append("Invalid email address format")
    
    # Validate phone format
    phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    if not re.match(phone_pattern, phone):
        validation_errors.append("Phone must be in format (XXX) XXX-XXXX")
    
    # Validate state code
    if len(state) != 2 or not state.isalpha():
        validation_errors.append("State must be a 2-letter code (e.g., CA, NY)")
    
    # Validate ZIP code
    if not re.match(r'^\d{5}$', zip_code):
        validation_errors.append("ZIP code must be 5 digits")
    
    # Account-specific validations
    if account_type in ["regular_checking", "premium_checking"]:
        if initial_deposit < 25:
            validation_errors.append(f"{account_name} requires a minimum initial deposit of $25")
    
    if account_type == "savings":
        if initial_deposit < 100:
            validation_errors.append("Savings account requires a minimum initial deposit of $100")
    
    if account_type in ["regular_credit_card", "travel_credit_card"]:
        if not employer:
            validation_errors.append("Employer name is required for credit card applications")
        if annual_income <= 0:
            validation_errors.append("Annual income is required for credit card applications")
        if annual_income < 15000:
            warnings.append("Annual income below $15,000 may affect credit card approval")
    
    if account_type == "travel_credit_card" and frequent_flyer_number:
        # Validate Fiction Airlines frequent flyer format (FA followed by 9 digits)
        if not re.match(r'^FA\d{9}$', frequent_flyer_number):
            warnings.append("Fiction Airlines frequent flyer number should be in format FA123456789")
    
    # If there are validation errors, return them
    if validation_errors:
        return {
            "status": "validation_failed",
            "account_type": account_name,
            "errors": validation_errors,
            "warnings": warnings,
            "message": "Please correct the following errors and try again."
        }
    
    # Mask SSN for display (show only last 4 digits)
    masked_ssn = f"XXX-XX-{ssn[-4:]}"
    
    # Generate application reference number
    reference_number = f"APP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    # Prepare success response
    response = {
        "status": "pending_verification",
        "reference_number": reference_number,
        "account_type": account_name,
        "applicant_name": f"{first_name} {last_name}",
        "masked_ssn": masked_ssn,
        "email": email,
        "phone": phone,
        "address": f"{street_address}, {city}, {state} {zip_code}",
        "warnings": warnings,
        "message": f"Application submitted successfully! Reference number: {reference_number}",
        "next_steps": [
            "Your application has been received and validated",
            "For security and compliance, account opening requires in-branch verification",
            "Please visit a Lendyr Bank branch with:",
            "  - Valid government-issued photo ID (driver's license or passport)",
            "  - Social Security card or official document with your SSN",
            "  - Proof of address (utility bill, lease agreement, or bank statement)",
            f"  - Initial deposit of ${initial_deposit:.2f}" if initial_deposit > 0 else "",
            "Branch staff will complete your application and activate your account",
            "Would you like help finding the nearest Lendyr Bank branch?"
        ],
        "kyc_required": True,
        "documents_needed": [
            "Government-issued photo ID",
            "Social Security card or document",
            "Proof of address"
        ]
    }
    
    # Add account-specific information
    if account_type in ["regular_checking", "premium_checking", "savings"]:
        response["initial_deposit"] = f"${initial_deposit:.2f}"
    
    if account_type in ["regular_credit_card", "travel_credit_card"]:
        response["employer"] = employer
        response["annual_income"] = f"${annual_income:,.2f}"
        response["credit_check_required"] = True
    
    if account_type == "travel_credit_card" and frequent_flyer_number:
        response["frequent_flyer_linked"] = frequent_flyer_number
        response["travel_benefits"] = [
            "2x miles on Fiction Airlines purchases",
            "1.5x miles on all other purchases",
            "Priority boarding on Fiction Airlines flights",
            "Free checked bag on Fiction Airlines"
        ]
    
    return response

# Made with Bob