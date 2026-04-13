#!/usr/bin/env python3
"""Insert payment histories for 5 customers into the database"""

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

# Read the SQL file
print("Reading SQL file...")
with open('scripts/add_payment_histories_v2.sql', 'r') as f:
    sql_content = f.read()

# Split into individual statements (filter out comments and verification queries)
statements = []
for line in sql_content.split('\n'):
    line = line.strip()
    if line.startswith('INSERT INTO'):
        statements.append(line)

print(f"Found {len(statements)} INSERT statements\n")

# Execute each INSERT statement
success_count = 0
error_count = 0

print("Inserting payment records...")
for i, stmt in enumerate(statements, 1):
    try:
        ibm_db.exec_immediate(conn, stmt)
        success_count += 1
        if i % 10 == 0:
            print(f"  Inserted {i}/{len(statements)} records...")
    except Exception as e:
        error_count += 1
        print(f"  ❌ Error on statement {i}: {e}")

print(f"\n✅ Insertion complete!")
print(f"   Success: {success_count}")
print(f"   Errors: {error_count}")

# Verify the results
print("\n" + "=" * 80)
print("VERIFICATION: Payment counts by customer")
print("=" * 80)

sql = """
SELECT c.customer_id, c.first_name, c.last_name,
       COUNT(ph.payment_id) as total_payments,
       SUM(CASE WHEN ph.was_late = 0 THEN 1 ELSE 0 END) as on_time,
       SUM(CASE WHEN ph.was_late = 1 THEN 1 ELSE 0 END) as late
FROM "LENDYR-DEMO".customers c
LEFT JOIN "LENDYR-DEMO".payment_history ph ON CAST(c.customer_id AS VARCHAR(50)) = ph.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(ph.payment_id) > 0
ORDER BY total_payments DESC
"""

stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)

while row:
    cid, fname, lname, total, on_time, late = row
    print(f"{cid}: {fname} {lname}")
    print(f"   Total: {total} payments ({on_time} on-time, {late} late)")
    row = ibm_db.fetch_tuple(stmt)

# Total count
print("\n" + "=" * 80)
sql = 'SELECT COUNT(*) FROM "LENDYR-DEMO".payment_history'
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)
print(f"Total payment records in database: {row[0]}")

ibm_db.close(conn)
print("\n✅ Done!")

# Made with Bob
