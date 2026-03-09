
import sqlite3
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS processos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT,
        data TEXT,
        local TEXT,
        latitude REAL,
        longitude REAL,
        infrator TEXT,
        descricao TEXT,
        regimes TEXT,
        gravidade TEXT
    )
    """)

    conn.commit()
    conn.close()
