import sqlite3
import os

print("Current Working Directory:", os.getcwd())

os.makedirs("database", exist_ok=True)

db_path = os.path.abspath("database/attendance.db")
print("Database Path:", db_path)

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")