"""SQLite persistence for services and health-check history."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "monitor.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id INTEGER NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('UP', 'DOWN')),
                http_status INTEGER,
                response_ms REAL NOT NULL,
                message TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                FOREIGN KEY(service_id) REFERENCES services(id) ON DELETE CASCADE
            )
        """)


def add_service(name, url):
    name = name.strip()
    url = url.strip()
    if len(name) > 80:
        raise ValueError("Service name must be 80 characters or fewer.")
    try:
        with connect() as db:
            db.execute("INSERT INTO services(name, url) VALUES (?, ?)", (name, url))
    except sqlite3.IntegrityError:
        raise ValueError("That URL is already being monitored.") from None


def save_check(service_id, result):
    with connect() as db:
        db.execute("""
            INSERT INTO checks(service_id, status, http_status, response_ms, message, checked_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            service_id, result["status"], result["http_status"],
            result["response_ms"], result["message"], result["checked_at"]
        ))


def get_services():
    with connect() as db:
        rows = db.execute("""
            SELECT s.id, s.name, s.url, s.created_at,
                   c.status AS last_status, c.http_status AS last_http_status,
                   c.response_ms AS last_response_ms, c.message AS last_message,
                   c.checked_at AS last_checked_at
            FROM services s
            LEFT JOIN checks c ON c.id = (
                SELECT c2.id FROM checks c2
                WHERE c2.service_id = s.id
                ORDER BY c2.id DESC LIMIT 1
            )
            ORDER BY s.id DESC
        """).fetchall()
    return [dict(row) for row in rows]


def get_history(limit=10):
    with connect() as db:
        rows = db.execute("""
            SELECT c.*, s.name AS service_name, s.url AS service_url
            FROM checks c JOIN services s ON s.id = c.service_id
            ORDER BY c.id DESC LIMIT ?
        """, (limit,)).fetchall()
    return [dict(row) for row in rows]


def delete_service(service_id):
    with connect() as db:
        db.execute("DELETE FROM services WHERE id = ?", (service_id,))
