import cv2, json, os, glob, numpy as np
from mmdet.apis import inference_detector, init_detector, set_random_seed
from mmdet.datasets import build_dataset, DATASETS
from mmdet.models import build_detector
from mmdet.datasets.coco import CocoDataset
from mmcv import Config
"""COCO Dataset 기준으로 봤을 때 기본 구조"""

"""Config 설정(train과 동일함)"""

"""Dynamic RCNN 설정"""
config_file = './configs/dynamic_rcnn/dynamic_rcnn_r50_fpn_1x_coco.py'
cfg = Config.fromfile(config_file) # cfg라는 변수 선언해주고 쭉 다뤄나간다


"""DATASETS.register_module로 등록"""
@DATASETS.register_module(force=True)
class WineLabelsDataset(CocoDataset) : # 상속받는 건 CocoDataset | json 파일에 적힌 label(=class 정보)대로 입력하면 됨
                                       # mmdet\datasets\coco.py | 번호로 들어가기 때문에 한글로 클래스 입력해도 동작한다
    CLASSES = ('cat', 'chicken', 'cow', 'dog', 'fox', 'goat', 'horse', 'person', 'racoon','skunk')


"""dataset 설정"""
cfg.dataset_type = 'AnimalDataset' # configs\_base_\datasets\coco_detection.py 참고
cfg.data_root = './animals.v2-release.coco'


"""Train, Valid and Test dataset의 type, data_root, ann_file, img_prefix 등 하이퍼파라미터 지정"""
cfg.data.train.type = 'AnimalDataset' # train
cfg.data.train.ann_file = './animals.v2-release.coco/train/_annotations.coco.json'
cfg.data.train.img_prefix = './animals.v2-release.coco/train/' # 뒤에 알아서 train 붙을 거기 때문에 여기까지만 써주면 됨
cfg.data.val.type = 'AnimalDataset' # valid
cfg.data.val.ann_file = './animals.v2-release.coco/valid/_annotations.coco.json'
cfg.data.val.img_prefix = './animals.v2-release.coco/valid/'
cfg.data.test.type = 'AnimalDataset' # test
cfg.data.test.ann_file = './animals.v2-release.coco/test/_annotations.coco.json'
cfg.data.test.img_prefix = './animals.v2-release.coco/test/'

cfg.model.roi_head.bbox_head.num_classes = 10 # 모델에 들어가는 클래스 갯수 수정. resnet 계열이 대체로 roi_head 부분에서 설정함
cfg.load_from = './dynamic_rcnn_r50_fpn_1x-62a3f276.pth' # Pretrained model의 아키텍처 불러오기
cfg.work_dir = './0131' # weight file save directory 설정

cfg.lr_config.warmup = None # train 하이퍼파라미터 설정
cfg.log_config.interval = 10


"""[평가]COCO dataset evaluation type = bbox 지정"""
# VOC 데이터 같은 경우에는 mAP로 놓는 경우도 있음
# mAP IoU threshold 0.5 ~ 0.95 변경하면서 측정
cfg.evaluation.metric = 'bbox'
cfg.evaluation.interval = 10
cfg.checkpoint_config.interval = 10

cfg.runner.max_epochs = 10 # epoch 설정. test라서 10회 정도로만 설정
cfg.seed = 0 # 고정된 seed값 지정
cfg.gpu_ids = range(1)
set_random_seed(0, deterministic=False)

checkpoint_file = './work_dirs/0131_animal/latest.pth' # 평가에 사용할(=학습에 사용했던) 모델을 불러오자
model = init_detector(cfg, checkpoint_file, device='cuda') # train에 사용했던 정보로 해야한다


"""한 장의 이미지에 대해서 결과를 보고 싶다면?"""
# from mmdet.apis import show_result_pyplot # 필요한 라이브러리 불러오기
# img = './animals.v2-release.coco/test/9_jpg.rf.bca7063b1ce4c9c9b8f10c2fdfd6736d.jpg' # 보려는 이미지 아무거나 1장 경로 지정
# images = cv2.imread(img) # 이미지를 cv2로 읽어준다
# results = inference_detector(model, images) # 읽은 이미지랑 모델을 inference_detector에 던져준다
# show_result_pyplot(model, img, results) # 불러온 라이브러리에다가 인자들을 던져준다. 그러면 결과가 그림으로 나옴

