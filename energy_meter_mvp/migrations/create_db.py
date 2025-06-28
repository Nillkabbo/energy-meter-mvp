import sqlite3

conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    smart_meter_id TEXT NOT NULL,
    start_datetime TEXT NOT NULL,
    end_datetime TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT,
    error_message TEXT,
    record_count INTEGER,
    file_size_bytes INTEGER
);
''')
conn.commit()
conn.close() 