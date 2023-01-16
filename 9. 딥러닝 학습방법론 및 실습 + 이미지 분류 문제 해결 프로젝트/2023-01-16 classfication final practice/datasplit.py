"""
label -> dark, green, light, medium
org_data
image
    - labels image.png
test
    - labels image.png

dataset
  train
    - dark
    - green
    - light
    - mdium
  val
    - dark
    - green
    - light
    - mdium
"""
import os
import glob
import shutil

image_folder_path = "./test_image"
image_path = glob.glob(os.path.join(image_folder_path, "*.png"))

for path in image_path :
    file_name = os.path.basename(path)
    if "dark" in file_name :
        # file move
        os.makedirs("./dataset/val/dark/", exist_ok=True)
        shutil.move(path,f"./dataset/val/dark/{file_name}")
    elif "green" in file_name :
        # file move
        os.makedirs("./dataset/val/green/" , exist_ok=True)
        shutil.move(path, f"./dataset/val/green/{file_name}")
    elif "light" in file_name :
        # file move
        os.makedirs("./dataset/val/light/" , exist_ok=True)
        shutil.move(path, f"./dataset/val/light/{file_name}")
    elif "medium" in file_name :
        # file move
        os.makedirs("./dataset/val/medium/" , exist_ok=True)
        shutil.move(path, f"./dataset/val/medium/{file_name}")