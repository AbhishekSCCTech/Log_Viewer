import os
import sqlite3
from pathlib import Path

LOG_DIR = 'logs'
DB_FILE = 'log_data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    txt_files = Path(LOG_DIR).glob("*.txt")
    for txt_file in txt_files:
        with open(txt_file, 'r') as file:
            content = file.read()
        # Avoid duplicates
        cursor.execute("SELECT 1 FROM logs WHERE filename = ?", (txt_file.name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO logs (filename, content) VALUES (?, ?)",
                           (txt_file.name, content))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, content FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

