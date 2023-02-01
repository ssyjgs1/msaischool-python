"""CVAT XML to YOLO"""
import os
import glob
import cv2
from xml.etree.ElementTree import parse

"""xml 1 ~ 5 같이 여러 개 생기면 찾는 함수"""
def find_xml_file(xml_folder_path) :
    all_root = []
    for (path, dir, files) in os.walk(xml_folder_path) :
        for filename in files :
            ext = os.path.splitext(filename)[-1] # ext --> .xml
            if ext == ".xml" :
                root = os.path.join(path, filename) # ./xml_data/test.xml
                all_root.append(root)
            else : 
                print("No XML files....")
                break
    return all_root
# test = glob.glob(os.path.join(xml_folder_path, "*.xml")) # 위의 함수 대신 이런 방법도 쓸 수는 있다

xml_folder_dir = "./xml_data"
xml_paths = find_xml_file(xml_folder_dir)
# print(xml_paths)

# 기존꺼 갖다 붙인 방식이면 label_dict = {v:k for k,v in label_dict.items()} 이거 돌려도 됨
label_dict = {'big bus' : 0, 'big truck' : 1 , 'bus-l-' : 2, 'bus-s-':3 , 'car':4, 'mid truck':5, 'small bus':6, 'small truck':7, 'truck-l-':8, 'truck-m-':9, 'truck-s-':10, 'truck-xl-':11}

for xml_path in xml_paths :
    tree = parse(xml_path)
    root = tree.getroot()
    img_metas = root.findall("image")
    # print(img_metas)
    for img_meta in img_metas :
        # xml에 기록된 image name 가져오기
        image_name = img_meta.attrib['name']
        # print(image_name) # image_name >>> adit_mp4-498_jpg.rf.7ba4639065a7ae7ce846e5c30dd65ce9.jpg

        # Box meta 정보 뽑아오기 | XML은 모든 값이 str이라서 뭐 계산할 거면 int, float으로 바꿔줘야 함
        box_metas = img_meta.findall("box")
        img_width = int(img_meta.attrib['width'])
        img_height = int(img_meta.attrib['height'])
        # print(img_width, img_height)
        
        for box_meta in box_metas :
            box_label = box_meta.attrib['label']
            # print(box_label)
            box = [int(float(box_meta.attrib['xtl'])), int(float(box_meta.attrib['ytl'])), int(float(box_meta.attrib['xbr'])), int(float(box_meta.attrib['ybr']))]
            # print(box_label, box)

            # yolo 형식에 맞게 normalization을 해보자
            yolo_x = round(((box[0] + box[2]) / 2) / img_width, 6)
            yolo_y = round(((box[1] + box[3]) / 2) / img_height, 6)
            yolo_w = round((box[2] - box[0]) / img_width, 6)
            yolo_h = round((box[3] - box[1]) / img_height, 6)
            # print("yolo xywh >>>", yolo_x, yolo_y, yolo_w, yolo_h)

            image_name_temp = image_name.replace(".jpg", ".txt")

            # txt file save folder 만들기
            os.makedirs("./cvat_xml_to_yolo_txt", exist_ok=True)
            
            # label
            label = label_dict[box_label]
            # print(label) # 4.....+ 그 외 숫자들

            # 앞서 모은 정보들로 txt파일로 저장해보자
            with open(f"./cvat_xml_to_yolo_txt/{image_name_temp}", 'a') as f :
                f.write(f"{label} {yolo_x} {yolo_y} {yolo_w} {yolo_h} \n")