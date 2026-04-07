"""
Lendyr Bank Demo API
FastAPI + CSV files — deployed on IBM Code Engine
No database drivers, no connection strings.
"""

import csv
import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# ─── Data Layer ───────────────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load(table: str) -> list[dict]:
    """Load a CSV file and return list of dicts."""
    path = os.path.join(DATA_DIR, f"{table}.csv")
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

# Load all tables into memory at startup
DB = {
    "customers":     load("customers"),
    "accounts":      load("accounts"),
    "cards":         load("cards"),
    "transactions":  load("transactions"),
    "transfers":     load("transfers"),
    "loans":         load("loans"),
    "disputes":      load("disputes"),
    "support_cases": load("support_cases"),
}

def get_customer_id(email: str) -> Optional[str]:
    for row in DB["customers"]:
        if row["email"] == email:
            return row["customer_id"]
    return None

def clean(row: dict) -> dict:
    """Convert empty strings to None and numeric strings to numbers."""
    result = {}
    for k, v in row.items():
        if v == "" or v == "None":
            result[k] = None
        else:
            try:
                result[k] = int(v)
            except (ValueError, TypeError):
                try:
                    result[k] = float(v)
                except (ValueError, TypeError):
                    result[k] = v
    return result

# ─── Models ──────────────────────────────────────────────────────────────────

class CardStatusUpdate(BaseModel):
    status: str

class CardLimitUpdate(BaseModel):
    daily_limit: float

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health", summary="Health check", tags=["System"])
def health():
    return {"status": "ok", "service": "Lendyr Bank API"}


@app.get("/customers/{email}", tags=["Customers"],
    summary="Get customer profile",
    description="Returns full profile for a customer identified by their email address.")
def get_customer(email: str):
    for row in DB["customers"]:
        if row["email"] == email:
            return clean(row)
    raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/customers/{email}/accounts", tags=["Accounts"],
    summary="Get all accounts for a customer",
    description="Returns all checking, savings, credit, and loan accounts for the customer.")
def get_accounts(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    rows = [clean(r) for r in DB["accounts"] if r["customer_id"] == cid]
    if not rows:
        raise HTTPException(status_code=404, detail="No accounts found")
    return sorted(rows, key=lambda r: r["account_type"])


@app.get("/customers/{email}/accounts/{account_type}", tags=["Accounts"],
    summary="Get a specific account type",
    description="Returns a single account of the given type (checking, savings, credit, loan).")
def get_account_by_type(email: str, account_type: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    for row in DB["accounts"]:
        if row["customer_id"] == cid and row["account_type"] == account_type:
            return clean(row)
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

    # Get account IDs for this customer
    account_ids = {r["account_id"] for r in DB["accounts"] if r["customer_id"] == cid}
    if account_type:
        account_ids = {
            r["account_id"] for r in DB["accounts"]
            if r["customer_id"] == cid and r["account_type"] == account_type
        }

    # Build account_type lookup
    acct_lookup = {r["account_id"]: r for r in DB["accounts"]}

    rows = []
    for t in DB["transactions"]:
        if t["account_id"] in account_ids:
            row = clean(t)
            acct = acct_lookup.get(t["account_id"], {})
            row["account_type"] = acct.get("account_type")
            row["account_number"] = acct.get("account_number")
            rows.append(row)

    rows.sort(key=lambda r: r.get("created_at") or "", reverse=True)
    return rows[:limit]


@app.get("/customers/{email}/transfers", tags=["Transfers"],
    summary="Get transfer history",
    description="Returns all inbound and outbound transfers involving the customer.")
def get_transfers(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")

    account_ids = {r["account_id"] for r in DB["accounts"] if r["customer_id"] == cid}
    acct_lookup = {r["account_id"]: r["account_number"] for r in DB["accounts"]}

    rows = []
    for t in DB["transfers"]:
        if t["from_account_id"] in account_ids or t["to_account_id"] in account_ids:
            row = clean(t)
            row["from_account"] = acct_lookup.get(t["from_account_id"])
            row["to_account"] = acct_lookup.get(t["to_account_id"])
            rows.append(row)

    rows.sort(key=lambda r: r.get("initiated_at") or "", reverse=True)
    return rows


@app.get("/customers/{email}/cards", tags=["Cards"],
    summary="Get all cards",
    description="Returns all debit and credit cards for the customer.")
def get_cards(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    acct_lookup = {r["account_id"]: r["account_type"] for r in DB["accounts"]}
    rows = []
    for c in DB["cards"]:
        if c["customer_id"] == cid:
            row = clean(c)
            row["account_type"] = acct_lookup.get(c["account_id"])
            rows.append(row)
    if not rows:
        raise HTTPException(status_code=404, detail="No cards found")
    return sorted(rows, key=lambda r: r["card_type"])


@app.patch("/cards/{card_id}/status", tags=["Cards"],
    summary="Freeze or unfreeze a card",
    description="Updates the status of a card. Use 'frozen' to freeze or 'active' to unfreeze.")
def update_card_status(card_id: int, body: CardStatusUpdate):
    if body.status not in ("active", "frozen", "blocked"):
        raise HTTPException(status_code=400, detail="Status must be 'active', 'frozen', or 'blocked'")
    for row in DB["cards"]:
        if row["card_id"] == str(card_id):
            row["status"] = body.status
            return {"card_id": card_id, "status": body.status, "message": f"Card successfully set to {body.status}"}
    raise HTTPException(status_code=404, detail="Card not found")


@app.patch("/cards/{card_id}/limit", tags=["Cards"],
    summary="Update card daily limit",
    description="Updates the daily spending limit on a card.")
def update_card_limit(card_id: int, body: CardLimitUpdate):
    if body.daily_limit <= 0:
        raise HTTPException(status_code=400, detail="Daily limit must be greater than 0")
    for row in DB["cards"]:
        if row["card_id"] == str(card_id):
            row["daily_limit"] = str(body.daily_limit)
            return {"card_id": card_id, "daily_limit": body.daily_limit, "message": "Daily limit updated successfully"}
    raise HTTPException(status_code=404, detail="Card not found")


@app.get("/customers/{email}/loans", tags=["Loans"],
    summary="Get loan details",
    description="Returns loan details including outstanding balance and next payment date.")
def get_loans(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    account_ids = {r["account_id"] for r in DB["accounts"] if r["customer_id"] == cid}
    acct_lookup = {r["account_id"]: r for r in DB["accounts"]}
    rows = []
    for l in DB["loans"]:
        if l["account_id"] in account_ids:
            row = clean(l)
            row["interest_rate"] = clean(acct_lookup.get(l["account_id"], {})).get("interest_rate")
            rows.append(row)
    if not rows:
        raise HTTPException(status_code=404, detail="No loans found")
    return rows


@app.get("/customers/{email}/disputes", tags=["Disputes"],
    summary="Get dispute history",
    description="Returns all transaction disputes filed by the customer.")
def get_disputes(email: str):
    cid = get_customer_id(email)
    if not cid:
        raise HTTPException(status_code=404, detail="Customer not found")
    txn_lookup = {r["transaction_id"]: r for r in DB["transactions"]}
    rows = []
    for d in DB["disputes"]:
        if d["customer_id"] == cid:
            row = clean(d)
            txn = txn_lookup.get(d["transaction_id"], {})
            row["merchant_name"] = txn.get("merchant_name")
            row["amount"] = txn.get("amount")
            row["transaction_date"] = txn.get("created_at")
            rows.append(row)
    rows.sort(key=lambda r: r.get("filed_at") or "", reverse=True)
    return rows