"""json파일에서 이미지 이름과 각종 정보들을 뽑아내자"""
img_info_path = './animals.v2-release.coco/test/_annotations.coco.json' 
with open(img_info_path, 'r', encoding='utf-8') as f :
    image_info = json.loads(f.read())
# print(image_info)

"""임계값 설정"""
score_threshold = 0.7


"""JSON을 만들기 위해 빈 리스트 선언"""
submission_anno = list()

"""이미지를 한 개씩 순회하면서 inference를 보는 구간"""
for img_info in image_info['images'] : # json 데이터 상위에 위치
    # print(img_info) # {'id': 629, 'license': 1, 'file_name': 'tjwcg1wtrukphohufrun_jpg.rf.f0ce477d819ddff197254ed8ed070923.jpg', 'height': 712, 'width': 767, 'date_captured': '2022-08-30T09:49:53+00:00'}
    
    file_name = img_info['file_name'] # json - images - file_name
    img_width = img_info['width'] # json - images - width
    img_height = img_info['height'] # json - images - height
    # print(file_name, img_width, img_height) # kcx3xqc9cxd61axefwgv_jpg.rf.03a85546c8ffe0a266ed771579c77429.jpg 480 310
    
    img_path = os.path.join('./animals.v2-release.coco/test/', file_name) # 입력한 경로 안의 파일을 보자
    # print(img_path) # ./dataset/test/kcx3xqc9cxd61axefwgv_jpg.rf.03a85546c8ffe0a266ed771579c77429.jpg
    
    image = cv2.imread(img_path)
    image_copy = image.copy() # 원본이랑 비교해보게 복사를 해두자
    image_resize = cv2.resize(image_copy, (960, 540)) # 위에서 복사해둔 걸 리사이즈

    '''scale 구하기'''
    x_scale = float(960) / img_width
    y_scale = float(540) / img_height
    # print(x_scale, y_scale) # 1.125 3.096774193548387
    
    results = inference_detector(model, img_path) # 이미지 경로로 넣어도 동작함(내부적으로 처리가 되어 있는 듯)
    for number, result in enumerate(results) :
        if len(result) == 0 : # 이미지 내용(?)이 없다면(=object detect된 게 없으면)
            continue # 그냥 진행
        category_id = number + 1
        result_filtered = result[np.where(result[:, 4] > score_threshold)] # threshold 설정 : score_threshold보다 높은 것(=bounding box)만 뽑게 필터링
        if len(result_filtered) == 0 : # bounding box 잡힌 게 없다면?
            continue # GPU 아까우니 종료해라 or 다음 꺼로 넘어가라
            
        for i in range(len(result_filtered)) : # 0.5 이상으로 살아남은 애들에 대해서는 하나씩 좌표를 뽑아보자
            # print(result_filtered) # [[], []] --> [0][0], [0][1] 이중으로 된 list임

            tmp_dict = dict() # json은 dict 형태라 하나 만들어주자
            x_min = int(result_filtered[i, 0])
            y_min = int(result_filtered[i, 1])
            x_max = int(result_filtered[i, 2])
            y_max = int(result_filtered[i, 3])
            # print(x_min, y_min, x_max, y_max)

            '''xyxy --> xywh로 변환'''
            json_x = x_min
            json_y = y_min
            json_w = x_max - x_min
            json_h = y_max - y_min
            # print(json_x, json_y, json_w, json_h).
            
            '''JSON 정보를 작성'''
            tmp_dict['bbox'] = [json_x, json_y, json_w, json_h]
            tmp_dict['category_id'] = category_id
            tmp_dict['area'] = json_w * json_h # 해당하는 box의 면적 --> 너무 작으면 학습해도 의미가 없어서 제외하는 용도
            tmp_dict['image_id'] = img_info['id']
            tmp_dict['score'] = float(result_filtered[i, 4])
            submission_anno.append(tmp_dict)

            '''scale bbox - 해당하는 scale(비율)로 변환'''
            x1 = int(x_min * x_scale)
            y1 = int(y_min * y_scale)
            x2 = int(x_max * x_scale)
            y2 = int(y_max * y_scale)
            cv2.rectangle(image_resize, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)
    cv2.imshow('test', image_resize)
    # cv2.imshow('test', image)
    if cv2.waitKey() == ord('q') : # q 입력하면 종료
        exit()

    '''위에서 작성한 정보들로 json 파일을 작성해서 생성'''
    with open('./test_animal.json', 'w', encoding='utf-8') as f :
        json.dump(submission_anno, f, indent=4, sort_keys=True, ensure_ascii=False)