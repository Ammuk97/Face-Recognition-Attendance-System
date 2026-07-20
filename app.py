from flask import Flask, render_template, request
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

        # Get data from form
        name = request.form["name"]
        roll = request.form["roll"]

        # Save to database
        success = add_student(name, roll)

        if success:

            # Open webcam and capture face images
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

                        <br>

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

                        <br>

                        <a href="/register" class="btn btn-warning">
                            Try Again
                        </a>

                    </div>

                </div>

            </body>
            </html>
            """

    return render_template("register.html")


# ---------------- START FLASK ---------------- #

if __name__ == "__main__":
    app.run(debug=True)