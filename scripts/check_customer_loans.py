#!/usr/bin/env python3
"""Check loan details for customers"""

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

# First check the structure of loans table
print("Checking LOANS table structure:")
sql = """
SELECT COLNAME, TYPENAME, LENGTH
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = 'LENDYR-DEMO' AND TABNAME = 'LOANS'
ORDER BY COLNO
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
print("Columns in LOANS table:")
while row:
    print(f"  {row[0]} - {row[1]}({row[2]})")
    row = ibm_db.fetch_tuple(stmt)

print("\n" + "=" * 80)

# Get all loans
sql = 'SELECT * FROM "LENDYR-DEMO".loans'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_assoc(stmt)

print("\nAll loans in database:")
print("=" * 80)
while row:
    print(f"Loan ID: {row.get('LOAN_ID')}")
    for key, value in row.items():
        if key != 'LOAN_ID':
            print(f"  {key}: {value}")
    print()
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)

# Made with Bob
