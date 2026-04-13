#!/usr/bin/env python3
"""Check payment records in the database"""

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

# Check if payment_history table exists
print("Checking if payment_history table exists...")
sql = """
SELECT COUNT(*) as table_count
FROM SYSCAT.TABLES 
WHERE TABNAME = 'PAYMENT_HISTORY'
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
table_exists = row[0] > 0

if not table_exists:
    print("❌ payment_history table does NOT exist\n")
else:
    print("✅ payment_history table exists\n")
    
    # Count total payment records
    print("Counting payment records...")
    sql = "SELECT COUNT(*) as total FROM payment_history"
    stmt = ibm_db.exec_immediate(conn, sql)
    row = ibm_db.fetch_tuple(stmt)
    total_payments = row[0]
    print(f"Total payment records: {total_payments}\n")
    
    if total_payments > 0:
        # Show payment breakdown by customer
        print("Payment records by customer:")
        sql = """
        SELECT c.customer_id, c.first_name, c.last_name, c.email, 
               COUNT(ph.payment_id) as payment_count,
               SUM(CASE WHEN ph.status = 'on_time' THEN 1 ELSE 0 END) as on_time,
               SUM(CASE WHEN ph.status = 'late' THEN 1 ELSE 0 END) as late
        FROM customers c
        LEFT JOIN payment_history ph ON c.customer_id = ph.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        ORDER BY payment_count DESC
        """
        stmt = ibm_db.exec_immediate(conn, sql)
        row = ibm_db.fetch_tuple(stmt)
        while row:
            cid, fname, lname, email, count, on_time, late = row
            if count > 0:
                print(f"  ✅ {fname} {lname} ({email}): {count} payments ({on_time} on-time, {late} late)")
            else:
                print(f"  ❌ {fname} {lname} ({email}): NO payments")
            row = ibm_db.fetch_tuple(stmt)
    else:
        print("❌ No payment records found in the table\n")
        
        # Show all customers
        print("All customers in database:")
        sql = """
        SELECT customer_id, first_name, last_name, email
        FROM customers
        ORDER BY customer_id
        """
        stmt = ibm_db.exec_immediate(conn, sql)
        row = ibm_db.fetch_tuple(stmt)
        while row:
            print(f"  {row[0]}: {row[1]} {row[2]} ({row[3]})")
            row = ibm_db.fetch_tuple(stmt)

# Check loans
print("\nChecking loans...")
sql = "SELECT COUNT(*) as total FROM loans"
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
print(f"Total loans: {row[0]}")

ibm_db.close(conn)
print("\n✅ Done!")

# Made with Bob
