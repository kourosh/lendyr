"""
Lendyr Bank - Account Information Collection Form Tool

This tool presents an interactive form for collecting customer information for new account applications.
Uses FormWidget with ComboBox dropdown for account type selection.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.widgets.forms.types import (
    FormWidget, TextInput, ComboBox, NumberInput
)
from ibm_watsonx_orchestrate.run.tool_result import ToolResult


@tool(
    name="show_account_opening_form",
    description="Display an interactive form for collecting new account application information with dropdown menu for account type selection"
)
def show_account_opening_form():
    """
    Display an interactive form for new account applications.
    
    Returns:
        ToolResult with FormWidget containing all necessary fields including
        a dropdown (ComboBox) for account type selection.
    """
    
    form = FormWidget(
        title="New Account Application",
        description="Please complete this form to begin your account opening process. All information will be validated before scheduling your in-branch appointment.",
        inputs=[
            ComboBox(
                name="account_type",
                title="Account Type",
                description="Select the type of account you wish to open",
                required=True,
                options=[
                    "regular_checking",
                    "premium_checking",
                    "savings",
                    "regular_credit_card",
                    "travel_credit_card"
                ],
                option_labels=[
                    "Regular Checking Account",
                    "Premium Checking Account",
                    "Savings Account",
                    "Regular Credit Card",
                    "Travel Credit Card (Fiction Airlines Partnership)"
                ]
            ),
            TextInput(
                name="full_name",
                title="Full Legal Name",
                description="Enter your full name as it appears on your government ID",
                required=True,
                placeholder="John Doe"
            ),
            TextInput(
                name="ssn",
                title="Social Security Number",
                description="9 digits (format: XXX-XX-XXXX)",
                required=True,
                placeholder="123-45-6789"
            ),
            TextInput(
                name="date_of_birth",
                title="Date of Birth",
                description="Format: MM/DD/YYYY (Must be 18+ years old)",
                required=True,
                placeholder="01/15/1990"
            ),
            TextInput(
                name="street_address",
                title="Street Address",
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
                description="2-letter state code",
                required=True,
                placeholder="CA"
            ),
            TextInput(
                name="zip_code",
                title="ZIP Code",
                description="5 digits or 5+4 format",
                required=True,
                placeholder="94102"
            ),
            TextInput(
                name="phone",
                title="Phone Number",
                description="10 digits",
                required=True,
                placeholder="415-555-0123"
            ),
            TextInput(
                name="email",
                title="Email Address",
                required=True,
                placeholder="john.doe@example.com"
            ),
            NumberInput(
                name="initial_deposit",
                title="Initial Deposit Amount",
                description="Minimum $25.00",
                required=True,
                default_value=100.0,
                minimum=25.0
            )
        ]
    )
    
    return ToolResult(
        content=["Please complete the account application form below. After submission, we'll validate your information and help you schedule an appointment at your nearest Lendyr Bank branch."],
        widget=form
    )

# Made with Bob
