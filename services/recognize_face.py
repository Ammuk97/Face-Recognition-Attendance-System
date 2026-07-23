from attendance import mark_attendance

import cv2
import os
import time
import joblib
import numpy as np

# -----------------------------
# Load Trained Model
# -----------------------------
model = joblib.load("models/face_model.pkl")
label_map = joblib.load("models/labels.pkl")

# -----------------------------
# Load Haar Cascade
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# XML file is in the project root
cascade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

print("Cascade Path:", cascade_path)

face_detector = cv2.CascadeClassifier(cascade_path)

if face_detector.empty():
    print("❌ ERROR: Could not load Haar Cascade!")
    exit()

print("✅ Haar Cascade loaded successfully!")

# -----------------------------
# Start Camera
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ ERROR: Camera could not be opened!")
    exit()

print("📷 Camera started... Press Q to quit.")

# -----------------------------
# Prevent repeated attendance
# -----------------------------
marked_students = {}
COOLDOWN = 10  # seconds

# -----------------------------
# Face Recognition Loop
# -----------------------------
while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        # Extract face
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))
        face = face.flatten().reshape(1, -1)

        try:
            prediction = model.predict(face)[0]
            student = label_map[prediction]

            current_time = time.time()

            # Mark attendance only once every 10 seconds
            if (
                student not in marked_students
                or current_time - marked_students[student] > COOLDOWN
            ):
                mark_attendance(student)
                marked_students[student] = current_time

            # Draw rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Display student name
            cv2.putText(
                frame,
                student,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        except Exception as e:
            print("Recognition Error:", e)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# Cleanup
# -----------------------------
camera.release()
cv2.destroyAllWindows()