import sqlite3

DATABASE = "database/scamshield.db"


def create_database():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            score INTEGER NOT NULL,
            status TEXT NOT NULL,
            reasons TEXT NOT NULL,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_scan(url, score, status, reasons):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history
        (url, score, status, reasons)
        VALUES (?, ?, ?, ?)
    """, (
        url,
        score,
        status,
        ", ".join(reasons)
    ))

    conn.commit()
    conn.close()


def get_scan_history():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, score, status, reasons, scanned_at
        FROM scan_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
