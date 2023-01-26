import torch
import cv2
import numpy as np
import os
import glob
from xml.etree import ElementTree as et
from config import CLASSES, RESIZE_TO, TRAIN_DIR, VALID_DIR, BATCH_SIZE
from torch.utils.data import Dataset, DataLoader
from utils import collate_fn, get_train_transform, get_valid_transform

"""the dataset class"""
class MicroControllerDataset(Dataset) :
    def __init__(self, dir_path, width, height, classes, transform=None) :
        self.dir_path = dir_path
        self.width = width
        self.height = height
        self.classes = classes
        self.transform = transform

        # get all the image paths in sorted order
        self.image_paths = glob.glob(f"{self.dir_path}/*.jpg")
        self.all_images = [image_path.split('\\')[-1] for image_path in self.image_paths]
        self.all_images = sorted(self.all_images)

    def __getitem__(self, idx) :
        # capture the image name and the full image path
        image_name = self.all_images[idx]
        image_path = os.path.join(self.dir_path, image_name)

        # read the image
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

        # get the height and width of the image
        image_width = image.shape[1]
        image_height = image.shape[0]

        for member in root.findall('object') :
            labels.append(self.classes.index(member.find('name').text))

            xmin = int(member.find('bondbox').find('xmin').text) # x min = left corner x-coordinates
            xmax = int(member.find('bondbox').find('xmax').text) # x max = right corner x-coordinates
            ymin = int(member.find('bondbox').find('ymin').text) # y min = left corner y-coordinates
            ymax = int(member.find('bondbox').find('ymax').text) # y max = right corner y-coordinates

            # resize the bounding boxes according to the...
            xmin_final = (xmin / image_width) * self.width
            xmax_final = (xmax / image_width) * self.width
            ymin_final = (ymin / image_height) * self.height
            ymax_final = (ymax / image_height) * self.height

            boxes.append([xmin_final, ymin_final, xmax_final, ymax_final])

    def __len__(self) :
        pass