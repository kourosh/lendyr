#!/usr/bin/env python3
"""Show all customer names and IDs"""

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

sql = 'SELECT customer_id, first_name, last_name, email FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql)

print("Customer ID | Name                    | Email")
print("-" * 70)

row = ibm_db.fetch_assoc(stmt)
while row:
    cid = row['CUSTOMER_ID']
    first = row['FIRST_NAME']
    last = row['LAST_NAME']
    email = row['EMAIL']
    name = f"{first} {last}"
    print(f"{cid:11} | {name:23} | {email}")
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)

# Made with Bob
