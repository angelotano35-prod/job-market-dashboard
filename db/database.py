import sqlite3

DB_PATH = "data/jobs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            tags TEXT,
            date_posted TEXT,
            url TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def insert_job(job):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO jobs (source, title, company, location, tags, date_posted, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job["source"], job["title"], job["company"],
        job["location"], job["tags"], job["date_posted"], job["url"]
    ))
    conn.commit()
    conn.close()