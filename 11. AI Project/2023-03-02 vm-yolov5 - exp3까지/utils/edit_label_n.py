import os 
import glob 
import shutil 

path = './dataset/valid/labels' #path of labels
labels = os.listdir(path)
for x in labels:
    with open(path+'/'+x) as f:
        lines = f.read().splitlines()
        for y in lines:
            index = int(y[:1])
            if index>5:
                print(x)