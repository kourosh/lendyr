#!/usr/bin/env python3
"""Check what tables exist in DB2"""

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

# List all tables
print("Available tables:")
sql = """
SELECT TABSCHEMA, TABNAME, TYPE 
FROM SYSCAT.TABLES 
WHERE TABSCHEMA NOT LIKE 'SYS%' 
ORDER BY TABSCHEMA, TABNAME
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
while row:
    print(f"  {row[0]}.{row[1]} ({row[2]})")
    row = ibm_db.fetch_tuple(stmt)

print("\nChecking CUSTOMERS table structure:")
sql = """
SELECT COLNAME, TYPENAME, LENGTH, NULLS
FROM SYSCAT.COLUMNS
WHERE TABNAME = 'CUSTOMERS'
ORDER BY COLNO
"""
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
if row:
    print("  Columns:")
    while row:
        print(f"    {row[0]} - {row[1]}({row[2]}) NULL={row[3]}")
        row = ibm_db.fetch_tuple(stmt)
else:
    print("  No CUSTOMERS table found")

ibm_db.close(conn)

# Made with Bob
