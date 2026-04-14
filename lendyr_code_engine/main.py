"""
Lendyr Bank Demo API
FastAPI + DB2 Database — deployed on IBM Code Engine
Connects to external DB2 database for all data operations.
"""

import os
from typing import Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ibm_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Lendyr Bank API",
    description="Customer care REST API for the Lendyr Bank watsonx Orchestrate demo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Database Connection ─────────────────────────────────────────────────────

# DB2 connection parameters
dsn_driver = os.getenv("DRIVER")
dsn_database = os.getenv("DATABASE")
dsn_hostname = os.getenv("DSN_HOSTNAME")
dsn_port = os.getenv("DSN_PORT")
dsn_protocol = os.getenv("PROTOCOL")
dsn_uid = os.getenv("USERNAME")
dsn_pwd = os.getenv("PASSWORD")
dsn_security = os.getenv("SECURITY")


def mask_value(value: str | None, visible: int = 2) -> str:
    if not value:
        return "<missing>"
    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}{'*' * (len(value) - (visible * 2))}{value[-visible:]}"


required_env = {
    "DRIVER": dsn_driver,
    "DATABASE": dsn_database,
    "DSN_HOSTNAME": dsn_hostname,
    "DSN_PORT": dsn_port,
    "PROTOCOL": dsn_protocol,
    "USERNAME": dsn_uid,
    "PASSWORD": dsn_pwd,
    "SECURITY": dsn_security,
}

missing_env = [key for key, value in required_env.items() if not value]
if missing_env:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_env)}")

print("---- DB2 Connection Diagnostics -----")
print(f"DRIVER={dsn_driver}")
print(f"DATABASE={dsn_database}")
print(f"HOSTNAME={dsn_hostname}")
print(f"PORT={dsn_port}")
print(f"PROTOCOL={dsn_protocol}")
print(f"USERNAME={mask_value(dsn_uid)}")
print(f"PASSWORD={'<set>' if dsn_pwd else '<missing>'}")
print(f"SECURITY={dsn_security}")

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# Global database connection
db_conn = None


def require_db_conn():
    if db_conn is None:
        raise RuntimeError("Database connection is not initialized")
    return db_conn

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    global db_conn
    try:
        db_conn = ibm_db.connect(dsn, "", "")
        print("✓ Connected to DB2 database")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    global db_conn
    if db_conn:
        try:
            ibm_db.close(db_conn)
            print("✓ Database connection closed")
        except:
            pass

# ─── Database Helper Functions ───────────────────────────────────────────────

def query_db(sql: str, params: tuple[Any, ...] | None = None) -> list[dict]:
    """Execute SQL query and return results as list of dicts"""
    conn = require_db_conn()

    if params:
        stmt = ibm_db.prepare(conn, sql)
        if not stmt:
            raise RuntimeError(f"Failed to prepare SQL statement: {sql}")
        for idx, value in enumerate(params):
            ibm_db.bind_param(stmt, idx + 1, value)
        ibm_db.execute(stmt)
    else:
        stmt = ibm_db.exec_immediate(conn, sql)
        if not stmt:
            raise RuntimeError(f"Failed to execute SQL statement: {sql}")

    results = []
    row = ibm_db.fetch_assoc(stmt)
    while row and isinstance(row, dict):
        # Convert all values, handling None
        cleaned_row = {}
        for key, value in row.items():
            if value is None:
                cleaned_row[key] = None
            else:
                cleaned_row[key] = value
        results.append(cleaned_row)
        row = ibm_db.fetch_assoc(stmt)

    return results

def execute_update(sql: str, params: tuple[Any, ...]) -> bool:
    """Execute UPDATE/INSERT/DELETE statement"""
    conn = require_db_conn()

    stmt = ibm_db.prepare(conn, sql)
    if not stmt:
        raise RuntimeError(f"Failed to prepare SQL statement: {sql}")

    for idx, value in enumerate(params):
        ibm_db.bind_param(stmt, idx + 1, value)

    result = ibm_db.execute(stmt)
    return result

