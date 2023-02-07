import cv2
vidcap = cv2.VideoCapture('The Wonderful World of Flying (HD) - Wolfe Air Reel by 3DF (RoKeSWzZAwA).mp4') ## 다운받은 비디오 이름 
success,image = vidcap.read()
count = 0

while(vidcap.isOpened()):
    ret, image = vidcap.read()
    
    if count == 9999999999999999999999999 : # 종료 시점 
        break

    if(int(vidcap.get(1)) % 10 == 0): # n 프레임당 저장 
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("frame%d.jpg" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1