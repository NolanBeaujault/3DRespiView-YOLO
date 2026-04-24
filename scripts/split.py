import os
import random
import shutil

base_dir = "3_yolo_dataset/v2_obb"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

for split in ["train", "val"]:
    os.makedirs(os.path.join(images_dir, split), exist_ok=True)
    os.makedirs(os.path.join(labels_dir, split), exist_ok=True)

images = [f for f in os.listdir(images_dir) if f.endswith(".jpg")]
random.shuffle(images)

split_index = int(len(images) * 0.8)
train_images = images[:split_index]
val_images = images[split_index:]


def move_files(file_list, split_name):
    for img_name in file_list:
        txt_name = img_name.replace(".jpg", ".txt")

        shutil.move(
            os.path.join(images_dir, img_name),
            os.path.join(images_dir, split_name, img_name),
        )

        if os.path.exists(os.path.join(labels_dir, txt_name)):
            shutil.move(
                os.path.join(labels_dir, txt_name),
                os.path.join(labels_dir, split_name, txt_name),
            )


move_files(train_images, "train")
move_files(val_images, "val")

yaml_content = """path: /workspace/3_yolo_dataset/v2_obb
train: images/train
val: images/val

names:
  0: thoracoabdominal
"""

with open(os.path.join(base_dir, "dataset.yaml"), "w") as f:
    f.write(yaml_content)

print(
    f"Terminé ! {len(train_images)} images pour l'entraînement, {len(val_images)} pour la validation."
)
print("Fichier dataset.yaml créé avec succès.")
