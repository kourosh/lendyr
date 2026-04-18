#!/usr/bin/env python3
"""Get customer phone number by name"""

import ibm_db
import os
import sys
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

# Get search name from command line or use default
search_name = sys.argv[1] if len(sys.argv) > 1 else "alice martinez"
first_name, last_name = search_name.lower().split()[:2]

print(f"Searching for: {first_name.title()} {last_name.title()}")
print("Connecting to DB2...")
conn = ibm_db.connect(dsn, "", "")
print("✅ Connected!\n")

sql = '''
SELECT customer_id, first_name, last_name, email, phone 
FROM "LENDYR-DEMO".CUSTOMERS 
WHERE LOWER(first_name) = ? AND LOWER(last_name) = ?
'''

stmt = ibm_db.prepare(conn, sql)
ibm_db.bind_param(stmt, 1, first_name.lower())
ibm_db.bind_param(stmt, 2, last_name.lower())
ibm_db.execute(stmt)

row = ibm_db.fetch_assoc(stmt)
if row:
    print(f"Customer ID: {row['CUSTOMER_ID']}")
    print(f"Name: {row['FIRST_NAME']} {row['LAST_NAME']}")
    print(f"Email: {row['EMAIL']}")
    print(f"Phone: {row['PHONE']}")
else:
    print(f"❌ Customer not found: {first_name.title()} {last_name.title()}")

ibm_db.close(conn)

# Made with Bob
