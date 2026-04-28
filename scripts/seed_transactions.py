#!/usr/bin/env python3
"""
Seed ~50 transactions per customer per month for Jan-Apr 2026.

Usage:
  python scripts/seed_transactions.py           # dry run (no DB writes)
  python scripts/seed_transactions.py --execute # write to DB2
"""

import argparse
import ibm_db
import os
import random
from collections import defaultdict
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv("lendyr_code_engine/.env")

DSN = (
    f"DRIVER={os.getenv('DRIVER')};"
    f"DATABASE={os.getenv('DATABASE')};"
    f"HOSTNAME={os.getenv('DSN_HOSTNAME')};"
    f"PORT={os.getenv('DSN_PORT')};"
    f"PROTOCOL={os.getenv('PROTOCOL')};"
    f"UID={os.getenv('USERNAME')};"
    f"PWD={os.getenv('PASSWORD')};"
    f"SECURITY={os.getenv('SECURITY')};"
)

MONTHS = [(2026, 1), (2026, 2), (2026, 3), (2026, 4)]

# ── Merchant pools ────────────────────────────────────────────────────────────

MERCHANTS = {
    "Groceries": [
        "Kroger", "Trader Joe's", "Whole Foods Market", "Safeway",
        "Costco Wholesale", "Aldi", "Publix", "H-E-B",
    ],
    "Dining": [
        "Chipotle", "Starbucks", "McDonald's", "Panera Bread",
        "Olive Garden", "Chili's", "Domino's Pizza", "Subway",
        "IHOP", "Applebee's", "Local Diner", "Panda Express",
    ],
    "Gas & Fuel": [
        "Shell", "Chevron", "BP", "Exxon", "Sunoco", "Marathon",
    ],
    "Shopping": [
        "Target", "Amazon", "Walmart", "Home Depot", "TJ Maxx",
        "Best Buy", "Kohl's", "Macy's", "Ross", "Marshalls",
        "Bed Bath & Beyond", "Lowe's",
    ],
    "Transport": [
        "Uber", "Lyft", "City Parking Garage", "Metro Transit",
        "Bus Pass", "Parking Meter",
    ],
    "Healthcare": [
        "CVS Pharmacy", "Walgreens", "Rite Aid",
        "Doctor Copay", "Urgent Care Visit", "Dentist Office",
    ],
    "Travel": [
        "Delta Airlines", "Southwest Airlines", "Marriott Hotels",
        "Airbnb", "Enterprise Rent-A-Car", "Hilton Hotels",
    ],
    "Other": [
        "Netflix", "Spotify", "Apple.com", "Google Play Store",
        "Planet Fitness", "Amazon Prime", "Hulu", "Disney+",
        "Verizon Wireless", "AT&T",
    ],
}

# Amount ranges (lo, hi) per category — middle-class realistic
AMOUNT_RANGES = {
    "Groceries":  (32.0,  148.0),
    "Dining":     (8.50,   68.0),
    "Gas & Fuel": (28.0,   72.0),
    "Shopping":   (12.0,  185.0),
    "Transport":  (7.0,    42.0),
    "Healthcare": (20.0,  145.0),
    "Travel":     (85.0,  380.0),
    "Other":      (9.0,    62.0),
}


def rand_amount(category: str) -> float:
    lo, hi = AMOUNT_RANGES[category]
    return round(random.uniform(lo, hi), 2)


def rand_merchant(category: str) -> str:
    return random.choice(MERCHANTS[category])


def rand_date(year: int, month: int) -> date:
    """Random date within the month, weekdays weighted 2x vs weekends."""
    if month == 12:
        last = 31
    else:
        last = (date(year, month + 1, 1) - timedelta(days=1)).day
    pool = []
    for d in range(1, last + 1):
        w = 1 if date(year, month, d).weekday() >= 5 else 2
        pool.extend([d] * w)
    return date(year, month, random.choice(pool))


def rand_time() -> str:
    return f"{random.randint(7, 21):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"


def make_ts(d: date) -> str:
    return f"{d.isoformat()} {rand_time()}"


# ── Transaction builder ───────────────────────────────────────────────────────

