import os, glob, cv2
from xml.etree.ElementTree import parse


xml_dir = "./wine labels_voc_dataset"
class voc_to_yolo_converter() :
    def __init__(self, xml_paths) : # xml 파일 경로를 받아와야 하니까 인자로 넣자
        self.xml_path_lish = glob.glob(os.path.join(xml_paths, "*.xml"))
        # print(self.xml_path_lish)

    def voc_xyxy_show(self, x1, y1, x2, y2, label_name, file_name) : # ?????
        image_path = os.path.join("./wine labels_voc_dataset", file_name)
        image = cv2.imread(image_path)
        img_rect = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # cv2.imshow("test", image)
        # cv2.waitKey(1)
        return img_rect

    def get_voc_to_yolo(self) :
        for xml_path in self.xml_path_lish :
            # print(xml_path)
            tree = parse(xml_path) # 불러와서 읽고 parse를 하자
            root = tree.getroot() # <annotations> | 이 밑은 root.findall('ㅁㅁ')로 해서 접근하면 된다

            file_name = root.find('filename')

            size_meta = root.findall('size') # get image size
            img_width = int(size_meta[0].find('width').text)
            img_height = int(size_meta[0].find('height').text)
            # print(img_width, img_height)

            object_metas = root.findall('object') # get object meta
            for object_meta in object_metas : # get box info
                object_label = object_meta.find('name').text # label name | <object><name>

                """bounding box 값을 찾아주자"""
                xmin = object_meta.find('bndbox').findtext('xmin')
                xmax = object_meta.find('bndbox').findtext('xmax')
                ymin = object_meta.find('bndbox').findtext('ymin')
                ymax = object_meta.find('bndbox').findtext('ymax')
                # print(object_label, xmin, xmax, ymin, ymax)

                # img_rect = self.voc_xyxy_show(xmin, ymin, xmax, ymax, object_label, file_name)

                """voc to yolo 변환 공식 = normalization"""
                yolo_x = round(((int(xmin) + int(xmax)) / 2) / img_width, 6)
                yolo_y = round(((int(ymin) + int(ymax)) / 2) / img_height, 6)
                yolo_w = round((int(xmax) - int(xmin)) / img_width)
                yolo_h = round((int(ymax) - int(ymin)) / img_height)
                # print(yolo_x, yolo_y, yolo_w, yolo_h)


"""디버깅용"""
if __name__ == "__main__" :
    test = voc_to_yolo_converter(xml_dir)
    test.get_voc_to_yolo()