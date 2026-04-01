import sqlite3
import os
from pathlib import Path

def search_passhub(q, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM passwords WHERE name LIKE ? LIMIT 10", (f"%{q}%",))
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception:
        return []

def search_versions(q, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM versions WHERE title LIKE ? LIMIT 10", (f"%{q}%",))
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception:
        return []

def search_tickets(q, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT subject FROM tickets WHERE subject LIKE ? LIMIT 10", (f"%{q}%",))
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception:
        return []

def search_stack_memory(q, base_dir):
    try:
        md_files = Path(base_dir).glob("*.md")
        results = [f.name for f in md_files if q.lower() in f.name.lower()]
        return results[:10]
    except Exception:
        return []
