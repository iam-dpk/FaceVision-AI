import sqlite3
from datetime import datetime
from .config import DB_DIR, ensure_dirs

DB_FILE = DB_DIR / "facevision.db"

def connect():
    ensure_dirs()
    return sqlite3.connect(DB_FILE)

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS persons(
            person_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            image_path TEXT,
            embedding_path TEXT,
            created_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Present'
        )""")
        con.commit()

def add_person(person_id, name, image_path="", embedding_path=""):
    init_db()
    with connect() as con:
        con.execute(
            """INSERT INTO persons(person_id,name,image_path,embedding_path,created_at)
               VALUES (?,?,?,?,?)
               ON CONFLICT(person_id) DO UPDATE SET
                 name=excluded.name,image_path=excluded.image_path,
                 embedding_path=excluded.embedding_path""",
            (person_id, name, image_path, embedding_path,
             datetime.now().isoformat(timespec="seconds"))
        )
        con.commit()

def remove_person(person_id):
    init_db()
    with connect() as con:
        con.execute("DELETE FROM persons WHERE person_id=?", (person_id,))
        con.commit()

def list_persons():
    init_db()
    with connect() as con:
        return con.execute(
            "SELECT person_id,name,image_path,embedding_path,created_at "
            "FROM persons ORDER BY name"
        ).fetchall()

def add_attendance(person_id, name, timestamp=None, status="Present"):
    init_db()
    timestamp = timestamp or datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        con.execute(
            "INSERT INTO attendance(person_id,name,timestamp,status) VALUES (?,?,?,?)",
            (person_id, name, timestamp, status)
        )
        con.commit()

def last_attendance_for(person_id):
    init_db()
    with connect() as con:
        return con.execute(
            "SELECT timestamp FROM attendance WHERE person_id=? "
            "ORDER BY timestamp DESC LIMIT 1", (person_id,)
        ).fetchone()

def list_attendance(query=""):
    init_db()
    with connect() as con:
        if query:
            q = f"%{query}%"
            return con.execute(
                """SELECT id,person_id,name,timestamp,status FROM attendance
                   WHERE person_id LIKE ? OR name LIKE ? OR timestamp LIKE ?
                   ORDER BY timestamp DESC""", (q, q, q)
            ).fetchall()
        return con.execute(
            "SELECT id,person_id,name,timestamp,status FROM attendance ORDER BY timestamp DESC"
        ).fetchall()

def clear_attendance():
    init_db()
    with connect() as con:
        con.execute("DELETE FROM attendance")
        con.commit()
