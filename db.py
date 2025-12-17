import sqlite3

conn = sqlite3.connect("media_jobs.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT,
    type TEXT,
    status TEXT
)
""")

conn.commit()
