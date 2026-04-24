from datetime import date, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


@tool(permission=ToolPermission.READ_ONLY)
def calculate_deferral_terms(
    outstanding_balance: float,
    annual_rate: float,
    due_date: str,
) -> dict:
    """
    Calculates the exact financial impact of a 30-day loan payment deferral.
    Returns the new payment date, accrued interest, and new outstanding balance.

    Args:
        outstanding_balance (float): Current outstanding loan balance in dollars.
        annual_rate (float): Annual interest rate as a percentage (e.g. 12.5 for 12.5%).
        due_date (str): Current next payment due date in YYYY-MM-DD format.

    Returns:
        dict: new_payment_date (str), accrued_interest (float), new_balance (float).
    """
    new_payment_date = (date.fromisoformat(due_date) + timedelta(days=30)).isoformat()
    accrued_interest = round(outstanding_balance * (annual_rate / 100) * (30 / 365), 2)
    new_balance = round(outstanding_balance + accrued_interest, 2)

    return {
        "new_payment_date": new_payment_date,
        "accrued_interest": accrued_interest,
        "new_balance": new_balance,
    }
