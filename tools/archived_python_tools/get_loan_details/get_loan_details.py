import requests
from datetime import date, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

BASE_URL = "https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"

@tool(permission=ToolPermission.READ_ONLY)
def get_loan_details(customer_id: str) -> dict:
    """
    Retrieves loan and payment data needed for deferral eligibility evaluation.
    Returns credit score, outstanding balance, annual rate, monthly payment,
    next payment due date, count of late payments in the past 3 years,
    and whether the customer has a prior deferral on record.

    Args:
        customer_id (str): The unique customer identifier.

    Returns:
        dict: Combined loan and eligibility data.
    """
    customer_resp = requests.get(f"{BASE_URL}/customers/by-id/{customer_id}")
    if customer_resp.status_code != 200:
        return None
    customer = customer_resp.json()
    credit_score = customer.get("credit_score")

    loans_resp = requests.get(f"{BASE_URL}/customers/by-id/{customer_id}/loans")
    if loans_resp.status_code != 200:
        return None
    loans = loans_resp.json()
    if not loans:
        return None
    loan = loans[0]

    # Count late payments in the past 3 years
    three_years_ago = (date.today() - timedelta(days=3 * 365)).isoformat()
    history_resp = requests.get(f"{BASE_URL}/customers/by-id/{customer_id}/payment-history")
    late_payments_3yr = 0
    if history_resp.status_code == 200:
        payments = history_resp.json().get("payment_history", [])
        late_payments_3yr = sum(
            1 for p in payments
            if p.get("was_late") == 1 and str(p.get("payment_date", "")) >= three_years_ago
        )

    return {
        "loan_id": loan.get("loan_id"),
        "credit_score": credit_score,
        "outstanding_balance": float(loan.get("outstanding_balance", 0)),
        "annual_rate": float(loan.get("interest_rate", 0)),
        "monthly_payment": float(loan.get("monthly_payment", 0)),
        "due_date": loan.get("next_payment_date"),
        "late_payments_3yr": late_payments_3yr,
        "prior_deferral": False,
    }
