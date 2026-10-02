import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "os.sqlite"


def get_connection():
    """Возвращает соединение с базой данных StudyOS."""
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            content TEXT,
            owner TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS processes (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            owner TEXT,
            memory INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syscall_name TEXT NOT NULL,
            args TEXT,
            user TEXT,
            status TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (login, password_hash, role) VALUES (?, ?, ?)",
        ("admin", "abc123", "admin"),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("База данных создана:", DB_PATH)
