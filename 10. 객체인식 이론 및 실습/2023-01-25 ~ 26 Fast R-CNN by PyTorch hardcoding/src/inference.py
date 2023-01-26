from config import TEST_DIR, CLASSES, DEVICE
from model import create_model
import glob, os, cv2, numpy as np, torch, copy


"""모델 호출? 선언?하기"""
model = create_model(num_classes=5).to(DEVICE)
model.load_state_dict(torch.load("../outputs/model100.pth", map_location=DEVICE)) # map_location 선언해서 쓰자
model.eval() # 평가 모드로 전환

"""이미지 불러오기"""
test_images = glob.glob(os.path.join(TEST_DIR, "*.jpg"))
# print(f"Test instances : {len(test_images)}")

"""임계값 설정하기"""
detection_threshold = 0.7


for i in range(len(test_images)) : # 이미지 갯수만큼 for문을 돌리자
    image_name = test_images[i].split('\\')[-1].split('.')[0] # 파일 이름 잘라서 가져오기
    # print(image_name)

    """이미지 읽기"""
    image = cv2.imread(test_images[i])
    # print(image)
    origin_image = image.copy()
    
    image = cv2.cvtColor(origin_image, cv2.COLOR_BGR2RGB).astype(np.float32) # BGR to RGB
    # cv2.imshow('test', image)
    # cv2.waitKey(0)

    image /= 255.0 # mask the pixel range between 0 and 1 --> normalize
    image = np.transpose(image, (2, 0, 1)).astype(np.float_) # bring color channels to front + np.float_으로 해야 적용되네?
                                                             # https://numpy.org/doc/stable/user/basics.types.html
    image = torch.tensor(image, dtype=torch.float).cuda() # convert to tensor + cuda로 보내기
    image = torch.unsqueeze(image, 0) # add batch dimentsion
    # print(image)

    with torch.no_grad() :
        outputs = model(image) # 예측값

    outputs = [{k : v.to('cpu') for k, v in t.items()} for t in outputs] # load all detection to cpu for further operations
    # print(outputs) # 여기까지는 threshold를 거치지 않은 상태

    if len(outputs[0]['boxes']) != 0 :
        boxes = outputs[0]['boxes'].data.numpy()
        scores = outputs[0]['scores'].data.numpy()
        # print("boxes >>> ", boxes, "scores >>> ", scores)
        boxes = boxes[scores >= detection_threshold].astype(np.int32) # filter out boxes according to 'detection_threshold'
        # print(boxes)
        draw_boxes = boxes.copy() # 그림 그릴 용으로 copy를 해두자

        pred_classes = [CLASSES[i] for i in outputs[0]['labels'].cpu().numpy()] # get all the predicted class names 
        # print(pred_classes)

        """바운딩 박스 그리기 + 최고 점수 class 이름 표기하기"""
        """draw the bounding boxes and write the class name on top of it"""
        for j, box in enumerate(draw_boxes) :
            cv2.rectangle(origin_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
            cv2.putText(origin_image, pred_classes[j], (int(box[0]), int(box[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(origin_image, str(scores[j]), (int(box[0]), int(box[1] - 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Prediction", origin_image)
        cv2.waitKey(0)
        os.makedirs("../test_result/", exist_ok=True)
        cv2.imwrite(f"../test_result/{image_name}.png", origin_image)
    
    print(f"Image {i + 1} done....")
    print("-" * 50)
print("평가 예측이 끝났습니다...")