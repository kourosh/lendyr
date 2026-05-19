"""
Lendyr Bank - Account Information Collection Tool

This tool collects and validates customer information for new account applications.
It does NOT create accounts in the database - it only validates and confirms the information
that will be used during the in-branch KYC verification process.

Supports five account types:
1. Regular Checking
2. Premium Checking
3. Savings
4. Regular Credit Card
5. Travel Credit Card
"""

from datetime import datetime
import re
from typing import Dict, Any, Optional, Literal
from ibm_watsonx_orchestrate.agent_builder.tools import tool


def validate_ssn(ssn: str) -> bool:
    """Validate SSN format (XXX-XX-XXXX or 9 digits)"""
    # Remove any spaces or dashes
    clean_ssn = ssn.replace("-", "").replace(" ", "")
    return len(clean_ssn) == 9 and clean_ssn.isdigit()


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)"""
    clean_phone = re.sub(r'[^0-9]', '', phone)
    return len(clean_phone) == 10


def validate_age(dob: str) -> tuple[bool, Optional[int]]:
    """Validate date of birth and check if 18+ years old"""
    try:
        birth_date = datetime.strptime(dob, "%m/%d/%Y")
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age >= 18, age
    except ValueError:
        return False, None


def mask_ssn(ssn: str) -> str:
    """Mask SSN for display (XXX-XX-1234)"""
    clean_ssn = ssn.replace("-", "").replace(" ", "")
    if len(clean_ssn) == 9:
        return f"XXX-XX-{clean_ssn[-4:]}"
    return "XXX-XX-XXXX"


@tool
def collect_account_info(
    account_type: Literal["Regular Checking", "Premium Checking", "Savings", "Regular Credit Card", "Travel Credit Card"],
    full_name: str,
    ssn: str,
    date_of_birth: str,
    street_address: str,
    city: str,
    state: str,
    zip_code: str,
    phone: str,
    email: str,
    initial_deposit: float,
    # Premium Checking fields
    employment_status: Optional[str] = None,
    annual_income: Optional[float] = None,
    employer_name: Optional[str] = None,
    # Savings fields
    savings_goal: Optional[str] = None,
    linked_checking_account: Optional[str] = None,
    monthly_deposit_amount: Optional[float] = None,
    # Credit Card fields
    monthly_housing_payment: Optional[float] = None,
    housing_status: Optional[str] = None,
    # Travel Credit Card fields
    travel_frequency: Optional[int] = None,
    fiction_airlines_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Collect and validate account opening information.
    
    Args:
        account_type: Type of account - select from dropdown menu
        full_name: Customer's full legal name
        ssn: Social Security Number (9 digits)
        date_of_birth: Date of birth in MM/DD/YYYY format
        street_address: Street address
        city: City
        state: State (2-letter code)
        zip_code: ZIP code
        phone: Phone number (10 digits)
        email: Email address
        initial_deposit: Initial deposit amount
        
        Premium Checking additional fields:
        employment_status: Employment status
        annual_income: Annual income (minimum $50,000)
        employer_name: Employer name
        
        Savings additional fields:
        savings_goal: Purpose of savings account
        linked_checking_account: Optional linked checking account number
        monthly_deposit_amount: Optional automatic monthly deposit
        
        Credit Card additional fields:
        employment_status: Employment status
        annual_income: Annual income (minimum $25,000)
        monthly_housing_payment: Monthly housing payment amount
        housing_status: Housing status (own, rent, live with family, other)
        
        Travel Credit Card additional fields:
        travel_frequency: Number of trips per year
        fiction_airlines_number: Optional Fiction Airlines frequent flyer number
    
    Returns:
        Dictionary with validation results and masked information summary
    """
    
    errors = []
    warnings = []
    
    # Normalize account type for internal processing
    account_type_normalized = account_type.lower().replace(" ", "_")
    
    valid_account_types = [
        "regular_checking",
        "premium_checking",
        "savings",
        "regular_credit_card",
        "travel_credit_card"
    ]
    
    if account_type_normalized not in valid_account_types:
        return {
            "success": False,
            "error": f"Invalid account type. Must be one of: {', '.join(valid_account_types)}"
        }
    
    # Validate base required fields
    if not full_name or len(full_name.strip()) < 2:
        errors.append("Full name is required and must be at least 2 characters")
    
    if not validate_ssn(ssn):
        errors.append("SSN must be 9 digits (format: XXX-XX-XXXX or 9 digits)")
    
    is_valid_age, age = validate_age(date_of_birth)
    if not is_valid_age:
        errors.append("Date of birth must be in MM/DD/YYYY format and customer must be 18+ years old")
    elif age and age < 18:
        errors.append(f"Customer must be at least 18 years old (current age: {age})")
    
    if not street_address or len(street_address.strip()) < 5:
        errors.append("Street address is required")
    
    if not city or len(city.strip()) < 2:
        errors.append("City is required")
    
    if not state or len(state) != 2:
        errors.append("State must be 2-letter code (e.g., CA, NY)")
    
    if not zip_code or not re.match(r'^\d{5}(-\d{4})?$', zip_code):
        errors.append("ZIP code must be 5 digits or 5+4 format")
    
    if not validate_phone(phone):
        errors.append("Phone number must be 10 digits")
    
    if not validate_email(email):
        errors.append("Email address must be valid format")
    
    # Validate initial deposit
    min_deposit = 25.0
    if initial_deposit < min_deposit:
        errors.append(f"Initial deposit must be at least ${min_deposit:.2f}")
    
    # Account-specific validations
    if account_type_normalized == "premium_checking":
        if not employment_status:
            errors.append("Employment status is required for Premium Checking")
        if not annual_income or annual_income < 50000:
            errors.append("Annual income of at least $50,000 is required for Premium Checking")
        if employment_status in ["employed", "self-employed"] and not employer_name:
            errors.append("Employer name is required when employed or self-employed")
    
    elif account_type_normalized == "savings":
        if not savings_goal:
            errors.append("Savings goal is required for Savings Account")
        if linked_checking_account and not re.match(r'^\d{10,12}$', linked_checking_account):
            warnings.append("Linked checking account should be 10-12 digits if provided")
    
    elif account_type_normalized in ["regular_credit_card", "travel_credit_card"]:
        if not employment_status:
            errors.append("Employment status is required for credit card applications")
        if not annual_income or annual_income < 25000:
            errors.append("Annual income of at least $25,000 is required for credit card applications")
        if monthly_housing_payment is None or monthly_housing_payment < 0:
            errors.append("Monthly housing payment amount is required")
        if not housing_status or housing_status not in ["own", "rent", "live with family", "other"]:
            errors.append("Housing status must be: own, rent, live with family, or other")
        
        if account_type_normalized == "travel_credit_card":
            if travel_frequency is None or travel_frequency < 0:
                errors.append("Travel frequency (trips per year) is required for Travel Credit Card")
            if fiction_airlines_number and not re.match(r'^[A-Z0-9]{6,12}$', fiction_airlines_number):
                warnings.append("Fiction Airlines number should be 6-12 alphanumeric characters if provided")
    
    # If there are errors, return them
    if errors:
        return {
            "success": False,
            "errors": errors,
            "warnings": warnings
        }
    
    # Build success response with masked PII
    full_address = f"{street_address}, {city}, {state} {zip_code}"
    masked_ssn = mask_ssn(ssn)
    
    response = {
        "success": True,
        "message": "Account application information validated successfully",
        "account_type": account_type_normalized.replace("_", " ").title(),
        "applicant_summary": {
            "name": full_name,
            "ssn": masked_ssn,
            "date_of_birth": date_of_birth,
            "age": age,
            "address": full_address,
            "phone": phone,
            "email": email,
            "initial_deposit": f"${initial_deposit:.2f}"
        }
    }
    
    # Add account-specific details
    if account_type_normalized == "premium_checking":
        response["additional_info"] = {
            "employment_status": employment_status,
            "annual_income": f"${annual_income:,.2f}",
            "employer_name": employer_name or "N/A"
        }
    
    elif account_type_normalized == "savings":
        response["additional_info"] = {
            "savings_goal": savings_goal,
            "linked_checking": linked_checking_account or "None",
            "monthly_deposit": f"${monthly_deposit_amount:.2f}" if monthly_deposit_amount else "None"
        }
    
    elif account_type_normalized in ["regular_credit_card", "travel_credit_card"]:
        response["additional_info"] = {
            "employment_status": employment_status,
            "annual_income": f"${annual_income:,.2f}",
            "monthly_housing_payment": f"${monthly_housing_payment:.2f}",
            "housing_status": housing_status
        }
        
        if account_type_normalized == "travel_credit_card":
            response["additional_info"]["travel_frequency"] = f"{travel_frequency} trips/year"
            response["additional_info"]["fiction_airlines_member"] = fiction_airlines_number or "Not provided"
    
    if warnings:
        response["warnings"] = warnings
    
    response["next_steps"] = "Information validated. Proceed to find nearest branch and schedule appointment."
    
    return response


