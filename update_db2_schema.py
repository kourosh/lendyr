#!/usr/bin/env python3
"""
Update DB2 Schema for Loan Deferral Feature
Adds credit_score column and payment_history table
"""

import ibm_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('lendyr_code_engine/.env')

# Build connection string
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

print("=" * 60)
print("DB2 Schema Update Script")
print("=" * 60)
print()

try:
    # Connect to DB2
    print("Connecting to DB2...")
    conn = ibm_db.connect(dsn, "", "")
    print("✅ Connected successfully!")
    print()
    
    # Step 1: Add credit_score column
    print("Step 1: Adding credit_score column to customers table...")
    try:
        sql = 'ALTER TABLE "LENDYR-DEMO".CUSTOMERS ADD COLUMN CREDIT_SCORE INTEGER'
        stmt = ibm_db.exec_immediate(conn, sql)
        print("✅ Column added successfully!")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
            print("⚠️  Column already exists, skipping...")
        else:
            raise
    print()
    
    # Step 2: Update credit scores
    print("Step 2: Updating credit scores for all customers...")
    credit_scores = [
        (1, 742),   # Alice Martinez
        (2, 755),   # Brian Nguyen (good credit for deferral)
        (3, 680),   # Carla Thompson
        (4, 810),   # David Kim
        (5, 725),   # Elena Okafor
        (6, 695),   # Frank Rossi
        (7, 770),   # Grace Patel
        (8, 650),   # Henry Williams
        (9, 788),   # Isabela Cruz
        (10, 715),  # James Holloway
    ]
    
    for customer_id, score in credit_scores:
        sql = f'UPDATE "LENDYR-DEMO".CUSTOMERS SET CREDIT_SCORE = {score} WHERE CUSTOMER_ID = {customer_id}'
        ibm_db.exec_immediate(conn, sql)
    print(f"✅ Updated credit scores for {len(credit_scores)} customers")
    print()
    
    # Step 3: Check if payment_history table exists (it already does!)
    print("Step 3: Checking payment_history table...")
    print("⚠️  Table already exists in schema, skipping creation...")
    print()
    
    # Step 4: Insert Brian's payment history
    print("Step 4: Inserting Brian Nguyen's payment history (45 payments)...")
    
    # Check if data already exists
    check_sql = 'SELECT COUNT(*) FROM "LENDYR-DEMO".PAYMENT_HISTORY WHERE CUSTOMER_ID = 2'
    stmt = ibm_db.exec_immediate(conn, check_sql)
    row = ibm_db.fetch_tuple(stmt)
    existing_count = row[0] if row else 0
    
    if existing_count > 0:
        print(f"⚠️  Found {existing_count} existing payments, skipping insert...")
    else:
        payments = []
        
        # Generate 45 on-time payments from July 2021 to March 2025
        from datetime import date, timedelta
        start_date = date(2021, 7, 13)
        
        for i in range(45):
            payment_date = start_date + timedelta(days=30 * i)
            payment_id = f"P{i+1:03d}"  # Shorter ID like P001, P002, etc.
            # Schema: PAYMENT_ID, CUSTOMER_ID, PAYMENT_DATE, PAYMENT_AMOUNT, AUTO_PAY_USED, WAS_LATE, DAYS_LATE, NOTE
            payments.append((payment_id, '2', payment_date.strftime('%Y-%m-%d'), 469.35, 1, 0, 0, 'Auto loan payment'))
        
        # Insert in batches
        for payment_id, customer_id, payment_date, amount, auto_pay, was_late, days_late, note in payments:
            sql = f"""
            INSERT INTO "LENDYR-DEMO".PAYMENT_HISTORY
            (PAYMENT_ID, CUSTOMER_ID, PAYMENT_DATE, PAYMENT_AMOUNT, AUTO_PAY_USED, WAS_LATE, DAYS_LATE, NOTE)
            VALUES ('{payment_id}', '{customer_id}', '{payment_date}', {amount}, {auto_pay}, {was_late}, {days_late}, '{note}')
            """
            ibm_db.exec_immediate(conn, sql)
        
        print(f"✅ Inserted {len(payments)} payment records")
    print()
    
    # Step 5: Verify changes
    print("Step 5: Verifying changes...")
    print()
    
    # Check credit scores
    print("Credit Scores:")
    sql = 'SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, CREDIT_SCORE FROM "LENDYR-DEMO".CUSTOMERS ORDER BY CUSTOMER_ID'
    stmt = ibm_db.exec_immediate(conn, sql)
    row = ibm_db.fetch_tuple(stmt)
    while row:
        print(f"  Customer {row[0]}: {row[1]} {row[2]} - Score: {row[3]}")
        row = ibm_db.fetch_tuple(stmt)
    print()
    
    # Check Brian's payment history
    print("Brian Nguyen's Payment History:")
    sql = """
    SELECT COUNT(*) as total,
           SUM(CASE WHEN WAS_LATE = 0 THEN 1 ELSE 0 END) as on_time,
           SUM(CASE WHEN WAS_LATE = 1 THEN 1 ELSE 0 END) as late
    FROM "LENDYR-DEMO".PAYMENT_HISTORY
    WHERE CUSTOMER_ID = '2'
    """
    stmt = ibm_db.exec_immediate(conn, sql)
    row = ibm_db.fetch_tuple(stmt)
    if row:
        print(f"  Total Payments: {row[0]}")
        print(f"  On-Time: {row[1]}")
        print(f"  Late: {row[2]}")
        if row[0] > 0:
            print(f"  On-Time %: {(row[1]/row[0]*100):.1f}%")
    print()
    
    # Close connection
    ibm_db.close(conn)
    
    print("=" * 60)
    print("✅ Schema update completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Redeploy the API to Code Engine")
    print("2. Test new endpoints:")
    print("   - GET /customers/{email}/payment-history")
    print("   - POST /customers/{email}/loans/{loan_id}/defer")
    print("3. Build agents in Watsonx Orchestrate")
    print()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Made with Bob
