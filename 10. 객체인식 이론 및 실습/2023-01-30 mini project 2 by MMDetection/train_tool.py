import torch, mmcv
from mmcv import Config
from mmdet.apis import init_detector, inference_detector, set_random_seed, train_detector
from mmdet.datasets.builder import DATASETS
from mmdet.datasets.coco import CocoDataset
from mmdet.datasets import build_dataset
from mmdet.models import build_detector
from mmcv.runner import get_dist_info, init_dist
from mmdet.utils import collect_env, get_root_logger, setup_multi_processes


"""Dataset Register"""
@DATASETS.register_module(force=True) # 강제로 클래스 정보 수정할 거기 때문에 넣음
class WineLabelsDataset(CocoDataset) : # 상속받는 건 CocoDataset | json 파일에 적힌 label(=class 정보)대로 입력하면 됨
                                       # mmdet\datasets\coco.py
    CLASSES = ('wine-labels', 'AlcoholPercentage', 'Appellation AOC DOC AVARegion', "Appellation QualityLevel", "CountryCountry", "Distinct Logo", "Established YearYear", "Maker-Name", "Organic", "Sustainable", "Sweetness-Brut-SecSweetness-Brut-Sec", "TypeWine Type", "VintageYear")


"""Config file"""
# cascade_rcnn(겁나 무거움), dynamic_rcnn, fast_rcnn, mask_rcnn(segmentation 할 때 씀) | 얘네를 좀 많이 씀
config_file = './configs/dynamic_rcnn/dynamic_rcnn_r50_fpn_1x_coco.py' # r50은 resnet50을 의미함
cfg = Config.fromfile(config_file) # 파일 읽어들이기
# print(cfg.pretty_text) # 해당 config file의 아키텍처 구조나 정보를 보고 싶을 때 사용


"""Learning Rate setting"""
# single GPU default --> 0.0025
cfg.optimizer.lr = 0.0025 # 0.02 / 8 : 1개의 GPU로 하는 거라서 8로 나눠줌. 원래 학습을 8개 GPU로 하기 때문


"""Dataset setting"""
cfg.dataset_type = 'WineLabelsDataset' # configs\_base_\datasets\coco_detection.py 참고
cfg.data_root = './dataset'


"""Train, Val, Test dataset의 type, data root, annotation file, img_prefix 설정"""
cfg.data.train.type = 'WineLabelsDataset' # train
cfg.data.train.ann_file = './dataset/train/_annotations.coco.json' # 이 파일을 읽고 처리해줘!
cfg.data.train.img_prefix = './dataset/train/' # 뒤에 알아서 train 붙을 거기 때문에 여기까지만 써주면 됨
cfg.data.val.type = 'WineLabelsDataset' # valid
cfg.data.val.ann_file = './dataset/valid/_annotations.coco.json'
cfg.data.val.img_prefix = './dataset/valid/'
cfg.data.test.type = 'WineLabelsDataset' # test
cfg.data.test.ann_file = './dataset/test/_annotations.coco.json'
cfg.data.test.img_prefix = './dataset/test/'

cfg.model.roi_head.bbox_head.num_classes = 13 # class number 수정하기 | models쪽 타고 넘어감
cfg.model.rpn_head.anchor_generator.scales = [4] # 작은 객체를 잡기 위해 anchor size를 변경할 것임 | default=8 --> 4
cfg.load_from = './dynamic_rcnn_r50_fpn_1x-62a3f276.pth' # pretrained-model pt파일 불러오기, 다운로드 받아서 넣어야 함
cfg.work_dir = './work_dirs/0130' # 학습한 모델 저장 경로 지정

cfg.lr_config.warmup = None # learning rate hyperparameter 설정
cfg.log_config.interval = 10 # 10번째마다 보여줘

'''[평가]COCO dataset evaluation type = bbox 지정''' # mAP로 놓는 경우도 있음
# mAP IoU threshold 0.5 ~ 0.95 변경하면서 측정
cfg.evaluation.metric = 'bbox'
cfg.evaluation.interval = 10 # 평가 몇 번에 한 번씩 할래? 보통 10번 정도마다 봄
cfg.checkpoint_config.interval = 10 # 모델 파일 중간 저장 몇 번에 한 번씩 할래?

cfg.runner.max_epochs = 88 # epoch 설정 | 기본값 : 8(GPU 갯수) x 12 = 96, 지금은 GPU 1개라 저렇게 설정
cfg.seed = 777 # 고정된 seed값 지정
cfg.data.samples_per_gpu = 6 # single GPU에서 통용되는 값 | batch_size라고 인식하면 됨
cfg.data.workers_per_gpu = 2 # num_workers, single GPU에서 통용되는 값 | 얘네는 거의 고정값
# print('cfg.data >>', cfg.data)

cfg.gpu_ids = range(1) # GPU 사용 갯수
cfg.device = 'cuda' # device 지정
set_random_seed(777, deterministic=False) # 고정된 seed값 지정
# print('cfg info show >>> ', cfg.pretty_text)

datasets = [build_dataset(cfg.data.train)] # train용 데이터를 생성하고 올리자
# print('datasets[0]', datasets[0])

datasets[0].__dict__.keys() # datasets[0].__dict__ variables key val

model = build_detector(cfg.model, train_cfg=cfg.get('train_cfg'), test_cfg=cfg.get('test_cfg'))
model.CLASSES = datasets[0].CLASSES
# print(model.CLASSES)

if __name__ == '__main__' : # 얘는 num_worker로 인한 이유인지 이런 방식으로 실행해야 함. ipynb에서 할거면 조건문 없이 실행
    train_detector(model, datasets, cfg, distributed=False, validate=True)