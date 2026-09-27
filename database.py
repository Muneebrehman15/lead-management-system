"""SQLite data layer for the Prime Properties Karachi lead manager."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "leads.db"

STATUSES = [
    "New",
    "Contacted",
    "Site Visit",
    "Negotiation",
    "Converted",
    "Lost",
]
SOURCES = [
    "Website",
    "Walk-in",
    "Referral",
    "Facebook",
    "Instagram",
    "WhatsApp",
    "Zameen.com",
]
LOCATIONS = [
    "DHA",
    "Clifton",
    "Bahria Town",
    "Gulshan-e-Iqbal",
    "PECHS",
    "North Nazimabad",
    "Gulistan-e-Johar",
    "Korangi",
    "Scheme 33",
    "Saddar",
]
PROPERTY_TYPES = ["Apartment", "House", "Plot", "Commercial", "Villa"]

CREATE_LEADS_TABLE = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    property TEXT,
    budget REAL,
    location TEXT,
    status TEXT,
    source TEXT,
    created_at TEXT,
    last_contact TEXT,
    next_followup TEXT,
    notes TEXT
);
"""


def get_connection() -> sqlite3.Connection:
    """Return a connection to the local SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Create the database, leads table, and sample data if needed."""
    with get_connection() as connection:
        connection.execute(CREATE_LEADS_TABLE)
        connection.commit()
    seed_sample_leads_if_empty()


def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row is not None else None


def fetch_leads() -> list[dict]:
    """Return all leads, newest first."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM leads ORDER BY datetime(created_at) DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_lead(lead_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM leads WHERE id = ?", (lead_id,)
        ).fetchone()
    return _row_to_dict(row)


def add_lead(
    name: str,
    phone: str = "",
    email: str = "",
    property: str = "",
    budget: float | None = None,
    location: str = "",
    status: str = "New",
    source: str = "",
    last_contact: str = "",
    next_followup: str = "",
    notes: str = "",
    created_at: str | None = None,
) -> int:
    """Insert a lead and return its id."""
    created = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO leads (
                name, phone, email, property, budget, location, status,
                source, created_at, last_contact, next_followup, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                phone.strip(),
                email.strip(),
                property.strip(),
                budget,
                location.strip(),
                status,
                source.strip(),
                created,
                last_contact or None,
                next_followup or None,
                notes.strip(),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def update_lead(
    lead_id: int,
    name: str,
    phone: str,
    email: str,
    property: str,
    budget: float | None,
    location: str,
    status: str,
    source: str,
    last_contact: str,
    next_followup: str,
    notes: str,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE leads SET
                name = ?, phone = ?, email = ?, property = ?, budget = ?,
                location = ?, status = ?, source = ?, last_contact = ?,
                next_followup = ?, notes = ?
            WHERE id = ?
            """,
            (
                name.strip(),
                phone.strip(),
                email.strip(),
                property.strip(),
                budget,
                location.strip(),
                status,
                source.strip(),
                last_contact or None,
                next_followup or None,
                notes.strip(),
                lead_id,
            ),
        )
        connection.commit()


def delete_lead(lead_id: int) -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
        connection.commit()


def fetch_followups(*, overdue_only: bool = False) -> list[dict]:
    """Return open leads that have a follow-up date set."""
    query = """
        SELECT * FROM leads
        WHERE next_followup IS NOT NULL
          AND TRIM(next_followup) != ''
          AND status NOT IN ('Converted', 'Lost')
    """
    if overdue_only:
        query += " AND date(next_followup) <= date('now', 'localtime')"
    query += " ORDER BY date(next_followup) ASC, id ASC"

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()
    return [dict(row) for row in rows]


