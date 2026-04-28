#!/usr/bin/env python3
"""
Generate monthly bank statements as markdown files for all Lendyr customers.
Outputs one file per customer per month into statements/<YYYY-MM>/.

Usage:
  python scripts/generate_statements.py
"""

import ibm_db
import os
from datetime import date, datetime
from pathlib import Path
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

# Statement periods in descending order (most recent first in output, but we
# compute balances forward from January so we process ascending internally).
PERIODS = [
    (2026, 1, "January 2026",  "January 1, 2026",   "January 31, 2026",  31),
    (2026, 2, "February 2026", "February 1, 2026",  "February 28, 2026", 28),
    (2026, 3, "March 2026",    "March 1, 2026",      "March 31, 2026",   31),
]

# Output order shown to the user (most recent first)
OUTPUT_ORDER = [2, 1, 0]

ACCOUNT_TYPE_LABELS = {
    "checking": "Checking Account",
    "savings":  "Savings Account",
    "credit":   "Credit Card",
    "loan":     "Loan Account",
}

# Plausible Dec-31-2025 opening balances by account type.
# These seed the forward computation so statements show realistic numbers.
JAN_OPENING = {
    "checking": 2_450.00,
    "savings":  4_800.00,
    "credit":     -285.00,   # small existing balance owed
    "loan":    None,          # replaced with outstanding_balance from loans table
}


def mask(account_number: str) -> str:
    n = str(account_number).strip()
    return f"{'•' * max(len(n) - 4, 4)}{n[-4:]}" if len(n) >= 4 else n


def fmt_usd(amount: float) -> str:
    return f"${abs(amount):,.2f}"


def fetch_all(conn, sql: str, params: tuple = None) -> list[dict]:
    if params:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt, params)
    else:
        stmt = ibm_db.exec_immediate(conn, sql)
    rows = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        rows.append({k.lower(): v for k, v in row.items()})
        row = ibm_db.fetch_assoc(stmt)
    return rows