def get_customer_id(email: str) -> Optional[int]:
    """Get customer_id from email"""
    sql = 'SELECT customer_id FROM "LENDYR-DEMO".CUSTOMERS WHERE email = ?'
    results = query_db(sql, (email,))
    if results:
        return results[0]['CUSTOMER_ID']
    return None

def clean(row: dict) -> dict:
    """Convert database row to clean dict with proper types"""
    result = {}
    for k, v in row.items():
        # Convert key to lowercase for consistency
        key = k.lower()
        if v is None or v == "" or v == "None":
            result[key] = None
        else:
            result[key] = v
    return result

# ─── Models ──────────────────────────────────────────────────────────────────

class CustomerAuthInput(BaseModel):
    customer_id: int
    pin: str

class CustomerAuthOutput(BaseModel):
    success: bool
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    message: str

class CardStatusUpdate(BaseModel):
    status: str

class CardLimitUpdate(BaseModel):
    daily_limit: float

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health", summary="Health check", tags=["System"])
def health():
    return {"status": "ok", "service": "Lendyr Bank API"}


@app.post("/auth/validate", tags=["Authentication"],
    summary="Authenticate customer",
    description="Validates customer ID and PIN, returns customer email for subsequent API calls")
def authenticate_customer(body: CustomerAuthInput):
    """
    Authenticate a customer using their ID and PIN.
    Returns customer email if successful for use in subsequent API calls.
    """
    try:
        sql = '''
        SELECT customer_id, first_name, last_name, email, pin
        FROM "LENDYR-DEMO".CUSTOMERS
        WHERE customer_id = ? AND pin = ?
        '''
        
        results = query_db(sql, (body.customer_id, body.pin))
        
        if results:
            # Authentication successful
            row = results[0]
            customer_name = f"{row['FIRST_NAME']} {row['LAST_NAME']}"
            customer_email = row['EMAIL']
            
            return CustomerAuthOutput(
                success=True,
                customer_email=customer_email,
                customer_name=customer_name,
                message=f"Welcome, {customer_name}! Authentication successful."
            )
        else:
            # Authentication failed
            return CustomerAuthOutput(
                success=False,
                message="Invalid customer ID or PIN. Please try again."
            )
            
    except Exception as e:
        return CustomerAuthOutput(
            success=False,
            message=f"Authentication error: {str(e)}"
        )


@app.get("/customers/{email}", tags=["Customers"],
    summary="Get customer profile",
    description="Returns full profile for a customer identified by their email address.")
def get_customer(email: str):
    sql = 'SELECT * FROM "LENDYR-DEMO".CUSTOMERS WHERE email = ?'
    results = query_db(sql, (email,))
    if results:
        return clean(results[0])
    raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/customers/{email}/accounts", tags=["Accounts"],
    summary="Get all accounts for a customer",
    description="Returns all checking, savings, credit, and loan accounts for the customer.")
