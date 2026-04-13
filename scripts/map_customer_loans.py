#!/usr/bin/env python3
"""Map customers to their loans"""

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

# Get customer-loan mapping
sql = """
SELECT c.customer_id, c.first_name, c.last_name, 
       a.account_id, a.account_type,
       l.loan_id, l.loan_type, l.monthly_payment, l.term_months
FROM "LENDYR-DEMO".customers c
JOIN "LENDYR-DEMO".accounts a ON c.customer_id = a.customer_id
LEFT JOIN "LENDYR-DEMO".loans l ON a.account_id = l.account_id
WHERE l.loan_id IS NOT NULL
ORDER BY c.customer_id
"""

stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)

print('Customer-Loan Mapping:')
print('=' * 80)
while row:
    cid, fname, lname, acct_id, acct_type, loan_id, loan_type, monthly, term = row
    print(f'{cid}: {fname} {lname}')
    print(f'   Account #{acct_id} ({acct_type})')
    print(f'   Loan #{loan_id}: {loan_type} - ${float(monthly):.2f}/month for {term} months')
    print()
    row = ibm_db.fetch_tuple(stmt)

ibm_db.close(conn)

# Made with Bob
