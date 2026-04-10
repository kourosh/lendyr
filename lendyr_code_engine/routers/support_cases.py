"""
Support Cases skill router — exposes three actions consumed by watsonx Orchestrate:
  1. GET  /support-cases/customer/{customer_id}  — fetch all open cases for a customer
  2. POST /support-cases/{case_id}/escalate       — escalate a case to the next priority tier
  3. PATCH /support-cases/{case_id}               — update status and/or agent notes
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import ibm_db
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from db import get_connection, fetchall_as_dicts, fetchone_as_dict

router = APIRouter(prefix="/support-cases", tags=["Support Cases"])


# ---------------------------------------------------------------------------
# Enums & Schemas
# ---------------------------------------------------------------------------

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


ESCALATION_MAP = {
    Priority.low: Priority.medium,
    Priority.medium: Priority.high,
    Priority.high: Priority.critical,
    Priority.critical: Priority.critical,   # already at top
}


class SupportCase(BaseModel):
    case_id: str
    customer_id: str
    customer_name: str
    subject: str
    description: Optional[str]
    status: str
    priority: str
    created_at: Optional[str]
    updated_at: Optional[str]
    agent_notes: Optional[str]


class EscalateResponse(BaseModel):
    case_id: str
    previous_priority: str
    new_priority: str
    message: str


class UpdateCaseRequest(BaseModel):
    status: Optional[str] = Field(
        None,
        description="New status for the case, e.g. 'In Progress', 'Resolved', 'Closed'.",
    )
    agent_notes: Optional[str] = Field(
        None,
        description="Agent notes to append or replace on the case.",
    )


class UpdateCaseResponse(BaseModel):
    case_id: str
    updated_fields: list[str]
    message: str


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_case_or_404(conn, case_id: str) -> dict:
    sql = """
        SELECT sc.case_id, sc.customer_id, sc.subject, sc.description,
               sc.status, sc.priority, sc.created_at, sc.updated_at, sc.agent_notes,
               c.first_name || ' ' || c.last_name AS customer_name
        FROM support_cases sc
        JOIN customers c ON c.customer_id = sc.customer_id
        WHERE sc.case_id = ?
    """
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, case_id)
    ibm_db.execute(stmt)
    row = fetchone_as_dict(stmt)
    if not row:
        raise HTTPException(status_code=404, detail=f"Support case '{case_id}' not found.")
    return row


def _row_to_case(row: dict) -> SupportCase:
    return SupportCase(
        case_id=row["case_id"],
        customer_id=row["customer_id"],
        customer_name=row.get("customer_name", ""),
        subject=row["subject"],
        description=row.get("description"),
        status=row["status"],
        priority=row["priority"],
        created_at=str(row["created_at"]) if row.get("created_at") else None,
        updated_at=str(row["updated_at"]) if row.get("updated_at") else None,
        agent_notes=row.get("agent_notes"),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "/customer/{customer_id}",
    response_model=list[SupportCase],
    summary="Get support cases for a customer",
    description=(
        "Retrieve all open or in-progress support cases for the given customer ID. "
        "Returns full case details including priority, status, and agent notes."
    ),
)
def get_cases_for_customer(customer_id: str):
    conn = get_connection()
    try:
        sql = """
            SELECT sc.case_id, sc.customer_id, sc.subject, sc.description,
                   sc.status, sc.priority, sc.created_at, sc.updated_at, sc.agent_notes,
                   c.first_name || ' ' || c.last_name AS customer_name
            FROM support_cases sc
            JOIN customers c ON c.customer_id = sc.customer_id
            WHERE sc.customer_id = ?
              AND sc.status NOT IN ('Resolved', 'Closed')
            ORDER BY
                CASE sc.priority
                    WHEN 'Critical' THEN 1
                    WHEN 'High'     THEN 2
                    WHEN 'Medium'   THEN 3
                    ELSE 4
                END,
                sc.created_at DESC
        """
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, customer_id)
        ibm_db.execute(stmt)
        rows = fetchall_as_dicts(stmt)
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No open support cases found for customer '{customer_id}'.",
            )
        return [_row_to_case(r) for r in rows]
    finally:
        ibm_db.close(conn)


@router.post(
    "/{case_id}/escalate",
    response_model=EscalateResponse,
    summary="Escalate a support case",
    description=(
        "Escalate the priority of a support case by one tier "
        "(Low → Medium → High → Critical). "
        "If the case is already Critical, the priority stays unchanged and the response "
        "indicates no further escalation is possible."
    ),
)
def escalate_case(case_id: str):
    conn = get_connection()
    try:
        row = _get_case_or_404(conn, case_id)
        current_priority = row["priority"].strip()

        try:
            current_enum = Priority(current_priority)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Unrecognised priority value '{current_priority}' on case.",
            )

        new_enum = ESCALATION_MAP[current_enum]
        already_critical = current_enum == Priority.critical

        if not already_critical:
            now = datetime.now(timezone.utc)
            sql = """
                UPDATE support_cases
                SET priority = ?, updated_at = ?
                WHERE case_id = ?
            """
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, new_enum.value)
            ibm_db.bind_param(stmt, 2, now)
            ibm_db.bind_param(stmt, 3, case_id)
            ibm_db.execute(stmt)

        return EscalateResponse(
            case_id=case_id,
            previous_priority=current_enum.value,
            new_priority=new_enum.value,
            message=(
                f"Case escalated from {current_enum.value} to {new_enum.value}."
                if not already_critical
                else "Case is already at Critical priority — no further escalation possible."
            ),
        )
    finally:
        ibm_db.close(conn)


@router.patch(
    "/{case_id}",
    response_model=UpdateCaseResponse,
    summary="Update a support case",
    description=(
        "Update the status and/or agent notes on a support case. "
        "At least one of 'status' or 'agent_notes' must be provided. "
        "Valid status values: 'Open', 'In Progress', 'Pending Customer', 'Resolved', 'Closed'."
    ),
)
def update_case(case_id: str, body: UpdateCaseRequest):
    if not body.status and not body.agent_notes:
        raise HTTPException(
            status_code=422,
            detail="Provide at least one of 'status' or 'agent_notes' to update.",
        )

    conn = get_connection()
    try:
        _get_case_or_404(conn, case_id)   # confirm exists

        set_clauses = []
        params = []
        updated_fields = []

        if body.status:
            set_clauses.append("status = ?")
            params.append(body.status)
            updated_fields.append("status")

        if body.agent_notes:
            set_clauses.append("agent_notes = ?")
            params.append(body.agent_notes)
            updated_fields.append("agent_notes")

        now = datetime.now(timezone.utc)
        set_clauses.append("updated_at = ?")
        params.append(now)
        params.append(case_id)

        sql = f"UPDATE support_cases SET {', '.join(set_clauses)} WHERE case_id = ?"
        stmt = ibm_db.prepare(conn, sql)
        for i, p in enumerate(params, start=1):
            ibm_db.bind_param(stmt, i, p)
        ibm_db.execute(stmt)

        return UpdateCaseResponse(
            case_id=case_id,
            updated_fields=updated_fields,
            message=f"Case {case_id} updated successfully: {', '.join(updated_fields)}.",
        )
    finally:
        ibm_db.close(conn)