def build_all_statements(conn, customer: dict) -> dict[tuple, str]:
    """
    Returns {(year, month): markdown_string} for all periods.
    Balances are computed forward from a synthetic Jan 1 opening.
    """
    cid = customer["customer_id"]
    name = f"{customer['first_name']} {customer['last_name']}"
    address_line = (customer.get("address") or "").strip()
    city  = (customer.get("city")  or "").strip()
    state = (customer.get("state") or "").strip()
    zip_  = (customer.get("zip")   or "").strip()
    city_state_zip = " ".join(filter(None, [city, state, zip_]))
    phone = (customer.get("phone") or "").strip()

    accounts = fetch_all(conn,
        'SELECT * FROM "LENDYR-DEMO".ACCOUNTS WHERE customer_id = ? ORDER BY account_type',
        (cid,))

    # Fetch outstanding loan balance per account (to seed loan opening balance)
    loan_balances: dict[int, float] = {}
    for acct in accounts:
        if acct["account_type"].lower().strip() == "loan":
            rows = fetch_all(conn,
                'SELECT outstanding_balance FROM "LENDYR-DEMO".LOANS WHERE account_id = ?',
                (acct["account_id"],))
            if rows:
                lb = rows[0].get("outstanding_balance")
                loan_balances[acct["account_id"]] = -abs(float(lb)) if lb else 0.0

    # Fetch ALL seeded transactions (Jan–Apr 2026) per account, sorted by date
    all_txns_by_acct: dict[int, list[dict]] = {}
    for acct in accounts:
        aid = acct["account_id"]
        txns = fetch_all(conn, """
            SELECT transaction_id, transaction_type, amount, merchant_name,
                   merchant_category, created_at
            FROM "LENDYR-DEMO".TRANSACTIONS
            WHERE account_id = ?
              AND created_at >= '2026-01-01'
              AND transaction_id >= 277
            ORDER BY created_at ASC
        """, (aid,))
        all_txns_by_acct[aid] = txns

    # Running balance per account — seeded with Jan 1 opening
    running: dict[int, float] = {}
    for acct in accounts:
        aid  = acct["account_id"]
        atype = acct["account_type"].lower().strip()
        if atype == "loan":
            running[aid] = loan_balances.get(aid, -15_000.0)
        else:
            running[aid] = JAN_OPENING.get(atype, 0.0)

    # Pre-compute per-period opening/closing balances by walking forward
    period_data: dict[tuple, dict] = {}   # (year, month) -> {acct_id: {opening, closing, txns}}

    for year, month, *_ in PERIODS:
        period_start_str = f"{year}-{month:02d}-01"
        period_end_str   = f"{year}-{month:02d}-{'31' if month in (1,3,5,7,8,10,12) else ('28' if month==2 else '30')}"

        acct_data: dict[int, dict] = {}
        for acct in accounts:
            aid = acct["account_id"]
            opening = running[aid]

            month_txns = [
                t for t in all_txns_by_acct[aid]
                if str(t.get("created_at", ""))[:7] == f"{year}-{month:02d}"
            ]

            bal = opening
            for t in month_txns:
                bal += float(t.get("amount") or 0)

            acct_data[aid] = {
                "opening": opening,
                "closing": bal,
                "txns": month_txns,
            }
            running[aid] = bal   # carry forward to next period

        period_data[(year, month)] = acct_data

    # Now render each period as a markdown string
    result: dict[tuple, str] = {}

    for year, month, period_label, start_label, end_label, last_day in PERIODS:
        acct_data = period_data[(year, month)]
        lines = []

        # Header
        lines += [
            "# Lendyr Bank",
            f"## Monthly Statement — {period_label}",
            "",
            "---",
            "",
            f"**Customer Name:** {name}  ",
            f"**Customer ID:** {cid}  ",
        ]
        if address_line:
            lines.append(f"**Address:** {address_line}  ")
        if city_state_zip:
            lines.append(f"**City, State ZIP:** {city_state_zip}  ")
        if phone:
            lines.append(f"**Phone:** {phone}  ")
        lines += [
            f"**Statement Period:** {start_label} – {end_label}  ",
            f"**Generated:** {datetime.now().strftime('%B %d, %Y')}  ",
            "",
            "---",
            "",
        ]

        for acct in accounts:
            aid    = acct["account_id"]
            atype  = acct["account_type"].lower().strip()
            label  = ACCOUNT_TYPE_LABELS.get(atype, atype.title())
            acct_num = mask(str(acct.get("account_number", aid)))
            data   = acct_data[aid]
            opening  = data["opening"]
            closing  = data["closing"]
            txns     = data["txns"]

            credits = sum(float(t["amount"]) for t in txns if float(t.get("amount", 0)) > 0)
            debits  = sum(float(t["amount"]) for t in txns if float(t.get("amount", 0)) < 0)
            net     = credits + debits

            lines += [
                f"## {label}",
                f"**Account Number:** {acct_num}  ",
                f"**Opening Balance:** ${opening:,.2f}  ",
                f"**Closing Balance:** ${closing:,.2f}  ",
                "",
            ]

            if not txns:
                lines += ["*No transactions this period.*", ""]
            else:
                lines.append("| Date | Description | Category | Debit | Credit | Balance |")
                lines.append("|------|-------------|----------|------:|-------:|--------:|")

                bal = opening
                for t in txns:
                    amt = float(t.get("amount") or 0)
                    bal += amt
                    ts  = str(t.get("created_at", ""))[:10]
                    try:
                        d_fmt = datetime.strptime(ts, "%Y-%m-%d").strftime("%b %d")
                    except ValueError:
                        d_fmt = ts

                    merchant = str(t.get("merchant_name", "")).replace("|", "\\|")
                    category = str(t.get("merchant_category", "Other")).replace("|", "\\|")

                    if amt < 0:
                        debit_col, credit_col = fmt_usd(amt), "—"
                    else:
                        debit_col, credit_col = "—", fmt_usd(amt)

                    lines.append(
                        f"| {d_fmt} | {merchant} | {category} | {debit_col} | {credit_col} | ${bal:,.2f} |"
                    )

                lines.append("")

            # Period summary
            lines += [
                "**Period Summary**",
                "",
                "| | Amount |",
                "|---|---:|",
                f"| Total Credits | ${credits:,.2f} |",
                f"| Total Debits  | ${abs(debits):,.2f} |",
                f"| Net Change    | ${net:+,.2f} |",
                "",
                "---",
                "",
            ]

        lines += [
            "*Thank you for banking with Lendyr Bank. For questions or concerns about your "
            "statement, please contact us at 1-800-LENDYR1 or support@lendyrbank.com.*",
            "",
            f"*Statement generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}.*",
        ]

        result[(year, month)] = "\n".join(lines)

    return result


def main():
    print("Connecting to DB2...")
    conn = ibm_db.connect(DSN, "", "")
    print("✅ Connected!\n")

    customers = fetch_all(conn, 'SELECT * FROM "LENDYR-DEMO".CUSTOMERS ORDER BY customer_id')
    print(f"Found {len(customers)} customers.\n")

    out_root = Path("statements")
    generated = []

    for c in customers:
        first = str(c.get("first_name", "")).strip().lower().replace(" ", "_")
        last  = str(c.get("last_name",  "")).strip().lower().replace(" ", "_")

        all_mds = build_all_statements(conn, c)

        # Write in descending order (March → January)
        for year, month, period_label, _, _, _ in reversed(PERIODS):
            folder = out_root / f"{year}-{month:02d}"
            folder.mkdir(parents=True, exist_ok=True)
            fpath  = folder / f"{first}_{last}.md"
            fpath.write_text(all_mds[(year, month)], encoding="utf-8")
            generated.append(str(fpath))
            print(f"  ✅ {fpath}")

    ibm_db.close(conn)

    print(f"\nGenerated {len(generated)} statement files in statements/")
    print("\nDirectory layout:")
    for p in sorted(generated):
        print(f"  {p}")


if __name__ == "__main__":
    main()
