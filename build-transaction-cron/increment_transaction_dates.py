#!/usr/bin/env python3
"""
Transaction Date Incrementer
Updates all transaction dates so the most recent transaction is dated today,
with older transactions incrementing backwards from that date.
This keeps transaction data current and realistic.

Usage:
    python increment_transaction_dates.py

Environment Variables Required:
    - DRIVER: DB2 driver
    - DATABASE: Database name
    - DSN_HOSTNAME: DB2 hostname
    - DSN_PORT: DB2 port
    - PROTOCOL: Connection protocol
    - USERNAME: DB2 username
    - PASSWORD: DB2 password
    - SECURITY: Security setting (SSL)
"""

import ibm_db
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


def get_db_connection():
    """Get database connection using environment variables"""
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
    return ibm_db.connect(dsn, "", "")


def increment_transaction_dates():
    """
    Update all transaction dates so the most recent transaction is dated today.
    
    Strategy:
    1. Find the current maximum transaction date
    2. Calculate the difference between today and that max date
    3. Add that difference to all transaction dates
    
    This ensures the most recent transaction is always today, and all other
    transactions maintain their relative spacing but shift forward in time.
    """
    conn = None
    try:
        conn = get_db_connection()
        
        if not conn:
            raise Exception("Failed to establish database connection")
            
        print(f"[{datetime.now().isoformat()}] Connected to database successfully")
        
        # First, get the current maximum transaction date
        max_date_sql = '''
        SELECT MAX(created_at) as max_date 
        FROM "LENDYR-DEMO".TRANSACTIONS
        '''
        
        stmt = ibm_db.exec_immediate(conn, max_date_sql)
        if stmt is False or stmt is None:
            raise Exception("Failed to query max transaction date")
        
        row = ibm_db.fetch_assoc(stmt)
        if not row or not row.get('MAX_DATE'):
            print(f"[{datetime.now().isoformat()}] No transactions found in database")
            return True
        
        max_date_value = row['MAX_DATE']
        print(f"[{datetime.now().isoformat()}] Current max transaction date: {max_date_value}")
        
        # Parse the max date - handle both string and datetime objects
        if isinstance(max_date_value, datetime):
            max_date = max_date_value
        else:
            # Parse string format: YYYY-MM-DD HH:MM:SS
            max_date = datetime.strptime(str(max_date_value), '%Y-%m-%d %H:%M:%S')
        today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        
        # Calculate days difference
        days_diff = (today - max_date).days
        
        print(f"[{datetime.now().isoformat()}] Today's date: {today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[{datetime.now().isoformat()}] Days to add: {days_diff}")
        
        if days_diff == 0:
            print(f"[{datetime.now().isoformat()}] Transactions are already current. No update needed.")
            return True
        
        # SQL to increment all transaction dates by the calculated number of days
        # Using DB2's date arithmetic: created_at + X DAYS
        update_sql = f'''
        UPDATE "LENDYR-DEMO".TRANSACTIONS
        SET created_at = created_at + {days_diff} DAYS
        '''
        
        print(f"[{datetime.now().isoformat()}] Executing date increment...")
        stmt = ibm_db.exec_immediate(conn, update_sql)
        
        if stmt is False or stmt is None:
            raise Exception("Failed to execute SQL statement")
        
        # Get number of rows affected
        rows_affected = ibm_db.num_rows(stmt)  # type: ignore
        
        # Commit the transaction
        ibm_db.commit(conn)
        
        print(f"[{datetime.now().isoformat()}] Successfully updated {rows_affected} transaction records")
        print(f"[{datetime.now().isoformat()}] All transaction dates have been moved forward by {days_diff} days")
        print(f"[{datetime.now().isoformat()}] Most recent transaction is now dated: {today.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ERROR: Failed to increment transaction dates", file=sys.stderr)
        print(f"[{datetime.now().isoformat()}] Error details: {str(e)}", file=sys.stderr)
        return False
    finally:
        # Close connection
        if conn:
            ibm_db.close(conn)


def verify_environment():
    """Verify all required environment variables are set"""
    required_vars = [
        'DRIVER', 'DATABASE', 'DSN_HOSTNAME', 'DSN_PORT',
        'PROTOCOL', 'USERNAME', 'PASSWORD', 'SECURITY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}", file=sys.stderr)
        print("Please set these variables or create a .env file", file=sys.stderr)
        return False
    
    return True


if __name__ == "__main__":
    print(f"[{datetime.now().isoformat()}] Starting transaction date increment")
    
    # Verify environment
    if not verify_environment():
        sys.exit(1)
    
    # Increment dates
    success = increment_transaction_dates()
    
    if success:
        print(f"[{datetime.now().isoformat()}] Transaction date increment completed successfully")
        sys.exit(0)
    else:
        print(f"[{datetime.now().isoformat()}] Transaction date increment failed", file=sys.stderr)
        sys.exit(1)

# Made with Bob