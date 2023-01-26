import torch
import cv2


# Device Setting
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# 모델 정의
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./runs/train/exp5/weights/best.pt') # 앞 2개의 키워드는 공통
# print(model) # 모델 생겨먹은 모양 확인


# Inference Settings
model.conf = 0.5 # NMS confidence threshold | 예측한 클래스 점수 --> 0.5 이상인 애들만 박스 그림(임계값과 유사하다고 생각하면 됨)
model.iou = 0.45 # NMS IoU threshold | 겹침 정도 얼마나 허용할래?(0.45에서 거의 건드리지 않음)


"""Device Settings"""
# model.cpu() # cpu로 모델 동작함
# model.cuda() # gpu로 모델 동작함
model.to(device) # device = torch.device(0)


"""이미지 1장 호출"""
image_path = "./dataset/test/images/adit_mp4-164_jpg.rf.9091363d9ae472c294ed1b57b838693f.jpg"


"""이미지 읽기"""
img1 = cv2.imread(image_path) # opencv image BGR to RGB 따로 할 필요 없이 그냥 돌리면 됨
# img2 = cv2.imread(image_path)[..., ::-1]


"""label dictionary"""
label_dict = {0 : "big bus", 1 : "big truck", 2 : "bus-l-", 3 : "bus-s-", 4 : "car",
5 : "mid truck", 6 : "small bus", 7 : "small truck", 8 : "truck-l-", 9 : "truck-m-", 
10 : "truck-s-", 11 : "truck-xl-"}


"""Inference"""
results = model(img1, size=640)
# results = model([img1, img2], size=640) # 배치로 묶어서 돌릴 땐 이거 사용
# print(results.print())
# print(results.xyxy)
bbox = results.xyxy[0]
for bbox_info in bbox : # bounding box 정보 뽑기
    # print(bbox_info)
    x1 = bbox_info[0].item()
    y1 = bbox_info[1].item()
    x2 = bbox_info[2].item()
    y2 = bbox_info[3].item()
    sc = bbox_info[4].item() # score
    label_number = bbox_info[5].item()
    label = label_dict[int(label_number)]
    # print(x1, y1, x2, y2, sc, label)

    """image size h w c"""
    h, w, c = img1.shape
    # print(h, w, c)

    """xyxy to yolo center_x, center_y, w, h"""
    center_x = round(((x1 + x2) / 2) / w, 6)
    # print(center_x)
    center_y = round(((y1 + y2) / 2) / h, 6)
    yolo_w = round((x2 - x1) / w, 6)
    yolo_h = round((y2 - y1) / h, 6)
    # print(int(label_number), center_x, center_y, yolo_w, yolo_h)

    """yolo center_x, center_y, w, h --> text file save"""
    with open(f"./adit_mp4-164_jpg.rf.9091363d9ae472c294ed1b57b838693f.txt", 'a') as f :
        f.write(f"{int(label_number)} {center_x} {center_y} {yolo_w} {yolo_h} \n")
    

    img1 = cv2.putText(img1, label, (int(x1), int(y1-10)), cv2.FONT_HERSHEY_PLAIN, color=(255, 0, 0), fontScale=1.5)
    ret = cv2.rectangle(img1, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

cv2.imshow("test", ret)
cv2.waitKey(0)