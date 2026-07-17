import cv2
import mediapipe as mp
import os


def capture_faces(name, roll):

    folder_name = f"{roll}_{name}"
    dataset_path = os.path.join("dataset", folder_name)
    os.makedirs(dataset_path, exist_ok=True)

    mp_face_detection = mp.solutions.face_detection
    detector = mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.6
    )

    camera = cv2.VideoCapture(0)

    count = 0

    print("Camera Started...")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = detector.process(rgb)

        if results.detections:

            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                h, w, _ = frame.shape

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                x = max(0, x)
                y = max(0, y)

                face = frame[y:y+height, x:x+width]

                if face.size == 0:
                    continue

                face = cv2.resize(face, (200, 200))

                count += 1

                cv2.imwrite(
                    os.path.join(dataset_path, f"{count}.jpg"),
                    face
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Captured {count}/50",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Student Registration", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if count >= 50:
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Registration Completed")