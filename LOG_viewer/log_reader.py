import os
import sqlite3
from pathlib import Path
from datetime import datetime

LOG_DIR = 'logs'
DB_FILE = 'log_data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            timestamp TEXT
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
            timestamp = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO logs (filename, content, timestamp) VALUES (?, ?, ?)",
                (txt_file.name, content, timestamp)
            )
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, content, timestamp FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    logs = [{'filename': r[0], 'content': r[1], 'timestamp': r[2]} for r in rows]
    return logs
    
