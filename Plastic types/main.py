import os
import cv2
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Activation

# ================= CONFIG =================
DATASET_DIR = "data"     # <-- main folder
IMG_SIZE = 50
BATCH_SIZE = 32
EPOCHS = 15

# ================= LOAD DATA =================
data = []
class_names = sorted(os.listdir(DATASET_DIR))

print("Classes found:", class_names)

for class_name in class_names:
    class_path = os.path.join(DATASET_DIR, class_name)

    # Walk through ALL subfolders
    for root, dirs, files in os.walk(class_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                data.append((img_path, class_name))

print("Total images:", len(data))

# ================= PREPROCESS =================
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    return img

X, y = [], []

for img_path, label in data:
    img = preprocess_image(img_path)
    if img is not None:
        X.append(img)
        y.append(class_names.index(label))

X = np.array(X*2)
y = np.array(y*2)

print("Final X shape:", X.shape)
print("Final y shape:", y.shape)

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================= MODEL =================
model = Sequential([
    Conv2D(32, (3,3), input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    Activation("relu"),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3)),
    Activation("relu"),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3)),
    Activation("relu"),
    MaxPooling2D(2,2),
    Dropout(0.25),

    Flatten(),
    Dense(128),
    Activation("relu"),

    Dense(128),
    Activation("relu"),

    Dense(len(class_names)),
    Activation("softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ================= TRAIN =================
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2
)

# ================= SAVE =================
model.save("CNN.model")
print("✅ Model saved as CNN.model")

# ================= EVALUATE =================
y_pred = np.argmax(model.predict(X_test), axis=1)

acc = accuracy_score(y_test, y_pred) * 100
print(f"Test Accuracy: {acc:.2f}%")

print("\nClassification Report\n")
print(classification_report(y_test, y_pred, target_names=class_names))

# ================= CONFUSION MATRIX =================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8,8))
sns.heatmap(cm, annot=True, cmap="Blues",
            xticklabels=class_names,
            yticklabels=class_names,
            fmt="d")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# ================= ACC / LOSS CURVES =================
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label="Train")
plt.plot(history.history['val_accuracy'], label="Val")
plt.title("Accuracy")
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label="Train")
plt.plot(history.history['val_loss'], label="Val")
plt.title("Loss")
plt.legend()

plt.show()
