import os
import shutil
import subprocess
import sys
import sqlite3
import pandas as pd

from database_manager import add_student
from register import capture_faces
from flask import Flask, render_template, request, send_file, redirect, url_for

app = Flask(__name__)

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================================
# REGISTER STUDENT
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]

        success = add_student(name, roll)

        if success:

            capture_faces(name, roll)

            return f"""
            <html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>

            <body class="bg-light">

            <div class="container mt-5">

            <div class="card shadow p-4">

            <h2 class="text-success">
            Student Registered Successfully
            </h2>

            <hr>

            <h4>Name : {name}</h4>
            <h4>Roll Number : {roll}</h4>

            <p>Face images captured successfully.</p>

            <a href="/" class="btn btn-primary">
            Back Home
            </a>

            </div>

            </div>

            </body>
            </html>
            """

        else:

            return """
            <script>
            alert("Roll Number Already Exists!");
            window.location="/register";
            </script>
            """

    return render_template("register.html")


# ==========================================================
# ATTENDANCE DASHBOARD
# ==========================================================

@app.route("/attendance")
def attendance():

    search = request.args.get("search", "").strip()
    date = request.args.get("date", "").strip()

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    query = """
    SELECT roll,name,date,time,status
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

    query += " ORDER BY date DESC,time DESC"

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
        date=date,
    )


# ==========================================================
# EXPORT CSV
# ==========================================================

@app.route("/export")
def export():

    conn = sqlite3.connect("database/attendance.db")

    df = pd.read_sql_query(
        """
        SELECT roll,name,date,time,status
        FROM attendance
        ORDER BY date DESC,time DESC
        """,
        conn,
    )

    conn.close()

    filename = "attendance_report.csv"

    df.to_csv(filename, index=False)

    return send_file(
        filename,
        as_attachment=True,
        download_name="attendance_report.csv",
    )


# ==========================================================
# START ATTENDANCE
# ==========================================================

@app.route("/start_attendance")
def start_attendance():

    subprocess.Popen(
        [sys.executable, "services/recognize_face.py"]
    )

    return """
    <script>
    alert("Attendance Recognition Started");
    window.location="/attendance";
    </script>
    """


# ==========================================================
# STUDENT MANAGEMENT
# ==========================================================

@app.route("/students")
def students():

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,roll,name
        FROM students
        ORDER BY id
    """)

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students,
    )


# ==========================================================
# DELETE STUDENT
# ==========================================================

@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT roll,name FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    if student:
        roll, name = student

        cursor.execute("DELETE FROM attendance WHERE roll=?", (roll,))
        cursor.execute("DELETE FROM students WHERE id=?", (id,))
        conn.commit()

        folder = f"dataset/{roll}_{name}"
        if os.path.exists(folder):
            shutil.rmtree(folder)

    conn.close()

    return """
    <script>
    alert("Student Deleted Successfully!");
    window.location="/students";
    </script>
    """


# ==========================================================
# EDIT STUDENT
# ==========================================================

@app.route("/edit_student/<int:id>", methods=["GET","POST"])
def edit_student(id):

    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name=request.form["name"]
        roll=request.form["roll"]

        cursor.execute(
            "UPDATE students SET name=?, roll=? WHERE id=?",
            (name, roll, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("students"))

    cursor.execute("SELECT id, roll, name FROM students WHERE id=?", (id,))
    student=cursor.fetchone()
    conn.close()

    return render_template("edit_student.html", student=student)

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)