import sqlite3

DB_PATH = "users.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                voice_id TEXT
            )
        """)


def get_voice_id(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT voice_id FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row[0] if row else None


def set_voice_id(user_id: int, voice_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO users (user_id, voice_id) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET voice_id = excluded.voice_id",
            (user_id, voice_id)
        )