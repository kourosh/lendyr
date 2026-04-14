#!/usr/bin/env python3
"""Update customer IDs to use new numbering scheme (846301, 846302, etc.)"""

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

# Get current customers
sql = 'SELECT customer_id, first_name, last_name FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql)

customers = []
row = ibm_db.fetch_assoc(stmt)
while row:
    customers.append({
        'old_id': row['CUSTOMER_ID'],
        'new_id': 846300 + row['CUSTOMER_ID'],
        'name': f"{row['FIRST_NAME']} {row['LAST_NAME']}"
    })
    row = ibm_db.fetch_assoc(stmt)

print("Customer ID Mapping:")
print("=" * 60)
for c in customers:
    print(f"{c['name']:20} | {c['old_id']:3} -> {c['new_id']}")
print()

# Update in reverse order to avoid conflicts
print("\nUpdating customer IDs...")
print("=" * 60)

# First, update to temporary negative IDs to avoid conflicts
for c in reversed(customers):
    temp_id = -c['new_id']
    sql = f'UPDATE "LENDYR-DEMO".CUSTOMERS SET customer_id = {temp_id} WHERE customer_id = {c["old_id"]}'
    stmt = ibm_db.exec_immediate(conn, sql)
    print(f"Step 1: {c['name']:20} | {c['old_id']} -> {temp_id} (temp)")

print()

# Then update to final positive IDs
for c in customers:
    temp_id = -c['new_id']
    sql = f'UPDATE "LENDYR-DEMO".CUSTOMERS SET customer_id = {c["new_id"]} WHERE customer_id = {temp_id}'
    stmt = ibm_db.exec_immediate(conn, sql)
    print(f"Step 2: {c['name']:20} | {temp_id} (temp) -> {c['new_id']}")

print("\n✅ Customer IDs updated successfully!")

# Verify the changes
print("\nVerifying updated customer IDs:")
print("=" * 60)
sql = 'SELECT customer_id, first_name, last_name FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_assoc(stmt)
while row:
    print(f"{row['CUSTOMER_ID']:6} | {row['FIRST_NAME']} {row['LAST_NAME']}")
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)

# Made with Bob
