import ibm_db
import json
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_credentials() -> dict:
    """Load DB2 credentials from the mounted secrets file."""
    creds_path = os.environ.get("DB2_CREDS_PATH", "/secrets/db2_creds.json")
    with open(creds_path) as f:
        raw = json.load(f)
    db2 = raw[0]["credentials"]["connection"]["db2"]
    host = db2["hosts"][0]["hostname"]
    port = db2["hosts"][0]["port"]
    database = db2["database"]
    username = db2["authentication"]["username"]
    password = db2["authentication"]["password"]
    cert = db2.get("certificate", {}).get("certificate_base64", "")
    return {
        "host": host,
        "port": port,
        "database": database,
        "username": username,
        "password": password,
        "cert": cert,
    }


def get_connection() -> ibm_db.IBM_DBConnection:
    """Open and return a new DB2 connection."""
    c = _load_credentials()
    dsn = (
        f"DATABASE={c['database']};"
        f"HOSTNAME={c['host']};"
        f"PORT={c['port']};"
        f"PROTOCOL=TCPIP;"
        f"UID={c['username']};"
        f"PWD={c['password']};"
        f"Security=SSL;"
    )
    return ibm_db.connect(dsn, "", "")


def fetchall_as_dicts(stmt) -> list[dict]:
    """Return all rows from an ibm_db statement as a list of dicts."""
    rows = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        rows.append({k.lower(): v for k, v in row.items()})
        row = ibm_db.fetch_assoc(stmt)
    return rows


def fetchone_as_dict(stmt) -> dict | None:
    """Return a single row as a dict, or None."""
    row = ibm_db.fetch_assoc(stmt)
    if not row:
        return None
    return {k.lower(): v for k, v in row.items()}
