import torch
import cv2
import numpy as np
import os
import glob
from xml.etree import ElementTree as et
from config import CLASSES, RESIZE_TO, TRAIN_DIR, VALID_DIR, BATCH_SIZE, NUM_SAMPLES_TO_VISUALIZE # 상수 불러오기
from torch.utils.data import Dataset, DataLoader
from utils import collate_fn, get_train_transform, get_valid_transform # 함수 불러오기

"""the dataset class"""
class MicrocontrollerDataset(Dataset):
    def __init__(self, dir_path, width, height, classes, transform=None):
        self.dir_path = dir_path
        self.width = width
        self.height = height
        self.classes = classes
        self.transform = transform
        # print(dir_path, self.dir_path)

        # get all the image paths in sorted order
        self.image_paths = glob.glob(f"{self.dir_path}/*.jpg")
        # print(self.image_paths)
        self.all_images = [image_path.split('/')[-1] for image_path in self.image_paths]
        self.all_images = sorted(self.all_images)
        # print(self.all_images)

    def __getitem__(self, idx) :
        # capture the image name and the full image path
        image_name = self.all_images[idx]
        image_name = os.path.basename(image_name)
        # print("image_name", image_name)
        image_path = os.path.join(self.dir_path, image_name)
        # print(image_path)

        # 이미지 읽어오기
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) #convert BGR to RGB color format and change type
        image_resized = cv2.resize(image, (self.width, self.height)) # resize for the required size
        image_resized /= 255.0 # normalization

        # capture the corresponding xml file for getting the annotations
        annot_filename = image_name[:-4] + '.xml'
        annot_file_path = os.path.join(self.dir_path, annot_filename)

        boxes = []
        labels = []
        tree = et.parse(annot_file_path)
        root = tree.getroot()

        # 이미지의 너비, 높이를 구해보자(get the height and width of the image)
        image_width = image.shape[1]
        image_height = image.shape[0]

        for member in root.findall('object') :
            labels.append(self.classes.index(member.find('name').text))

            xmin = int(member.find('bndbox').find('xmin').text) # x min = left corner x-coordinates
            xmax = int(member.find('bndbox').find('xmax').text) # x max = right corner x-coordinates
            ymin = int(member.find('bndbox').find('ymin').text) # y min = left corner y-coordinates
            ymax = int(member.find('bndbox').find('ymax').text) # y max = right corner y-coordinates

            # resize the bounding boxes according to the...
            xmin_final = (xmin / image_width) * self.width
            xmax_final = (xmax / image_width) * self.width
            ymin_final = (ymin / image_height) * self.height
            ymax_final = (ymax / image_height) * self.height

            boxes.append([xmin_final, ymin_final, xmax_final, ymax_final])
        
        # bounding box를 tensor로 바꿔주자
        boxes = torch.as_tensor(boxes, dtype=torch.float32)

        # bounding box의 구역을 구해주자(area of bounding boxes)
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((boxes.shape[0], ), dtype=torch.int64) # 얘는 보통 0으로 만든다. COCO 포맷에서 어떻게 쓸건지?를 물어본다는 듯
        
        # label을 tensor로 바꿔주자
        labels = torch.as_tensor(labels, dtype=torch.int64)

        # target dict를 만들어주자
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["area"] = area
        target["iscrowd"] = iscrowd
        image_id = torch.tensor([idx]) # idx로 image_id를 뽑아오자
        target["image_id"] = image_id

        # 이미지에 transforms를 적용해주자
        if self.transform : # if self.transform is True :
            sample = self.transform(image=image_resized, bboxes=target['boxes'], labels=labels)
            image_resized = sample['image']
            target['boxes'] = torch.Tensor(sample['bboxes'])
        
        return image_resized, target

    def __len__(self) :
        return len(self.all_images) # 전체 이미지의 길이 반환


"""데이터셋과 데이터로더를 준비해보자(prepare the final datasets and dataloaders)"""
# dataset
train_dataset = MicrocontrollerDataset(TRAIN_DIR, RESIZE_TO, RESIZE_TO, CLASSES, get_train_transform()) # width, height 2개 받아야 해서 RESIZE_TO를 2번 받음
valid_dataset = MicrocontrollerDataset(VALID_DIR, RESIZE_TO, RESIZE_TO, CLASSES, get_valid_transform()) # width, height 2개 받아야 해서 RESIZE_TO를 2번 받음
# for j in train_dataset : print(j) # 잘 나오나 디버깅을 해보자 | 실행 경로 문제가 있었음
# for i in valid_dataset : print(i) # 잘 나오나 디버깅을 해보자 | cd src --> python datasets.py로 해야 돌아갔음

# dataloader
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, collate_fn=collate_fn)
valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, collate_fn=collate_fn)
# print(f"Number of training samples : {len(train_dataset)}")
# print(f"Number of validation samples : {len(valid_dataset)}")


"""아래 실행문은 모델 학습 시에는 실행되면 안 되므로 주석 처리함"""
"""실행문"""
# if __name__ == "__main__" :
#     dataset = MicrocontrollerDataset(TRAIN_DIR, RESIZE_TO, RESIZE_TO, CLASSES) # transforms를 먹이지 않으려고 여기서 dataset을 별도로 선언
#     # print(f"Number of training images : {len(dataset)}")

#     '''이미지 샘플을 시각화하는 함수(function to visualize a single sample)'''
#     def visualize_sample(image, target) :
#         box = target['boxes'][0]
#         # print(target['labels'])
#         label = CLASSES[target['labels']]
#         cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
#         cv2.putText(image, label, (int(box[0]), int(box[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#         cv2.imshow("Image", image)
#         cv2.waitKey(0)

#     for i in range(NUM_SAMPLES_TO_VISUALIZE) :
#         image, target = dataset[i]
#         visualize_sample(image, target)