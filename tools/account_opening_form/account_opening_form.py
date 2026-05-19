"""
Account Opening Form Tool
Displays an interactive form for collecting account opening information with dropdown for account type selection.
"""

from typing import Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.tool_result import ToolResult, TextContent, Annotations, Role
from ibm_watsonx_orchestrate.run.widgets.forms.types import (
    FormWidget,
    TextInput,
    ComboBox,
    DatePicker,
    NumberInput
)


@tool(
    name="show_account_opening_form",
    display_name="Show Account Opening Form",
    description="Displays an interactive form for collecting customer information to open a new account. Shows a dropdown menu for account type selection and collects all required information based on the selected account type."
)
def show_account_opening_form() -> ToolResult:
    """
    Displays an interactive form with dropdown for account type selection.
    
    This form tool presents the user with:
    - A dropdown menu to select account type (Regular Checking, Premium Checking, Savings, Regular Credit Card, Travel Credit Card)
    - Input fields for personal information (name, SSN, DOB, address, phone, email)
    - Additional fields based on account type selection
    
    Returns:
        ToolResult: A form widget with all necessary input fields for account opening
    """
    
    # Create the form widget with all necessary inputs
    form = FormWidget(
        title="New Account Application",
        description="Please complete all required fields to open your new account",
        inputs=[
            # Account Type Selection (Dropdown)
            ComboBox(
                name="account_type",
                title="Account Type",
                description="Select the type of account you want to open",
                required=True,
                options=["regular_checking", "premium_checking", "savings", "regular_credit_card", "travel_credit_card"],
                option_labels=["Regular Checking", "Premium Checking", "Savings", "Regular Credit Card", "Travel Credit Card (Fiction Airlines Partnership)"]
            ),
            
            # Personal Information
            TextInput(
                name="first_name",
                title="First Name",
                description="Your legal first name",
                required=True,
                placeholder="John"
            ),
            
            TextInput(
                name="last_name",
                title="Last Name",
                description="Your legal last name",
                required=True,
                placeholder="Doe"
            ),
            
            TextInput(
                name="ssn",
                title="Social Security Number",
                description="Format: XXX-XX-XXXX (will be securely encrypted)",
                required=True,
                placeholder="123-45-6789"
            ),
            
            DatePicker(
                name="date_of_birth",
                title="Date of Birth",
                description="You must be 18 or older to open an account",
                required=True
            ),
            
            # Contact Information
            TextInput(
                name="email",
                title="Email Address",
                description="Your primary email for account notifications",
                required=True,
                placeholder="john.doe@example.com"
            ),
            
            TextInput(
                name="phone",
                title="Phone Number",
                description="Format: (XXX) XXX-XXXX",
                required=True,
                placeholder="(555) 123-4567"
            ),
            
            # Address Information
            TextInput(
                name="street_address",
                title="Street Address",
                description="Your residential street address",
                required=True,
                placeholder="123 Main Street"
            ),
            
            TextInput(
                name="city",
                title="City",
                required=True,
                placeholder="San Francisco"
            ),
            
            TextInput(
                name="state",
                title="State",
                description="Two-letter state code",
                required=True,
                placeholder="CA"
            ),
            
            TextInput(
                name="zip_code",
                title="ZIP Code",
                required=True,
                placeholder="94102"
            ),
            
            # Initial Deposit (for checking/savings accounts)
            NumberInput(
                name="initial_deposit",
                title="Initial Deposit Amount",
                description="Minimum $25 for checking, $100 for savings (optional for credit cards)",
                required=False,
                minimum=0,
                default_value=0
            ),
            
            # Employment Information (for credit cards)
            TextInput(
                name="employer",
                title="Employer Name",
                description="Required for credit card applications",
                required=False,
                placeholder="Acme Corporation"
            ),
            
            NumberInput(
                name="annual_income",
                title="Annual Income",
                description="Required for credit card applications",
                required=False,
                minimum=0,
                default_value=0
            ),
            
            # Fiction Airlines Frequent Flyer Number (for travel credit card)
            TextInput(
                name="frequent_flyer_number",
                title="Fiction Airlines Frequent Flyer Number",
                description="Optional - link your existing Fiction Airlines account",
                required=False,
                placeholder="FA123456789"
            )
        ]
    )
    
    # Return the form with user-facing instructions
    return ToolResult(
        content=[
            TextContent(
                text="Please complete the account application form below. All fields marked as required must be filled out.",
                annotations=Annotations(audience=[Role.USER])
            ),
            TextContent(
                text="Form displayed to user for account opening. Waiting for user to complete and submit the form.",
                annotations=Annotations(audience=[Role.ASSISTANT])
            )
        ],
        widget=form
    )

# Made with Bob
