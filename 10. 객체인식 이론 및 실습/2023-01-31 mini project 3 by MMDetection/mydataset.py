import copy, cv2
import os.path as osp
import mmcv
import numpy as np
from mmdet.datasets.builder import DATASETS
from mmdet.datasets.custom import CustomDataset


@DATASETS.register_module()
class KittiTinyDataset(CustomDataset) : 
    CLASSES = ('Car', 'Pedestrian', 'Cyclist')

    def load_annotations(self, ann_file): 
        cat2label = {k : i for i, k in enumerate(self.CLASSES)} # 만들어낸 라벨
        # print(cat2label)

        image_list = mmcv.list_from_file(self.ann_file) # load image list from file

        data_infos = []
        for image_id in image_list :
            filename = '{0:}/{1:}.jpeg'.format(self.img_prefix, image_id) # 원본 이미지 데이터를 가져오기

            image = cv2.imread(filename) # image width and height 읽을 용도
            height, width = image.shape[:2] # 이 뒤에껀 이미지 채널수

            data_info = {'filename' : str(image_id) + '.jpeg', 'width' : width, 'height' : height}

            label_prefix = self.img_prefix.replace('image_2', 'label_2') # annotation sub dir prefix 반환

            lines = mmcv.list_from_file(osp.join(label_prefix, str(image_id) + '.txt')) # annotation file read 1 line

            content = [line.strip().split('') for line in lines]
            bbox_name = [x[0] for x in content]
            bboxes = [[float(info) for info in x[4:8]] for x in content] # bbox save | bounding box의 값들을 뽑아냄

            gt_bboxes = [] # 정답지
            gt_labels = [] # 정답지
            gt_bboxes_ignore = []
            gt_labels_ignore = []

            for bbox_name, bbox in zip(bbox_name, bboxes) :
                if bbox_name in cat2label : # 라벨에 있는 거랑 일치하면
                    gt_labels.append(cat2label[bbox_name])
                    gt_bboxes.append(bbox)
                else : # 그 외
                    gt_labels_ignore.append(-1)
                    gt_bboxes_ignore.append(bbox)
            
            data_anno = dict(bboxes = np.array(gt_bboxes, dtype=np.float32).reshape(-1, 4),
                            labels = np.array(gt_labels, dtype=np.long),
                            bboxes_ignore = np.array(gt_bboxes_ignore, dtype=np.float32).reshape(-1, 4),
                            labels_ignore = np.array(gt_labels_ignore, dtype=np.long))
            data_info.update(data_anno)
            data_infos.append(data_info)

        return data_infos


# test = KittiTinyDataset()
# test.load_annotations()