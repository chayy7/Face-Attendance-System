import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create attendance table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()
print("✅ Database initialized successfully!")
