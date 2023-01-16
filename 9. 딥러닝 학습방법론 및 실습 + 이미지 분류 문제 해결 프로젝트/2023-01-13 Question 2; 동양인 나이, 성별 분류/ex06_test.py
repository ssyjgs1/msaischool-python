import os
import cv2
import glob
import torch    
import torch.nn as nn
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from torch.utils.data import DataLoader
from ex04_customdataset import CustomDataset
from torchvision import models
from ex05_main import model_try

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def test_main():
    test_aug = A.Compose([
        A.CenterCrop(width= 200, height= 200),
        A.Normalize(mean=(0.485, 0.456, 0.406), std= (0.229, 0.224, 0.225)),
        ToTensorV2()
    ])

    test_dataset = CustomDataset("./dataset/test" , transform= test_aug)
    test_loader  = DataLoader(test_dataset, batch_size= 1, shuffle= False, num_workers= 2, pin_memory= True)

    ###### 모델에 따라 수정 필요 !!!!
    # model = models.__dict__["resnet50"](pretrained= True)
    # model.fc = nn.Linear(in_features = 2048, out_features = 6)
    # model.load_state_dict(torch.load(f'./0116/best_{model_try}.pt', map_location=device))
    # model.to(device)

    model = models.__dict__["vgg16"](pretrained=False)
    model.classifier[6] = nn.Linear(in_features= 4096, out_features=6)
    model.load_state_dict(torch.load("./experiment result/best_1.pt", map_location=device))
    model.to(device)

    test(model, test_loader, device)  # 테스트 진행할때 실행 : 정확도 출력
    print('====================================================================================')
    # test_show(test_loader, device)  # 틀린 label 이미지 확인하고 싶을 때 진행 : 사진 비교

def acc_function(correct, total) :
    acc = correct / total * 100
    return acc

def test(model, data_loader, device) :
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for i, (image, label, path) in enumerate(data_loader) :
            images, labels = image.to(device), label.to(device)
            output = model(images)
            _, argmax = torch.max(output, 1)
            total += images.size(0)
            correct += (labels == argmax).sum().item()
        acc = acc_function(correct, total)
        print(f"acc >> {acc}%" )

def test_show(test_loader, device) :
    model = models.__dict__["vgg16"](pretrained=False)
    model.classifier[6] = nn.Linear(in_features= 4096, out_features=6)
    model.load_state_dict(torch.load("./experiment result/best_2.pt", map_location=device))
    model.to(device)

    test_data_path = "./dataset/test"
    label_dict = folder_name_det(test_data_path)

    correct = 0
    total = 0
    model.eval()
    with torch.no_grad() :
        for i, (imgs, labels, path) in enumerate(test_loader) :
            inputs, outputs, paths = imgs.to(device), labels.to(device), path      
            predicted_outputs = model(inputs)            
            _, predicted = torch.max(predicted_outputs, 1) # 제일 확률 높은 답안지 내놔라

            # total += images.size(0)
            # correct += (labels == argmax).sum().item()

            labels_temp = labels.item()
            labels_pr_temp = predicted.item()

            predicted_label = label_dict[str(labels_pr_temp)]
            answer_label = label_dict[str(labels_temp)]
        
            img = cv2.imread(paths[0])
            if(answer_label != predicted_label):  # label과 predicted output이 다를 경우멘 사진출력
                print('Name of Label\t:', paths[0].split('\\')[1])
                print('Name of Image\t:', paths[0].split('\\')[2])
                print("Answer Label\t:" , answer_label)
                print("Predicted Label\t:", predicted_label)
                cv2.putText(img, predicted_label, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2) # 예상 답안 : 초록색
                cv2.putText(img, answer_label, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)    # 실제 답안 : 빨간색
                cv2.imshow("test", img)
                cv2.waitKey(0)

        # acc = acc_function(correct, total)
        # print(f"model accuracy >> {acc}%" )

def folder_name_det(folder_path) :
    folder_name = glob.glob(os.path.join(folder_path,"*"))
    det = {}
    for index, (path) in enumerate(folder_name) :
        temp_name = path.split("\\")
        temp_name = temp_name[1]
        det[str(index)] = temp_name
    return det          

if __name__ == '__main__':
    test_main()