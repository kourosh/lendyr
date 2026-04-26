import requests
import json

# Test the tool with customer 846307 for different categories
customer_id = "846307"
categories = ["Travel", "Shopping", "Transport", "Dining", "Groceries"]

print("\n" + "="*80)
print(f"SPENDING BY CATEGORY FOR CUSTOMER {customer_id}")
print("="*80)
print(f"{'Category':<20} {'Amount':<15} {'Transactions':<15} {'Status'}")
print("-"*80)

for category in categories:
    # Fetch transactions
    url = f"https://lendyr-db2-api.28d7yzowjq08.us-south.codeengine.appdomain.cloud/customers/by-id/{customer_id}/transactions"
    response = requests.get(url, timeout=10)
    transactions = response.json()
    
    # Calculate spending for this category
    total = 0.0
    count = 0
    
    for txn in transactions:
        if txn.get("transaction_type") == "debit":
            merchant_cat = txn.get("merchant_category", "")
            if category.lower() in merchant_cat.lower():
                total += float(txn.get("amount", 0))
                count += 1
    
    status = "✓" if count > 0 else "-"
    print(f"{category:<20} ${total:>12,.2f} {count:>14} {status:>15}")

print("="*80)