def seed_sample_leads_if_empty() -> None:
    """Add fictional Karachi leads so the first dashboard is not blank."""
    with get_connection() as connection:
        count = connection.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    if count:
        return

    today = datetime.now().date()
    samples = [
        {
            "name": "Ayesha Khan",
            "phone": "0300-1112233",
            "email": "ayesha.khan@email.com",
            "property": "Apartment",
            "budget": 18_500_000,
            "location": "Clifton",
            "status": "Negotiation",
            "source": "Referral",
            "last_contact": str(today - timedelta(days=1)),
            "next_followup": str(today),
            "notes": "Interested in a 3-bed sea-view apartment. Wants a second viewing.",
            "created_at": f"{today - timedelta(days=12)} 10:15:00",
        },
        {
            "name": "Bilal Ahmed",
            "phone": "0321-5556677",
            "email": "bilal.ahmed@email.com",
            "property": "House",
            "budget": 42_000_000,
            "location": "DHA",
            "status": "Site Visit",
            "source": "Website",
            "last_contact": str(today - timedelta(days=2)),
            "next_followup": str(today + timedelta(days=1)),
            "notes": "Looking at Phase 6 west-open houses.",
            "created_at": f"{today - timedelta(days=8)} 16:40:00",
        },
        {
            "name": "Sana Qureshi",
            "phone": "0333-8899001",
            "email": "sana.q@email.com",
            "property": "Plot",
            "budget": 25_000_000,
            "location": "Bahria Town",
            "status": "Contacted",
            "source": "Zameen.com",
            "last_contact": str(today - timedelta(days=4)),
            "next_followup": str(today + timedelta(days=2)),
            "notes": "Prefers a 500 sq yd plot near the sports complex.",
            "created_at": f"{today - timedelta(days=6)} 11:05:00",
        },
        {
            "name": "Usman Raza",
            "phone": "0345-2211009",
            "email": "usman.raza@email.com",
            "property": "Commercial",
            "budget": 60_000_000,
            "location": "Saddar",
            "status": "New",
            "source": "Walk-in",
            "last_contact": str(today),
            "next_followup": str(today + timedelta(days=3)),
            "notes": "Wants a shop on a main road for a pharmacy.",
            "created_at": f"{today} 09:20:00",
        },
        {
            "name": "Hira Siddiqui",
            "phone": "0312-7788990",
            "email": "hira.s@email.com",
            "property": "Apartment",
            "budget": 12_000_000,
            "location": "Gulshan-e-Iqbal",
            "status": "Converted",
            "source": "WhatsApp",
            "last_contact": str(today - timedelta(days=10)),
            "next_followup": "",
            "notes": "Closed on a 2-bed apartment in Block 13.",
            "created_at": f"{today - timedelta(days=21)} 14:00:00",
        },
        {
            "name": "Omar Farooq",
            "phone": "0301-4455667",
            "email": "omar.farooq@email.com",
            "property": "Villa",
            "budget": 85_000_000,
            "location": "DHA",
            "status": "Lost",
            "source": "Facebook",
            "last_contact": str(today - timedelta(days=7)),
            "next_followup": "",
            "notes": "Chose another agency after budget mismatch.",
            "created_at": f"{today - timedelta(days=18)} 12:30:00",
        },
        {
            "name": "Nimra Ali",
            "phone": "0331-9090887",
            "email": "nimra.ali@email.com",
            "property": "House",
            "budget": 22_000_000,
            "location": "PECHS",
            "status": "Contacted",
            "source": "Instagram",
            "last_contact": str(today - timedelta(days=5)),
            "next_followup": str(today - timedelta(days=1)),
            "notes": "Follow-up overdue. Ask about Block 2 vs Block 6.",
            "created_at": f"{today - timedelta(days=9)} 18:10:00",
        },
        {
            "name": "Farhan Malik",
            "phone": "0322-6677889",
            "email": "farhan.m@email.com",
            "property": "Apartment",
            "budget": 9_500_000,
            "location": "North Nazimabad",
            "status": "New",
            "source": "Website",
            "last_contact": "",
            "next_followup": str(today + timedelta(days=4)),
            "notes": "First-time buyer. Needs payment plan options.",
            "created_at": f"{today - timedelta(days=1)} 13:45:00",
        },
    ]
    for sample in samples:
        add_lead(**sample)
