import cv2

# Open the default webcam
camera = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not camera.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("✅ Webcam started.")
print("Press 'Q' to quit.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("❌ Failed to capture frame.")
        break

    # Display the live camera feed
    cv2.imshow("Smart Attendance Camera", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()