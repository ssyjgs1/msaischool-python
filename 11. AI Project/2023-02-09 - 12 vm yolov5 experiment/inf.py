# wine dataset 기준으로 짰던 inference.py
import torch
import os
import glob
import cv2
import xml.etree.ElementTree as ET

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# model call
model = torch.hub.load('ultralytics/yolov5', 'custom', path="./runs/train/exp2/weights/best.pt")

"""inference settings"""
model.conf = 0.5 # NMS confidence threshold
model.iou = 0.45 # NMS IoU threshold
# model.cuda() # GPU
model.to(device)

"""image loader"""
image_dir = "./dataset/test/images/"
image_path = glob.glob(os.path.join(image_dir, "*.jpg"))
label_dict = {0: 'Maker-Name', 1: 'Established YearYear', 2: 'TypeWine Type', 3: 'VintageYear', 4: 'Appellation AOC DOC AVARegion',
            5: 'Distinct Logo', 6: 'AlcoholPercentage', 7: 'CountryCountry', 8: 'Appellation QualityLevel',
            9: 'Sweetness-Brut-SecSweetness-Brut-Sec', 10: 'Sustainable', 11: 'Organic'}

tree = ET.ElementTree() # tree 생성자
root = ET.Element("annotations") # 아래 for문 안에 넣으면 만들 매번 초기화되므로 여기에서 작성 | tag 작성

"""
<annotations>
</annotations>
"""

seen_count = 0

for img_path in image_path :
    # print(img_path)
    img = cv2.imread(img_path)

    # inference
    results = model(img, size=640)

    # results
    bbox = results.xyxy[0]
    # print(bbox)
    

    # image name
    image_name = os.path.basename(img_path)
    # print(image_name)
    

    # image width, height
    h, w, c = img.shape
    # print(h, w, c)

    
    # xml fix code
    xml_frame = ET.SubElement(root, "image", id="%d"%seen_count, name=image_name, width="%d"%w, height="%d"%h)
    # print(xml_frame)
    
    """
    <annotations>
        <image id="0" name="adit_mp4-1002_jpg.rf.5e4018e963af1251b3f7e6fd487c479e.jpg" width="640" height="480">
        </image>
    </annotations>
    """        

    for box in bbox :
        """
        <annotations>
            <image id="0" name="adit_mp4-1002_jpg.rf.5e4018e963af1251b3f7e6fd487c479e.jpg" width="640" height="480">
                <box label="car" occluded="0" source="manual" xtl="349.78" ytl="331.68" xbr="424.53" ybr="407.59" z_order="0"> </box>
            </image>
        </annotations>
        """     
        # box
        x1 = box[0].item()
        y1 = box[1].item()
        x2 = box[2].item()
        y2 = box[3].item()
        xtl = str(round(x1, 3))
        ytl = str(round(y1, 3))
        xbr = str(round(x2, 3))
        ybr = str(round(y2, 3))
        
        # class
        class_number = box[5].item()
        class_number_int = int(class_number)
        print(x1, x2, y1, y2, class_number)

        labels = label_dict[class_number_int]
        print(labels)


        # score number
        sc = box[4].item()
        print(sc)
    
        
        # bbox xml
        ET.SubElement(xml_frame, "box", label=labels, occluded="0", source="manual",
                        xtl=xtl, ytl=ytl, xbr=xbr, ybr=ybr, z_order="0")
    
    seen_count += 1

tree._setroot(root)
tree.write("test.xml", encoding="utf-8")