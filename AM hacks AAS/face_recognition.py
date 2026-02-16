import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime

# ==============================
# KNN FUNCTIONS
# ==============================

def distance(v1, v2):
    return np.sqrt(((v1 - v2) ** 2).sum())

def knn(train, test, k=5):
    distances = []

    for i in range(train.shape[0]):
        features = train[i, :-1]
        label = train[i, -1]
        d = distance(test, features)
        distances.append([d, label])

    distances = sorted(distances, key=lambda x: x[0])[:k]
    labels = np.array(distances)[:, -1]
    values, counts = np.unique(labels, return_counts=True)

    return values[np.argmax(counts)]

# ==============================
# PATH SETUP
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "face_dataset")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
CSV_PATH = os.path.join(BASE_DIR, "attendance.csv")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ==============================
# LOAD FACE DATASET
# ==============================

face_data = []
labels = []
class_id = 0
names = {}

if not os.path.exists(DATASET_PATH):
    print("❌ face_dataset folder not found!")
    exit()

for file in os.listdir(DATASET_PATH):
    if file.endswith(".npy"):
        names[class_id] = file[:-4]
        data_item = np.load(os.path.join(DATASET_PATH, file))
        face_data.append(data_item)

        target = class_id * np.ones((data_item.shape[0],))
        labels.append(target)

        class_id += 1

if len(face_data) == 0:
    print("❌ No training data found!")
    exit()

face_dataset = np.concatenate(face_data, axis=0)
face_labels = np.concatenate(labels, axis=0).reshape((-1, 1))
trainset = np.concatenate((face_dataset, face_labels), axis=1)

print("✅ Dataset loaded")
print("Classes:", names)

# ==============================
# START CAMERA
# ==============================

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    os.path.join(BASE_DIR, "haarcascade_frontalface_alt.xml")
)

if face_cascade.empty():
    print("❌ Haarcascade file missing!")
    exit()

print("\nPress 's' to save attendance")
print("Press 'q' to quit\n")

# ==============================
# MAIN LOOP
# ==============================

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    detected_names = []

    for (x, y, w, h) in faces:
        face_section = frame[y:y+h, x:x+w]
        face_section = cv2.resize(face_section, (100, 100))
        face_flatten = face_section.flatten()

        prediction = knn(trainset, face_flatten)
        name = names[int(prediction)]

        detected_names.append(name)

        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Face Recognition Attendance", frame)

    key = cv2.waitKey(1) & 0xFF

    # ==============================
    # SAVE ATTENDANCE (ALWAYS SAVE)
    # ==============================

    if key == ord('s') and len(detected_names) > 0:

        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H-%M-%S")

        screenshot_name = f"screenshot_{date_str}_{time_str}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)

        # Save screenshot
        cv2.imwrite(screenshot_path, frame)
        print(f"📸 Screenshot saved: {screenshot_name}")

        rows = []

        for name in detected_names:
            rows.append([name, date_str, time_str, screenshot_name])

        df_new = pd.DataFrame(rows,
                              columns=["Name", "Date", "Time", "Screenshot"])

        # Always append (no duplicate checking)
        if os.path.exists(CSV_PATH):
            df_new.to_csv(CSV_PATH, mode='a', header=False, index=False)
        else:
            df_new.to_csv(CSV_PATH, index=False)

        print("📝 Attendance saved (multiple entries allowed)\n")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