def get_accounts(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sql = 'SELECT * FROM "LENDYR-DEMO".ACCOUNTS WHERE customer_id = ? ORDER BY account_type'
    results = query_db(sql, (cid,))
    
    if not results:
        raise HTTPException(status_code=404, detail="No accounts found")
    
    return [clean(r) for r in results]


@app.get("/customers/{email}/accounts/{account_type}", tags=["Accounts"],
    summary="Get a specific account type",
    description="Returns a single account of the given type (checking, savings, credit, loan).")
def get_account_by_type(email: str, account_type: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sql = 'SELECT * FROM "LENDYR-DEMO".ACCOUNTS WHERE customer_id = ? AND account_type = ?'
    results = query_db(sql, (cid, account_type))
    
    if results:
        return clean(results[0])
    raise HTTPException(status_code=404, detail=f"No {account_type} account found")


@app.get("/customers/{email}/transactions", tags=["Transactions"],
    summary="Get recent transactions",
    description="Returns the most recent transactions for the customer.")
def get_transactions(
    email: str,
    limit: int = Query(default=10, ge=1, le=100),
    account_type: Optional[str] = Query(default=None),
):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Build SQL query with JOIN
    if account_type:
        sql = '''
            SELECT t.*, a.account_type, a.account_number
            FROM "LENDYR-DEMO".TRANSACTIONS t
            JOIN "LENDYR-DEMO".ACCOUNTS a ON t.account_id = a.account_id
            WHERE a.customer_id = ? AND a.account_type = ?
            ORDER BY t.created_at DESC
            FETCH FIRST ? ROWS ONLY
        '''
        results = query_db(sql, (cid, account_type, limit))
    else:
        sql = '''
            SELECT t.*, a.account_type, a.account_number
            FROM "LENDYR-DEMO".TRANSACTIONS t
            JOIN "LENDYR-DEMO".ACCOUNTS a ON t.account_id = a.account_id
            WHERE a.customer_id = ?
            ORDER BY t.created_at DESC
            FETCH FIRST ? ROWS ONLY
        '''
        results = query_db(sql, (cid, limit))

    return [clean(r) for r in results]


@app.get("/customers/{email}/transfers", tags=["Transfers"],
    summary="Get transfer history",
    description="Returns all inbound and outbound transfers involving the customer.")
def get_transfers(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")

    sql = '''
        SELECT t.*, 
               a1.account_number as from_account,
               a2.account_number as to_account
        FROM "LENDYR-DEMO".TRANSFERS t
        LEFT JOIN "LENDYR-DEMO".ACCOUNTS a1 ON t.from_account_id = a1.account_id
        LEFT JOIN "LENDYR-DEMO".ACCOUNTS a2 ON t.to_account_id = a2.account_id
        WHERE a1.customer_id = ? OR a2.customer_id = ?
        ORDER BY t.initiated_at DESC
    '''
    results = query_db(sql, (cid, cid))
    
    return [clean(r) for r in results]


@app.get("/customers/{email}/cards", tags=["Cards"],
    summary="Get all cards",
    description="Returns all debit and credit cards for the customer.")
def get_cards(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sql = '''
        SELECT c.*, a.account_type
        FROM "LENDYR-DEMO".CARDS c
        JOIN "LENDYR-DEMO".ACCOUNTS a ON c.account_id = a.account_id
        WHERE c.customer_id = ?
        ORDER BY c.card_type
    '''
    results = query_db(sql, (cid,))
    
    if not results:
        raise HTTPException(status_code=404, detail="No cards found")
    
    return [clean(r) for r in results]


@app.patch("/cards/{card_id}/status", tags=["Cards"],
    summary="Freeze or unfreeze a card",
    description="Updates the status of a card. Use 'frozen' to freeze or 'active' to unfreeze.")
def update_card_status(card_id: int, body: CardStatusUpdate):
    if body.status not in ("active", "frozen", "blocked"):
        raise HTTPException(status_code=400, detail="Status must be 'active', 'frozen', or 'blocked'")
    
    # Check if card exists
    check_sql = 'SELECT card_id FROM "LENDYR-DEMO".CARDS WHERE card_id = ?'
    results = query_db(check_sql, (card_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Update card status
    update_sql = 'UPDATE "LENDYR-DEMO".CARDS SET status = ? WHERE card_id = ?'
    execute_update(update_sql, (body.status, card_id))
    
    return {"card_id": card_id, "status": body.status, "message": f"Card successfully set to {body.status}"}


@app.patch("/cards/{card_id}/limit", tags=["Cards"],
    summary="Update card daily limit",
    description="Updates the daily spending limit on a card.")
def update_card_limit(card_id: int, body: CardLimitUpdate):
    if body.daily_limit <= 0:
        raise HTTPException(status_code=400, detail="Daily limit must be greater than 0")
    
    # Check if card exists
    check_sql = 'SELECT card_id FROM "LENDYR-DEMO".CARDS WHERE card_id = ?'
    results = query_db(check_sql, (card_id,))
    
    if not results:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Update card limit
    update_sql = 'UPDATE "LENDYR-DEMO".CARDS SET daily_limit = ? WHERE card_id = ?'
    execute_update(update_sql, (body.daily_limit, card_id))
    
    return {"card_id": card_id, "daily_limit": body.daily_limit, "message": "Daily limit updated successfully"}


@app.get("/customers/{email}/loans", tags=["Loans"],
    summary="Get loan details",
    description="Returns loan details including outstanding balance and next payment date.")
def get_loans(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sql = '''
        SELECT l.*, a.interest_rate
        FROM "LENDYR-DEMO".LOANS l
        JOIN "LENDYR-DEMO".ACCOUNTS a ON l.account_id = a.account_id
        WHERE a.customer_id = ?
    '''
    results = query_db(sql, (cid,))
    
    if not results:
        raise HTTPException(status_code=404, detail="No loans found")
    
    return [clean(r) for r in results]


@app.get("/customers/{email}/disputes", tags=["Disputes"],
    summary="Get dispute history",
    description="Returns all transaction disputes filed by the customer.")
def get_disputes(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    sql = '''
        SELECT d.*, t.merchant_name, t.amount, t.created_at as transaction_date
        FROM "LENDYR-DEMO".DISPUTES d
        JOIN "LENDYR-DEMO".TRANSACTIONS t ON d.transaction_id = t.transaction_id
        WHERE d.customer_id = ?
        ORDER BY d.filed_at DESC
    '''
    results = query_db(sql, (cid,))
    
    return [clean(r) for r in results]

@app.get("/customers/{email}/payment-history", tags=["Loans"],
    summary="Get payment history",
    description="Returns payment history with statistics for credit evaluation.")
def get_payment_history(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get customer credit score
    customer_sql = 'SELECT credit_score FROM "LENDYR-DEMO".CUSTOMERS WHERE customer_id = ?'
    customer_results = query_db(customer_sql, (cid,))
    credit_score = customer_results[0]['CREDIT_SCORE'] if customer_results else None
    
    # Get payment history
    sql = '''
        SELECT payment_id, payment_date, payment_amount, was_late, days_late, auto_pay_used, note
        FROM "LENDYR-DEMO".PAYMENT_HISTORY
        WHERE customer_id = ?
        ORDER BY payment_date DESC
    '''
    results = query_db(sql, (cid,))
    
    # Calculate statistics
    total_payments = len(results)
    on_time_payments = sum(1 for r in results if r['WAS_LATE'] == 0)
    missed_payments = sum(1 for r in results if r['WAS_LATE'] == 1)
    on_time_percentage = (on_time_payments / total_payments * 100) if total_payments > 0 else 0
    
    return {
        "customer_id": cid,
        "credit_score": credit_score,
        "payment_history": [clean(r) for r in results],
        "statistics": {
            "total_payments": total_payments,
            "on_time_payments": on_time_payments,
            "missed_payments": missed_payments,
            "on_time_percentage": round(on_time_percentage, 2)
        }
    }


class LoanDeferralRequest(BaseModel):
    reason: str


@app.post("/customers/{email}/loans/{loan_id}/defer", tags=["Loans"],
    summary="Request loan payment deferral",
    description="Autonomous loan deferral approval based on credit score and payment history.")
def request_loan_deferral(email: str, loan_id: str, body: LoanDeferralRequest):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get customer credit score
    customer_sql = 'SELECT credit_score, first_name, last_name FROM "LENDYR-DEMO".CUSTOMERS WHERE customer_id = ?'
    customer_results = query_db(customer_sql, (cid,))
    if not customer_results:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    credit_score = customer_results[0]['CREDIT_SCORE']
    customer_name = f"{customer_results[0]['FIRST_NAME']} {customer_results[0]['LAST_NAME']}"
    
    # Get payment history statistics
    payment_sql = '''
        SELECT COUNT(*) as total_payments,
               SUM(CASE WHEN was_late = 0 THEN 1 ELSE 0 END) as on_time_payments,
               SUM(CASE WHEN was_late = 1 THEN 1 ELSE 0 END) as missed_payments
        FROM "LENDYR-DEMO".PAYMENT_HISTORY
        WHERE customer_id = ?
    '''
    payment_results = query_db(payment_sql, (cid,))
    
    total_payments = payment_results[0]['TOTAL_PAYMENTS'] if payment_results else 0
    on_time_payments = payment_results[0]['ON_TIME_PAYMENTS'] if payment_results else 0
    missed_payments = payment_results[0]['MISSED_PAYMENTS'] if payment_results else 0
    on_time_percentage = (on_time_payments / total_payments * 100) if total_payments > 0 else 0
    
    # Get loan details
    loan_sql = '''
        SELECT l.*, a.interest_rate
        FROM "LENDYR-DEMO".LOANS l
        JOIN "LENDYR-DEMO".ACCOUNTS a ON l.account_id = a.account_id
        WHERE l.loan_id = ? AND a.customer_id = ?
    '''
    loan_results = query_db(loan_sql, (loan_id, cid))
    
    if not loan_results:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    loan = clean(loan_results[0])
    
    # Autonomous decision logic
    # Approve if: credit_score >= 700 AND missed_payments == 0
    if credit_score >= 700 and missed_payments == 0:
        approval_status = "approved"
        approval_reason = f"Approved based on excellent credit score ({credit_score}) and perfect payment history ({on_time_payments}/{total_payments} on-time payments)"
    else:
        approval_status = "denied"
        reasons = []
        if credit_score < 700:
            reasons.append(f"credit score below threshold ({credit_score} < 700)")
        if missed_payments > 0:
            reasons.append(f"{missed_payments} missed payment(s)")
        approval_reason = f"Denied due to: {', '.join(reasons)}"
    
    # Calculate deferral impact (if approved)
    monthly_payment = float(loan['monthly_payment'])
    outstanding_balance = float(loan['outstanding_balance'])
    interest_rate = float(loan['interest_rate'])
    
    # Calculate one month's interest on the deferred payment
    monthly_interest_rate = interest_rate / 12 / 100
    interest_on_deferred_payment = monthly_payment * monthly_interest_rate
    new_balance = outstanding_balance + interest_on_deferred_payment
    
    # Extend payoff date by 1 month
    from datetime import datetime, timedelta, date
    next_payment_date = loan['next_payment_date']
    # Convert to datetime if it's a date object
    if isinstance(next_payment_date, date) and not isinstance(next_payment_date, datetime):
        next_payment_date = datetime.combine(next_payment_date, datetime.min.time())
    elif isinstance(next_payment_date, str):
        next_payment_date = datetime.strptime(next_payment_date, '%Y-%m-%d')
    new_payment_date = next_payment_date + timedelta(days=30)
    
    return {
        "loan_id": loan_id,
        "customer_name": customer_name,
        "approval_status": approval_status,
        "approval_reason": approval_reason,
        "deferral_details": {
            "reason": body.reason,
            "deferred_payment_amount": monthly_payment,
            "interest_accrued": round(interest_on_deferred_payment, 2),
            "new_outstanding_balance": round(new_balance, 2),
            "original_next_payment_date": loan['next_payment_date'],
            "new_next_payment_date": new_payment_date.strftime('%Y-%m-%d')
        },
        "credit_evaluation": {
            "credit_score": credit_score,
            "total_payments": total_payments,
            "on_time_payments": on_time_payments,
            "missed_payments": missed_payments,
            "on_time_percentage": round(on_time_percentage, 2)
        }
    }


# Made with Bob
