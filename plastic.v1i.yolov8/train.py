import os
import shutil
import yaml
from sklearn.model_selection import train_test_split
from ultralytics import YOLO

# ------------------ CHANGE THIS PATH ------------------
SOURCE_DATASET = r"C:\Users\arula\Downloads\plastic.v1i.yolov8"

IMAGE_DIR = os.path.join(SOURCE_DATASET, "images")
LABEL_DIR = os.path.join(SOURCE_DATASET, "labels")
WORKING_DIR = os.path.join(SOURCE_DATASET, "dataset_split")


def main():

    # ------------------ CREATE TRAIN/VAL STRUCTURE ------------------
    train_img_dir = os.path.join(WORKING_DIR, "images/train")
    val_img_dir = os.path.join(WORKING_DIR, "images/val")
    train_lbl_dir = os.path.join(WORKING_DIR, "labels/train")
    val_lbl_dir = os.path.join(WORKING_DIR, "labels/val")

    for folder in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
        os.makedirs(folder, exist_ok=True)

    # ------------------ GET IMAGE FILES ------------------
    images = [f for f in os.listdir(IMAGE_DIR)
              if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    # ------------------ SPLIT 80/20 ------------------
    train_files, val_files = train_test_split(
        images, test_size=0.2, random_state=42)

    print(f"Total Images: {len(images)}")
    print(f"Training: {len(train_files)}")
    print(f"Validation: {len(val_files)}")

    # ------------------ COPY FILES ------------------
    def copy_files(file_list, img_dest, lbl_dest):
        for file in file_list:
            img_src = os.path.join(IMAGE_DIR, file)
            lbl_file = os.path.splitext(file)[0] + ".txt"
            lbl_src = os.path.join(LABEL_DIR, lbl_file)

            if os.path.exists(lbl_src):
                shutil.copy(img_src, img_dest)
                shutil.copy(lbl_src, lbl_dest)

    copy_files(train_files, train_img_dir, train_lbl_dir)
    copy_files(val_files, val_img_dir, val_lbl_dir)

    print("Dataset split completed!")

    # ------------------ CONVERT ALL LABELS TO CLASS 0 ------------------
    def convert_to_single_class(label_folder):
        for file in os.listdir(label_folder):
            if file.endswith(".txt"):
                path = os.path.join(label_folder, file)

                new_lines = []
                with open(path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            parts[0] = "0"   # 🔥 convert class to 0
                            new_lines.append(" ".join(parts))

                with open(path, "w") as f:
                    f.write("\n".join(new_lines))

    convert_to_single_class(train_lbl_dir)
    convert_to_single_class(val_lbl_dir)

    print("All labels converted to single class.")

    # ------------------ CREATE data.yaml ------------------
    data_yaml = {
        'path': WORKING_DIR,
        'train': 'images/train',
        'val': 'images/val',
        'nc': 1,
        'names': ['waste']
    }

    yaml_path = os.path.join(SOURCE_DATASET, "data_auto.yaml")

    with open(yaml_path, "w") as f:
        yaml.dump(data_yaml, f)

    print("data_auto.yaml created!")

    # ------------------ LOAD MODEL ------------------
    model = YOLO("yolov8m.pt")

    # ------------------ TRAIN ------------------
    model.train(
        data=yaml_path,
        epochs=100,
        imgsz=240,
        batch=8,
        device=0,   # change to "cpu" if no GPU
        workers=0   # important for Windows
    )

    print("Training Completed!")

    # ------------------ VALIDATE ------------------
    metrics = model.val()
    print(metrics)


if __name__ == "__main__":
    main()