def build_month(year: int, month: int, accounts: dict, loan_amount: float | None) -> list[tuple]:
    """
    Returns list of (account_id, txn_type, amount, merchant, category, created_at, status)
    tuples for one customer for one month. transaction_id is assigned later.
    """
    rows = []
    checking = accounts.get("checking")
    savings   = accounts.get("savings")
    credit    = accounts.get("credit")
    loan      = accounts.get("loan")

    # ── Checking: direct deposits (bi-weekly payroll) ─────────────────────
    if checking:
        base_pay = round(random.uniform(1800, 2800), 2)
        for day in (random.randint(1, 5), random.randint(14, 19)):
            d = date(year, month, day)
            rows.append((checking, "transfer_in", base_pay,
                         "Employer Direct Deposit", "Other", make_ts(d), "completed"))

        # Check deposits (1–2)
        for _ in range(random.randint(1, 2)):
            amt = round(random.uniform(50, 480), 2)
            rows.append((checking, "transfer_in", amt,
                         "Check Deposit", "Other", make_ts(rand_date(year, month)), "completed"))

        # Everyday checking debits
        checking_spend = [
            ("Groceries",  6),
            ("Dining",     5),
            ("Gas & Fuel", 3),
            ("Shopping",   3),
            ("Transport",  2),
            ("Healthcare", 1),
        ]
        for cat, n in checking_spend:
            for _ in range(n):
                m = rand_merchant(cat)
                amt = rand_amount(cat)
                rows.append((checking, "debit", -amt, m, cat,
                             make_ts(rand_date(year, month)), "completed"))

        # Transfer to savings
        if savings:
            xfer = round(random.uniform(100, 400), 2)
            xfer_d = rand_date(year, month)
            rows.append((checking, "transfer_out", -xfer,
                         "Internal Transfer", "Other", make_ts(xfer_d), "completed"))
            rows.append((savings, "transfer_in", xfer,
                         "Internal Transfer", "Other", make_ts(xfer_d), "completed"))

        # Loan payment from checking
        if loan and loan_amount:
            pay_d = date(year, month, random.randint(10, 18))
            rows.append((checking, "debit", -round(loan_amount, 2),
                         "Loan Payment", "Other", make_ts(pay_d), "completed"))
            rows.append((loan, "payment", round(loan_amount, 2),
                         "Loan Payment", "Other", make_ts(pay_d), "completed"))

        # Credit card payment from checking
        if credit:
            cc_pmt = round(random.uniform(150, 580), 2)
            cc_d = date(year, month, random.randint(15, 27))
            rows.append((checking, "debit", -cc_pmt,
                         "Credit Card Payment", "Other", make_ts(cc_d), "completed"))
            rows.append((credit, "payment", cc_pmt,
                         "Credit Card Payment", "Other", make_ts(cc_d), "completed"))

    # ── Extra checking debits for customers without a credit card ─────────
    # Debit-card-only customers use checking for more everyday purchases
    if checking and not credit:
        extra_spend = [
            ("Shopping",  5),
            ("Dining",    4),
            ("Other",     4),
            ("Groceries", 3),
            ("Transport", 2),
            ("Shopping",  2),
        ]
        for cat, n in extra_spend:
            for _ in range(n):
                m = rand_merchant(cat)
                amt = rand_amount(cat)
                rows.append((checking, "debit", -amt, m, cat,
                             make_ts(rand_date(year, month)), "completed"))

    # ── Credit card charges ───────────────────────────────────────────────
    if credit:
        credit_spend = [
            ("Shopping",  5),
            ("Dining",    4),
            ("Groceries", 2),
            ("Other",     3),
            ("Transport", 1),
        ]
        if random.random() < 0.35:
            credit_spend.append(("Travel", 1))
        for cat, n in credit_spend:
            for _ in range(n):
                m = rand_merchant(cat)
                amt = rand_amount(cat)
                rows.append((credit, "debit", -amt, m, cat,
                             make_ts(rand_date(year, month)), "completed"))

    return rows


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true",
                        help="Write to DB2 (default: dry run)")
    args = parser.parse_args()

    print("Connecting to DB2...")
    conn = ibm_db.connect(DSN, "", "")
    print("✅ Connected!\n")

    # Fetch accounts per customer
    print("Fetching customers and accounts...")
    sql = """
        SELECT c.customer_id, c.first_name, c.last_name,
               a.account_id, a.account_type
        FROM "LENDYR-DEMO".customers c
        JOIN "LENDYR-DEMO".accounts a ON c.customer_id = a.customer_id
        ORDER BY c.customer_id, a.account_type
    """
    stmt = ibm_db.exec_immediate(conn, sql)
    raw: dict = {}
    row = ibm_db.fetch_tuple(stmt)
    while row:
        cid, fname, lname, acct_id, acct_type = row
        if cid not in raw:
            raw[cid] = {"cid": cid, "name": f"{fname} {lname}", "accounts": {}}
        raw[cid]["accounts"][acct_type.lower().strip()] = acct_id
        row = ibm_db.fetch_tuple(stmt)

    # Fetch loan monthly payment amounts
    loan_sql = """
        SELECT a.customer_id, l.monthly_payment
        FROM "LENDYR-DEMO".accounts a
        JOIN "LENDYR-DEMO".loans l ON a.account_id = l.account_id
    """
    stmt = ibm_db.exec_immediate(conn, loan_sql)
    row = ibm_db.fetch_tuple(stmt)
    while row:
        cid, monthly = row
        if cid in raw:
            raw[cid]["loan_amount"] = float(monthly)
        row = ibm_db.fetch_tuple(stmt)

    customers = list(raw.values())
    print(f"Found {len(customers)} customers:\n")
    for c in customers:
        acct_summary = ", ".join(
            f"{t}(#{aid})" for t, aid in sorted(c["accounts"].items())
        )
        loan_note = f"  — loan pmt ${c['loan_amount']:.2f}/mo" if "loan_amount" in c else ""
        print(f"  {c['cid']}: {c['name']:20s}  [{acct_summary}]{loan_note}")
    print()

    # Find next available transaction_id
    stmt = ibm_db.exec_immediate(conn, 'SELECT MAX(transaction_id) FROM "LENDYR-DEMO".TRANSACTIONS')
    row = ibm_db.fetch_tuple(stmt)
    next_id = (int(row[0]) if row and row[0] else 0) + 1
    print(f"Max existing transaction_id: {next_id - 1}. New IDs start at: {next_id}\n")

    # Build all transactions
    random.seed(42)
    all_rows: list[tuple] = []
    counts: dict = defaultdict(int)

    tid = next_id
    for c in customers:
        for year, month in MONTHS:
            month_rows = build_month(year, month, c["accounts"], c.get("loan_amount"))
            all_rows.extend(month_rows)
            counts[c["name"]] += len(month_rows)

    # Assign sequential transaction_ids
    all_rows = [(tid + i, *row) for i, row in enumerate(all_rows)]

    print(f"Generated {len(all_rows)} total transactions across {len(MONTHS)} months\n")
    print("Breakdown by customer:")
    for name, n in sorted(counts.items()):
        per_month = n // len(MONTHS)
        print(f"  {name:22s}: {n:4d} total  (~{per_month}/month)")
    print()

    if not args.execute:
        print("── DRY RUN ── Pass --execute to write to DB2.\n")
        print("Sample (first 12 rows):")
        print(f"  {'txn_id':>8}  {'acct_id':>8}  {'type':14}  {'amount':>10}  {'merchant':<30}  {'category':<12}  date")
        print("  " + "-" * 105)
        for r in all_rows[:12]:
            txn_id, acct_id, txn_type, amount, merchant, category, ts, status = r
            print(f"  {txn_id:>8}  {acct_id:>8}  {txn_type:14}  {amount:>10.2f}  {merchant:<30}  {category:<12}  {ts[:10]}")
        ibm_db.close(conn)
        return

    # Insert
    insert_sql = """
        INSERT INTO "LENDYR-DEMO".TRANSACTIONS
        (transaction_id, account_id, transaction_type, amount, merchant_name, merchant_category, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    prepared = ibm_db.prepare(conn, insert_sql)
    if not prepared:
        print(f"❌ Failed to prepare INSERT: {ibm_db.stmt_errormsg()}")
        ibm_db.close(conn)
        return

    print(f"Inserting {len(all_rows)} transactions into DB2...")
    success = 0
    errors = 0
    for i, row in enumerate(all_rows, 1):
        try:
            ibm_db.execute(prepared, row)
            success += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  ❌ Error on row {i}: {e}")
        if i % 200 == 0:
            print(f"  Inserted {i}/{len(all_rows)}...")

    print(f"\n✅ Done!  Success: {success}  Errors: {errors}")
    ibm_db.close(conn)


if __name__ == "__main__":
    main()
