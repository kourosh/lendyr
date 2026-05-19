"""
Lendyr Bank - Account Type Selector Tool

Returns a special marker tag that the web chat intercepts to render
a native <select> dropdown instead of a plain text response.
The web chat's pre:receive handler strips the tag and sets
response_type='user_defined'; userDefinedResponse renders the dropdown.
"""

import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.tool_result import ToolResult
from ibm_watsonx_orchestrate.run import TextContent, Annotations, Role


ACCOUNT_OPTIONS = [
    {
        "value": "Regular Checking",
        "label": "Regular Checking Account",
        "description": "No monthly fees · $25 minimum deposit",
    },
    {
        "value": "Premium Checking",
        "label": "Premium Checking Account",
        "description": "Rewards & benefits · $50,000+ annual income required",
    },
    {
        "value": "Savings",
        "label": "Savings Account",
        "description": "High-yield savings · $25 minimum deposit",
    },
    {
        "value": "Regular Credit Card",
        "label": "Regular Credit Card",
        "description": "Competitive rates · $25,000+ annual income required",
    },
    {
        "value": "Travel Credit Card",
        "label": "Travel Credit Card",
        "description": "Fiction Airlines rewards · $25,000+ annual income required",
    },
]


@tool(
    name="present_account_type_selector",
    description="Display a dropdown menu so the customer can choose which type of account to open. Call this at the start of the account opening conversation.",
)
def present_account_type_selector() -> ToolResult:
    """
    Present the customer with a dropdown of available Lendyr account types.

    Returns a ToolResult whose text contains an <account-type-selector> JSON tag.
    The embedded web chat's pre:receive handler intercepts this tag, converts the
    message to user_defined type, and renders a native dropdown.
    """
    payload = json.dumps({"options": ACCOUNT_OPTIONS})
    marker = f"<account-type-selector>{payload}</account-type-selector>"

    return ToolResult(
        content=[
            TextContent(
                text=marker,
                annotations=Annotations(audience=[Role.USER]),
            )
        ]
    )
