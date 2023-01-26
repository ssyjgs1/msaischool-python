import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


def create_model(num_classes) : # pre-trained를 사용할 거기 때문에 class 갯수를 바꿔줘야 함
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True) # Faster RCNN pre-trained model 불러오기
    # print(model) # FastRCNNPredictor - in_features, out_features 바꿔줘야 함

    '''입력 features의 갯수를 구해보자(get the number of input features)'''
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # print(in_features) # 1024
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    # print(model) # (cls_score): Linear(in_features=1024, out_features=3, bias=True)
    return model