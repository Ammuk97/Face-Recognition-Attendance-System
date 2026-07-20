import mediapipe as mp

print("MediaPipe Version:", mp.__version__)
print("Has solutions:", hasattr(mp, "solutions"))

if hasattr(mp, "solutions"):
    print("MediaPipe is working correctly!")
else:
    print("MediaPipe installation/problem detected.")