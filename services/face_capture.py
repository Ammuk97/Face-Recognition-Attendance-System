import cv2
import os


def capture_faces(name, roll):
    folder_name = f"{roll}_{name}"
    dataset_path = os.path.join("dataset", folder_name)

    os.makedirs(dataset_path, exist_ok=True)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera not found!")
        return False

    count = 0

    print("Camera started. Look at the camera.")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        count += 1

        image_path = os.path.join(dataset_path, f"{count}.jpg")

        cv2.imwrite(image_path, gray)

        cv2.putText(
            frame,
            f"Captured: {count}/100",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Capture", frame)

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        if count >= 100:
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Face capture completed!")

    return True