#!/usr/bin/env python3
"""
Add Lendyr Travel Rewards credit cards to 7 of 10 customers with random travel points (0-200,000)
"""

import ibm_db
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv('lendyr_code_engine/.env')

# Database connection
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

print("=" * 80)
print("LENDYR TRAVEL REWARDS CARD SETUP")
print("=" * 80)

print("\n1. Connecting to DB2...")
conn = ibm_db.connect(dsn, "", "")
print("✅ Connected!\n")

# Step 1: Get all customers
print("2. Fetching all customers...")
sql_customers = 'SELECT customer_id, first_name, last_name, email FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id'
stmt = ibm_db.exec_immediate(conn, sql_customers)

customers = []
row = ibm_db.fetch_assoc(stmt)
while row:
    customers.append({
        'customer_id': row['CUSTOMER_ID'],
        'first_name': row['FIRST_NAME'],
        'last_name': row['LAST_NAME'],
        'email': row['EMAIL']
    })
    row = ibm_db.fetch_assoc(stmt)

print(f"✅ Found {len(customers)} customers\n")
for c in customers:
    print(f"   {c['customer_id']:11} | {c['first_name']} {c['last_name']}")

# Step 2: Check existing card structure
print("\n3. Checking existing card structure...")
sql_cards = 'SELECT * FROM "LENDYR-DEMO".CARDS LIMIT 1'
stmt = ibm_db.exec_immediate(conn, sql_cards)
row = ibm_db.fetch_assoc(stmt)

if row:
    print("✅ Card table structure:")
    for key in row.keys():
        print(f"   - {key}")
else:
    print("⚠️  No existing cards found")

# Step 3: Check existing accounts to understand account_id structure
print("\n4. Checking existing accounts...")
sql_accounts = 'SELECT account_id, customer_id, account_type FROM "LENDYR-DEMO".ACCOUNTS ORDER BY customer_id LIMIT 5'
stmt = ibm_db.exec_immediate(conn, sql_accounts)

print("✅ Sample accounts:")
row = ibm_db.fetch_assoc(stmt)
while row:
    print(f"   Account ID: {row['ACCOUNT_ID']}, Customer: {row['CUSTOMER_ID']}, Type: {row['ACCOUNT_TYPE']}")
    row = ibm_db.fetch_assoc(stmt)

# Step 4: Select 7 random customers
print("\n5. Selecting 7 random customers for Travel Rewards cards...")
selected_customers = random.sample(customers, 7)
print("✅ Selected customers:")
for c in selected_customers:
    print(f"   {c['customer_id']:11} | {c['first_name']} {c['last_name']}")

# Step 5: Get the next available card_id
print("\n6. Getting next available card_id...")
sql_max_card = 'SELECT MAX(card_id) as max_id FROM "LENDYR-DEMO".CARDS'
stmt = ibm_db.exec_immediate(conn, sql_max_card)
row = ibm_db.fetch_assoc(stmt)
next_card_id = (row['MAX_ID'] or 0) + 1
print(f"✅ Next card_id will be: {next_card_id}")

# Step 6: Get the next available account_id
print("\n7. Getting next available account_id...")
sql_max_account = 'SELECT MAX(account_id) as max_id FROM "LENDYR-DEMO".ACCOUNTS'
stmt = ibm_db.exec_immediate(conn, sql_max_account)
row = ibm_db.fetch_assoc(stmt)
next_account_id = (row['MAX_ID'] or 0) + 1
print(f"✅ Next account_id will be: {next_account_id}")

# Step 7: Create Travel Rewards accounts and cards
print("\n8. Creating Travel Rewards accounts and cards...")
print("=" * 80)

for i, customer in enumerate(selected_customers):
    account_id = next_account_id + i
    card_id = next_card_id + i
    travel_points = random.randint(0, 200000)
    
    # Create credit account for Travel Rewards card
    # Generate account number (format: 8 digits)
    account_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    
    sql_insert_account = '''
        INSERT INTO "LENDYR-DEMO".ACCOUNTS
        (account_id, customer_id, account_number, account_type, balance, status,
         credit_limit, interest_rate, opened_at, currency)
        VALUES (?, ?, ?, 'credit', 0.00, 'active',
                10000.00, 18.99, CURRENT_TIMESTAMP, 'USD')
    '''
    
    stmt = ibm_db.prepare(conn, sql_insert_account)
    ibm_db.bind_param(stmt, 1, account_id)
    ibm_db.bind_param(stmt, 2, customer['customer_id'])
    ibm_db.bind_param(stmt, 3, account_number)
    ibm_db.execute(stmt)
    
    # Create Travel Rewards card
    # Generate a random 16-digit card number
    card_number = '4' + ''.join([str(random.randint(0, 9)) for _ in range(15)])
    
    sql_insert_card = '''
        INSERT INTO "LENDYR-DEMO".CARDS
        (card_id, customer_id, account_id, card_number, card_type, network,
         status, daily_limit, expiry_date, issued_at, rewards_points)
        VALUES (?, ?, ?, ?, 'Travel Rewards', 'Visa',
                'active', 5000.00, '2029-12-31', CURRENT_TIMESTAMP, ?)
    '''
    
    stmt = ibm_db.prepare(conn, sql_insert_card)
    ibm_db.bind_param(stmt, 1, card_id)
    ibm_db.bind_param(stmt, 2, customer['customer_id'])
    ibm_db.bind_param(stmt, 3, account_id)
    ibm_db.bind_param(stmt, 4, card_number)
    ibm_db.bind_param(stmt, 5, travel_points)
    ibm_db.execute(stmt)
    
    print(f"✅ Created for {customer['first_name']} {customer['last_name']}:")
    print(f"   Account ID: {account_id}")
    print(f"   Card ID: {card_id}")
    print(f"   Card Number: {card_number}")
    print(f"   Travel Points: {travel_points:,}")
    print()

print("=" * 80)
print("9. Verifying created cards...")

# Verify the cards were created
for customer in selected_customers:
    sql_verify = '''
        SELECT c.card_id, c.card_type, c.rewards_points, c.status
        FROM "LENDYR-DEMO".CARDS c
        WHERE c.customer_id = ? AND c.card_type = 'Travel Rewards'
    '''
    stmt = ibm_db.prepare(conn, sql_verify)
    ibm_db.bind_param(stmt, 1, customer['customer_id'])
    ibm_db.execute(stmt)
    
    row = ibm_db.fetch_assoc(stmt)
    if row:
        print(f"✅ {customer['first_name']} {customer['last_name']}: Card ID {row['CARD_ID']}, {row['REWARDS_POINTS']:,} points")
    else:
        print(f"❌ {customer['first_name']} {customer['last_name']}: Card not found!")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Successfully created {len(selected_customers)} Travel Rewards cards")
print(f"✅ Travel points range: 0 to 200,000")
print("=" * 80)

ibm_db.close(conn)
print("\n✅ Database connection closed")
print("✅ Script completed successfully!")

# Made with Bob
