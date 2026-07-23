import os
import cv2
import numpy as np
import joblib
from sklearn.neighbors import KNeighborsClassifier

# Paths
DATASET_PATH = "dataset"
MODEL_PATH = "models"

os.makedirs(MODEL_PATH, exist_ok=True)


def train_model():
    faces = []
    labels = []
    label_map = {}

    label_id = 0

    for folder in os.listdir(DATASET_PATH):

        folder_path = os.path.join(DATASET_PATH, folder)

        if not os.path.isdir(folder_path):
            continue

        label_map[label_id] = folder

        for image_name in os.listdir(folder_path):

            image_path = os.path.join(folder_path, image_name)

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                continue

            image = cv2.resize(image, (100, 100))

            faces.append(image.flatten())
            labels.append(label_id)

        label_id += 1

    if len(faces) == 0:
        print("No face images found!")
        return

    faces = np.array(faces)
    labels = np.array(labels)

    model = KNeighborsClassifier(n_neighbors=3)

    model.fit(faces, labels)

    joblib.dump(model, os.path.join(MODEL_PATH, "face_model.pkl"))
    joblib.dump(label_map, os.path.join(MODEL_PATH, "labels.pkl"))

    print("✅ Model trained successfully!")


if __name__ == "__main__":
    train_model()