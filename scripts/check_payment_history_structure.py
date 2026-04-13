#!/usr/bin/env python3
"""Check the structure of payment_history table"""

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

conn = ibm_db.connect(dsn, '', '')

sql = """
SELECT COLNAME, TYPENAME, LENGTH
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = 'LENDYR-DEMO' AND TABNAME = 'PAYMENT_HISTORY'
ORDER BY COLNO
"""

stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)

print('PAYMENT_HISTORY table structure:')
print('=' * 60)
col_count = 0
while row:
    col_count += 1
    print(f'{col_count}. {row[0]} - {row[1]}({row[2]})')
    row = ibm_db.fetch_tuple(stmt)

print(f'\nTotal columns: {col_count}')

# Also check one existing record to see the structure
print('\n' + '=' * 60)
print('Sample existing record:')
print('=' * 60)
sql = 'SELECT * FROM "LENDYR-DEMO".payment_history WHERE payment_id = 1'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_assoc(stmt)
if row:
    for key, value in row.items():
        print(f'{key}: {value}')

ibm_db.close(conn)

# Made with Bob
