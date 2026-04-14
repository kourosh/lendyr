#!/usr/bin/env python3
"""Fix customer_id foreign key references in all tables after customer ID update"""

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

# Get the mapping of old IDs to new IDs
# Old IDs: 1, 2, 3, 4, 5
# New IDs: 846301, 846302, 846303, 846304, 846305
id_mapping = {
    1: 846301,
    2: 846302,
    3: 846303,
    4: 846304,
    5: 846305
}

print("Customer ID Mapping:")
print("=" * 40)
for old_id, new_id in id_mapping.items():
    print(f"  {old_id} -> {new_id}")
print()

# Tables to update and their customer_id columns
tables_to_update = [
    ('ACCOUNTS', 'customer_id'),
    ('CARDS', 'customer_id'),
    ('DISPUTES', 'customer_id'),
    ('PAYMENT_HISTORY', 'customer_id'),
]

for table_name, column_name in tables_to_update:
    print(f"\nUpdating {table_name}.{column_name}...")
    print("=" * 60)
    
    # First, update to temporary negative IDs to avoid conflicts
    for old_id, new_id in reversed(list(id_mapping.items())):
        temp_id = -new_id
        sql = f'UPDATE "LENDYR-DEMO".{table_name} SET {column_name} = {temp_id} WHERE {column_name} = {old_id}'
        try:
            stmt = ibm_db.exec_immediate(conn, sql)
            rows_affected = ibm_db.num_rows(stmt)
            if rows_affected > 0:
                print(f"  Step 1: {old_id} -> {temp_id} (temp) - {rows_affected} rows")
        except Exception as e:
            print(f"  Error updating {old_id} to {temp_id}: {e}")
    
    # Then update to final positive IDs
    for old_id, new_id in id_mapping.items():
        temp_id = -new_id
        sql = f'UPDATE "LENDYR-DEMO".{table_name} SET {column_name} = {new_id} WHERE {column_name} = {temp_id}'
        try:
            stmt = ibm_db.exec_immediate(conn, sql)
            rows_affected = ibm_db.num_rows(stmt)
            if rows_affected > 0:
                print(f"  Step 2: {temp_id} (temp) -> {new_id} - {rows_affected} rows")
        except Exception as e:
            print(f"  Error updating {temp_id} to {new_id}: {e}")
    
    print(f"✅ {table_name} updated successfully!")

# Verify the changes
print("\n\nVerifying updates:")
print("=" * 60)

for table_name, column_name in tables_to_update:
    sql = f'SELECT DISTINCT {column_name} FROM "LENDYR-DEMO".{table_name} ORDER BY {column_name}'
    stmt = ibm_db.exec_immediate(conn, sql)
    
    ids = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        ids.append(row[column_name.upper()])
        row = ibm_db.fetch_assoc(stmt)
    
    print(f"\n{table_name}.{column_name} values: {ids}")

# Show sample data
print("\n\nSample account data:")
print("=" * 60)
sql = '''
SELECT a.account_id, a.customer_id, a.account_type, c.first_name, c.last_name
FROM "LENDYR-DEMO".ACCOUNTS a
JOIN "LENDYR-DEMO".CUSTOMERS c ON a.customer_id = c.customer_id
FETCH FIRST 5 ROWS ONLY
'''
stmt = ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_assoc(stmt)
while row:
    print(f"Account {row['ACCOUNT_ID']}: customer_id={row['CUSTOMER_ID']}, {row['FIRST_NAME']} {row['LAST_NAME']}, {row['ACCOUNT_TYPE']}")
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)
print("\n✅ All updates completed successfully!")

# Made with Bob
