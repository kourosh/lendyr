#!/usr/bin/env python3
"""Add PIN column to CUSTOMERS table and populate with 5-digit numbers"""

import ibm_db
import os
import random
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

# Check if PIN column already exists
print("Checking if PIN column exists...")
sql = """
SELECT COLNAME 
FROM SYSCAT.COLUMNS 
WHERE TABSCHEMA = 'LENDYR-DEMO' AND TABNAME = 'CUSTOMERS' AND COLNAME = 'PIN'
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_assoc(stmt)

if row:
    print("⚠️  PIN column already exists. Updating values...\n")
else:
    print("Adding PIN column to CUSTOMERS table...")
    sql = 'ALTER TABLE "LENDYR-DEMO".CUSTOMERS ADD COLUMN pin VARCHAR(5)'
    try:
        stmt = ibm_db.exec_immediate(conn, sql)
        print("✅ PIN column added successfully!\n")
    except Exception as e:
        print(f"Error adding column: {e}\n")

# Get all customers
sql = 'SELECT customer_id, first_name, last_name FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql)

customers = []
row = ibm_db.fetch_assoc(stmt)
while row:
    customers.append({
        'id': row['CUSTOMER_ID'],
        'name': f"{row['FIRST_NAME']} {row['LAST_NAME']}"
    })
    row = ibm_db.fetch_assoc(stmt)

# Generate and assign PINs
print("Assigning 5-digit PINs to customers:")
print("=" * 60)

random.seed(42)  # For reproducible PINs
used_pins = set()

for customer in customers:
    # Generate unique 5-digit PIN
    while True:
        pin = str(random.randint(10000, 99999))
        if pin not in used_pins:
            used_pins.add(pin)
            break
    
    # Update customer with PIN
    sql = f'UPDATE "LENDYR-DEMO".CUSTOMERS SET pin = \'{pin}\' WHERE customer_id = {customer["id"]}'
    stmt = ibm_db.exec_immediate(conn, sql)
    print(f"Customer {customer['id']} ({customer['name']:20}) | PIN: {pin}")

print("\n✅ PINs assigned successfully!")

# Verify the changes
print("\nVerifying customer data with PINs:")
print("=" * 80)
sql = 'SELECT customer_id, first_name, last_name, email, pin FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql)

print(f"{'Customer ID':<12} | {'Name':<20} | {'Email':<30} | {'PIN':<5}")
print("-" * 80)

row = ibm_db.fetch_assoc(stmt)
while row:
    cid = row['CUSTOMER_ID']
    name = f"{row['FIRST_NAME']} {row['LAST_NAME']}"
    email = row['EMAIL']
    pin = row['PIN'] if row['PIN'] else 'N/A'
    print(f"{cid:<12} | {name:<20} | {email:<30} | {pin:<5}")
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)

# Made with Bob
