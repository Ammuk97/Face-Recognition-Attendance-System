import sqlite3
from datetime import datetime


def mark_attendance(student):

    roll, name = student.split("_", 1)

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
        SELECT * FROM attendance
        WHERE roll=? AND date=?
    """, (roll, today))

    data = cursor.fetchone()

    if data is None:

        cursor.execute("""
            INSERT INTO attendance
            (roll, name, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            roll,
            name,
            today,
            current_time,
            "Present"
        ))

        conn.commit()

        print(f"✅ Attendance marked for {name}")

    else:

        print(f"ℹ Attendance already marked for {name}")

    conn.close()