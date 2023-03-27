from ultralytics import YOLO

# ultralytics\yolo\cfg\default.yaml에서 config 값 수정
# ultralytics\yolo\data\augment.py에서 augmentation 값 수정(560번째 줄 가면 T = [] 있다)

"""아래 주소에 있는 파일 확인하고 돌릴 것"""
# datasets\data.yaml
# ultralytics\yolo\data\augment.py
# ultralytics\yolo\cfg\default.yaml

if __name__ == '__main__':
    # Load a model
    model = YOLO("yolov8l.yaml")  # build a new model from scratch
    model = YOLO("./runs/detect/train3/weights/best.pt")  # load a pretrained model (recommended for training)

    # Use the model 
    # 다양한 cfg 값은 https://docs.ultralytics.com/cfg/ 참고 
    # model.train(task="detect", data="datasets/data.yaml", optimizer='AdamW', lr0=0.001, batch=16, epochs=300, device=0)  # train the model
    model.val()
    metrics = model.val()  # evaluate model performance on the validation set
    # Validate the model
    metrics.box.map    # mAP50-95
    metrics.box.map50  # mAP50
    metrics.box.map75  # mAP75
    metrics.box.maps   # a list contains mAP50-95 of each category