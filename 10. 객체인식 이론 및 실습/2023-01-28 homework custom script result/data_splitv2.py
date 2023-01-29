from sklearn.model_selection import train_test_split
import os
import glob
import cv2
import shutil
import copy

# 데이터 나누기
# train 80 val 10 test 10

origin_path = "./wine labels_voc_dataset"

# dekopon 이미지 경로 -> list
images = glob.glob(os.path.join(origin_path, "*.jpg"))
texts = glob.glob(os.path.join(origin_path, "*.txt"))


train_image, val_image = train_test_split(images , test_size= 0.2, random_state= 777)
val_image, test_image  = train_test_split(val_image, test_size= 0.5, random_state= 777)
train_texts, val_texts = train_test_split(texts , test_size= 0.2, random_state= 777)
val_texts, test_texts  = train_test_split(val_texts, test_size= 0.5, random_state= 777)


for i in train_image:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/train/images", exist_ok=True)
    shutil.move(i, f"./dataset/train/images/{file_name}")

for i in val_image:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/valid/images", exist_ok=True)
    shutil.move(i, f"./dataset/valid/images/{file_name}")

for i in test_image:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/test/images", exist_ok=True)
    shutil.move(i, f"./dataset/test/images/{file_name}")

for i in train_texts:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/train/labels", exist_ok=True)
    shutil.move(i, f"./dataset/train/labels/{file_name}")

for i in val_texts:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/valid/labels", exist_ok=True)
    shutil.move(i, f"./dataset/valid/labels/{file_name}")

for i in test_texts:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/test/labels", exist_ok=True)
    shutil.move(i, f"./dataset/test/labels/{file_name}")