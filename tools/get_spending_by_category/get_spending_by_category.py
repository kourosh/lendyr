"""
Get customer spending for a specific category.

This tool fetches transaction data and calculates total spending
for a specified category (e.g., shopping, dining, travel).
"""

from typing import Dict, Any
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


@tool(permission=ToolPermission.READ_ONLY)
def get_spending_by_category(customer_id: str, category: str) -> Dict[str, Any]:
    """
    Calculate total spending for a specific category.
    
    Args:
        customer_id: The unique identifier for the customer
        category: The spending category to analyze (e.g., "Dining", "Shopping", "Travel", "Groceries", "Gas & Fuel")
        
    Returns:
        Dictionary containing:
        - customer_id: The customer ID
        - category: The category analyzed
        - total_amount: Total spending in this category
        - transaction_count: Number of transactions in this category
        - formatted_amount: Formatted dollar amount
    """
    
    # Fetch transactions from the Lendyr API
    base_url = "https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud"
    url = f"{base_url}/customers/by-id/{customer_id}/transactions"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        transactions = response.json()
        
        if not transactions:
            return {
                "customer_id": customer_id,
                "category": category,
                "total_amount": 0.0,
                "transaction_count": 0,
                "formatted_amount": "$0.00",
                "message": "No transactions found for this customer"
            }
        
        # Calculate spending for the specified category
        total_amount = 0.0
        transaction_count = 0
        category_lower = category.lower()
        
        for transaction in transactions:
            # Skip credits/deposits (positive amounts)
            amount = float(transaction.get("amount", 0))
            if amount >= 0:
                continue
            
            # Get transaction category
            txn_category = transaction.get("category", "").lower()
            
            # If no category, try to infer from description
            if not txn_category:
                description = transaction.get("description", "").lower()
                if "restaurant" in description or "cafe" in description or "food" in description:
                    txn_category = "dining"
                elif "store" in description or "shop" in description or "retail" in description:
                    txn_category = "shopping"
                elif "gas" in description or "fuel" in description:
                    txn_category = "gas & fuel"
                elif "hotel" in description or "airline" in description or "travel" in description:
                    txn_category = "travel"
                elif "grocery" in description or "market" in description:
                    txn_category = "groceries"
            
            # Check if this transaction matches the requested category
            if category_lower in txn_category or txn_category in category_lower:
                total_amount += abs(amount)
                transaction_count += 1
        
        return {
            "customer_id": customer_id,
            "category": category,
            "total_amount": round(total_amount, 2),
            "transaction_count": transaction_count,
            "formatted_amount": f"${total_amount:,.2f}",
            "message": f"Found {transaction_count} transactions in {category} totaling ${total_amount:,.2f}"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "customer_id": customer_id,
            "category": category,
            "error": f"Failed to fetch transaction data: {str(e)}",
            "total_amount": 0.0,
            "transaction_count": 0,
            "formatted_amount": "$0.00"
        }
    except Exception as e:
        return {
            "customer_id": customer_id,
            "category": category,
            "error": f"Error calculating spending: {str(e)}",
            "total_amount": 0.0,
            "transaction_count": 0,
            "formatted_amount": "$0.00"
        }

# Made with Bob
