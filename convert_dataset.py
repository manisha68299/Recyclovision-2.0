import os
import random
import shutil

# 🔥 CHANGE THIS TO YOUR RAW DATASET PATH
SOURCE_DIR = "dataset_raw"

DEST_IMAGES_TRAIN = "dataset/images/train"
DEST_IMAGES_VAL = "dataset/images/val"
DEST_LABELS_TRAIN = "dataset/labels/train"
DEST_LABELS_VAL = "dataset/labels/val"

os.makedirs(DEST_IMAGES_TRAIN, exist_ok=True)
os.makedirs(DEST_IMAGES_VAL, exist_ok=True)
os.makedirs(DEST_LABELS_TRAIN, exist_ok=True)
os.makedirs(DEST_LABELS_VAL, exist_ok=True)

class_map = {
    "Plastic": 0,
    "Metal": 1,
    "Paper": 2,
    "Cardboard": 3,
    "Glass": 4,
    "Trash": 5
}

for class_name, class_id in class_map.items():

    class_path = os.path.join(SOURCE_DIR, class_name)
    images = os.listdir(class_path)

    for img in images:

        src_img_path = os.path.join(class_path, img)

        # 80/20 split
        if random.random() < 0.8:
            dest_img_path = os.path.join(DEST_IMAGES_TRAIN, img)
            dest_label_path = os.path.join(DEST_LABELS_TRAIN, img.replace(".jpg", ".txt"))
        else:
            dest_img_path = os.path.join(DEST_IMAGES_VAL, img)
            dest_label_path = os.path.join(DEST_LABELS_VAL, img.replace(".jpg", ".txt"))

        shutil.copyfile(src_img_path, dest_img_path)

        # YOLO label format: class x_center y_center width height
        # Full image box (0.5,0.5 center, full width/height)
        with open(dest_label_path, "w") as f:
            f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

print("✅ Dataset converted to YOLO format successfully!")