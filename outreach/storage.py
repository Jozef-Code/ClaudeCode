import sqlite3
import json
import os
from datetime import datetime
from typing import Set, List
from .models import OutreachRecord

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outreach.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contacted_companies (
                lusha_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT,
                contacted_date TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS outreach_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                company_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                manager_name TEXT NOT NULL,
                manager_title TEXT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'Te versturen',
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def get_contacted_company_ids() -> Set[str]:
    init_db()
    with _conn() as conn:
        rows = conn.execute("SELECT lusha_id FROM contacted_companies").fetchall()
    return {row[0] for row in rows}


def mark_company_contacted(lusha_id: str, name: str, domain: str = None):
    init_db()
    with _conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO contacted_companies (lusha_id, name, domain, contacted_date) VALUES (?, ?, ?, ?)",
            (lusha_id, name, domain, datetime.now().isoformat())
        )
        conn.commit()


def save_outreach_record(record: OutreachRecord):
    init_db()
    mark_company_contacted(
        record.company.lusha_id,
        record.company.name,
        record.company.domain
    )
    with _conn() as conn:
        conn.execute(
            """INSERT INTO outreach_records
               (date, company_id, company_name, manager_name, manager_title, role, message, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record.date,
                record.company.lusha_id,
                record.company.name,
                record.hiring_manager.full_name,
                record.hiring_manager.title,
                record.inferred_role,
                record.message,
                record.status,
            )
        )
        conn.commit()


def get_stats() -> dict:
    init_db()
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM contacted_companies").fetchone()[0]
        today = conn.execute(
            "SELECT COUNT(*) FROM contacted_companies WHERE contacted_date >= date('now')"
        ).fetchone()[0]
        by_status = conn.execute(
            "SELECT status, COUNT(*) FROM outreach_records GROUP BY status"
        ).fetchall()
    return {
        "total_contacted": total,
        "contacted_today": today,
        "by_status": dict(by_status),
    }
