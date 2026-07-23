import pandas as pd
import sqlite3

from flask import Flask, render_template, request, send_file
from database_manager import add_student
from register import capture_faces

app = Flask(__name__)

# ---------------- HOME PAGE ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER STUDENT ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]

        success = add_student(name, roll)

        if success:

            capture_faces(name, roll)

            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Registration Successful</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>

            <body class="bg-light">

                <div class="container mt-5">

                    <div class="card shadow p-4">

                        <h2 class="text-success">
                            ✅ Student Registered Successfully
                        </h2>

                        <hr>

                        <h4>Name : {name}</h4>
                        <h4>Roll Number : {roll}</h4>

                        <p>50 face images have been captured successfully.</p>

                        <a href="/" class="btn btn-primary">
                            Back to Home
                        </a>

                    </div>

                </div>

            </body>
            </html>
            """

        else:

            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>

            <body class="bg-light">

                <div class="container mt-5">

                    <div class="card shadow p-4">

                        <h2 class="text-danger">
                            ❌ Roll Number Already Exists
                        </h2>

                        <a href="/register" class="btn btn-warning">
                            Try Again
                        </a>

                    </div>

                </div>

            </body>
            </html>
            """

    return render_template("register.html")


# ---------------- ATTENDANCE DASHBOARD ---------------- #

@app.route("/attendance")
def attendance():

    search = request.args.get("search", "").strip()
    date = request.args.get("date", "").strip()

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    query = """
        SELECT roll, name, date, time, status
        FROM attendance
        WHERE 1=1
    """

    params = []

    if search:
        query += " AND (name LIKE ? OR roll LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if date:
        query += " AND date=?"
        params.append(date)

    query += " ORDER BY date DESC, time DESC"

    cursor.execute(query, params)

    records = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "attendance.html",
        records=records,
        total_students=total_students,
        total_attendance=total_attendance,
        search=search,
        date=date
    )


# ---------------- EXPORT ATTENDANCE CSV ---------------- #

@app.route("/export")
def export():

    conn = sqlite3.connect("database/attendance.db")

    df = pd.read_sql_query(
        """
        SELECT roll, name, date, time, status
        FROM attendance
        ORDER BY date DESC, time DESC
        """,
        conn
    )

    conn.close()

    file_name = "attendance_report.csv"

    df.to_csv(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True,
        download_name="attendance_report.csv"
    )


# ---------------- START FLASK ---------------- #

if __name__ == "__main__":
    app.run(debug=True)