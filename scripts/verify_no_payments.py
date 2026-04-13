#!/usr/bin/env python3
"""Verify that customers have no payment records"""

import ibm_db
import os
from dotenv import load_dotenv

load_dotenv('lendyr_code_engine/.env')

dsn = (
    f"DRIVER={os.getenv('DRIVER')};"
    f"DATABASE={os.getenv('DATABASE')};"
    f"HOSTNAME={os.getenv('DSN_HOSTNAME')};"
    f"PORT={os.getenv('DSN_PORT')};"
    f"PROTOCOL={os.getenv('PROTOCOL')};"
    f"UID={os.getenv('USERNAME')};"
    f"PWD={os.getenv('PASSWORD')};"
    f"SECURITY={os.getenv('SECURITY')};"
)

print("Connecting to DB2...")
conn = ibm_db.connect(dsn, "", "")
print("✅ Connected!\n")

# Show all customers
print("=" * 60)
print("ALL CUSTOMERS IN DATABASE")
print("=" * 60)
sql = """
SELECT customer_id, first_name, last_name, email
FROM "LENDYR-DEMO".customers
ORDER BY customer_id
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
customer_count = 0
while row:
    customer_count += 1
    print(f"  {row[0]}: {row[1]} {row[2]} ({row[3]})")
    row = ibm_db.fetch_tuple(stmt)

print(f"\nTotal customers: {customer_count}")

# Count loans
print("\n" + "=" * 60)
print("LOANS IN DATABASE")
print("=" * 60)
sql = 'SELECT COUNT(*) FROM "LENDYR-DEMO".loans'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
loan_count = row[0]
print(f"Total loans: {loan_count}")

# Check payment_history table
print("\n" + "=" * 60)
print("PAYMENT RECORDS")
print("=" * 60)
sql = 'SELECT COUNT(*) FROM "LENDYR-DEMO".payment_history'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
payment_count = row[0]

if payment_count > 0:
    print(f"✅ Found {payment_count} payment records\n")
    
    # Show payment breakdown by customer
    sql = """
    SELECT c.customer_id, c.first_name, c.last_name, c.email, 
           COUNT(ph.payment_id) as payment_count
    FROM "LENDYR-DEMO".customers c
    LEFT JOIN "LENDYR-DEMO".payment_history ph ON c.customer_id = ph.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.email
    ORDER BY payment_count DESC
    """
    stmt = ibm_db.exec_immediate(conn, sql)
    row = ibm_db.fetch_tuple(stmt)
    customers_with_payments = 0
    customers_without_payments = 0
    
    print("Payment records by customer:")
    while row:
        cid, fname, lname, email, count = row
        if count > 0:
            customers_with_payments += 1
            print(f"  ✅ {fname} {lname} ({email}): {count} payments")
        else:
            customers_without_payments += 1
            print(f"  ❌ {fname} {lname} ({email}): NO payments")
        row = ibm_db.fetch_tuple(stmt)
    
    print(f"\nCustomers WITH payments: {customers_with_payments}")
    print(f"Customers WITHOUT payments: {customers_without_payments}")
else:
    print("❌ NO payment records found in payment_history table")
    print("❌ All customers have ZERO payment records")

# Final summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✅ Database has {customer_count} customers")
print(f"✅ Database has {loan_count} loans")
print(f"{'✅' if payment_count > 0 else '❌'} Database has {payment_count} payment records")

if payment_count == 0:
    print("\n🔴 CONFIRMED: No customers have made any payments!")

ibm_db.close(conn)
print("\n✅ Verification complete!")

# Made with Bob
