#!/usr/bin/env python3
"""
Create the credit_score_history table and seed it with 6 months of history.

Each customer's most recent month matches their current credit_score.
Scores walk backward one month at a time, drifting ±3–5 points per step.

Usage:
  python scripts/seed_credit_score_history.py           # dry run
  python scripts/seed_credit_score_history.py --execute # write to DB2
"""

import argparse
import ibm_db
import os
import random
from datetime import date
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

SCHEMA = '"LENDYR-DEMO"'
HISTORY_MONTHS = 6  # current month + 5 prior months

CREATE_TABLE_SQL = f"""
CREATE TABLE {SCHEMA}.credit_score_history (
    history_id    INTEGER      NOT NULL PRIMARY KEY,
    customer_id   INTEGER      NOT NULL,
    score_date    DATE         NOT NULL,
    credit_score  INTEGER      NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES {SCHEMA}.customers(customer_id)
)
"""


def month_date(year: int, month: int) -> date:
    """First day of the given month."""
    return date(year, month, 1)


def prev_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def build_history(current_score: int, current_year: int, current_month: int) -> list[tuple[date, int]]:
    """
    Returns [(score_date, credit_score), ...] from most recent to oldest,
    covering HISTORY_MONTHS months.
    """
    entries = []
    score = current_score
    year, month = current_year, current_month

    for _ in range(HISTORY_MONTHS):
        entries.append((month_date(year, month), score))
        drift = random.randint(3, 5) * random.choice([-1, 1])
        score = max(300, min(850, score - drift))  # walk backward = undo the drift
        year, month = prev_month(year, month)

    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true",
                        help="Write to DB2 (default: dry run)")
    args = parser.parse_args()

    print("Connecting to DB2...")
    conn = ibm_db.connect(DSN, "", "")
    print("Connected!\n")

    # Fetch current credit scores
    sql = f"""
        SELECT customer_id, first_name, last_name, credit_score
        FROM {SCHEMA}.customers
        ORDER BY customer_id
    """
    stmt = ibm_db.exec_immediate(conn, sql)
    customers = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        customers.append({
            "customer_id": int(row["CUSTOMER_ID"]),
            "name": f"{row['FIRST_NAME']} {row['LAST_NAME']}",
            "credit_score": int(row["CREDIT_SCORE"]),
        })
        row = ibm_db.fetch_assoc(stmt)

    print(f"Found {len(customers)} customers with credit scores:")
    for c in customers:
        print(f"  {c['customer_id']:2d}: {c['name']:22s}  current score: {c['credit_score']}")
    print()

    # Build history rows — seed for reproducibility
    random.seed(99)
    today = date.today()
    all_rows: list[tuple] = []  # (history_id, customer_id, score_date, credit_score)

    next_id = 1
    for c in customers:
        entries = build_history(c["credit_score"], today.year, today.month)
        for score_date, score in entries:
            all_rows.append((next_id, c["customer_id"], score_date.isoformat(), score))
            next_id += 1

    # Print preview
    print(f"Generated {len(all_rows)} rows ({HISTORY_MONTHS} months × {len(customers)} customers)\n")
    print(f"  {'ID':>4}  {'cust':>4}  {'date':12}  {'score':>5}")
    print("  " + "-" * 35)
    for row in all_rows[:18]:
        hid, cid, dt, score = row
        print(f"  {hid:>4}  {cid:>4}  {dt:12}  {score:>5}")
    if len(all_rows) > 18:
        print(f"  ... ({len(all_rows) - 18} more rows)")
    print()

    if not args.execute:
        print("── DRY RUN ── Pass --execute to write to DB2.\n")
        ibm_db.close(conn)
        return

    # Create table
    print(f"Creating {SCHEMA}.credit_score_history ...")
    try:
        ibm_db.exec_immediate(conn, CREATE_TABLE_SQL)
        print("  Table created.\n")
    except Exception as e:
        msg = str(e)
        if "-601" in msg or "already exists" in msg.lower():
            print("  Table already exists — skipping CREATE.\n")
        else:
            print(f"  Error creating table: {e}")
            ibm_db.close(conn)
            return

    # Insert rows
    insert_sql = f"""
        INSERT INTO {SCHEMA}.credit_score_history
        (history_id, customer_id, score_date, credit_score)
        VALUES (?, ?, ?, ?)
    """
    prepared = ibm_db.prepare(conn, insert_sql)
    if not prepared:
        print(f"Failed to prepare INSERT: {ibm_db.stmt_errormsg()}")
        ibm_db.close(conn)
        return

    print(f"Inserting {len(all_rows)} rows...")
    success = errors = 0
    for row in all_rows:
        try:
            ibm_db.execute(prepared, row)
            success += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  Error on row {row}: {e}")

    print(f"\nDone!  Success: {success}  Errors: {errors}")
    ibm_db.close(conn)


if __name__ == "__main__":
    main()
