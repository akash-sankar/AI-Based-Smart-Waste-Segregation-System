import cv2
import numpy as np
from tensorflow.keras.models import load_model
from ultralytics import YOLO
import os
import requests
ESP32_STREAM_URL = "http://192.168.137.69:81/stream"   
# ---------------- CONFIG ----------------
NODEMCU_IP = "http://192.168.137.121"
IMG_SIZE = 50
DATA_DIR = "data"

# ---------------- LOAD MODELS ----------------
print("Loading CNN model...")
cnn_model = load_model("CNN.model")

print("Loading YOLO model...")
yolo_model = YOLO("best.pt")

class_names = os.listdir(DATA_DIR)

print("Models Loaded Successfully")

# ---------------- PREPROCESS ----------------
def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(ESP32_STREAM_URL)

print("Press Q → Capture & Classify")
print("Press ESC → Exit")

last_crop = None

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera Error")
        break

    # ---------------- YOLO LIVE DETECTION ----------------
    results = yolo_model(frame, verbose=False)

    for r in results:

        boxes = r.boxes

        if boxes is None:
            continue

        for box in boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            if conf < 0.70:
                continue

            # Draw box
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            # Save latest crop
            last_crop = frame[y1:y2, x1:x2]

    cv2.imshow("Live Detection", frame)

    key = cv2.waitKey(1)

    # ---------------- PRESS Q ----------------
    if key & 0xFF == ord('q'):

        if last_crop is None:
            print("No object detected to classify")
            continue

        print("Running CNN classification...")

        processed = preprocess(last_crop)

        prediction = cnn_model.predict(processed)

        idx = np.argmax(prediction)
        print(idx)
        label = class_names[idx]
        confidence = float(np.max(prediction))*100

        print("Prediction:", label)
        print("Confidence:", confidence)

        cv2.imshow("Captured Object", last_crop)

        a=int(idx+1)
        print(label)
        url = f"{NODEMCU_IP}/{a}"
        requests.get(url, timeout=20)
        print("Sent:", url)


    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()