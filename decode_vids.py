import os
import cv2


video_dir = '/home/levan/Datasets/SGMaritimeDataset/VIS_Onshore/Videos'
out_img_dir = '/home/levan/Datasets/SGMaritimeDataset/VIS_Onshore/Imgs'
samplePerSec = 1 

for vid in os.listdir(video_dir):
    basename = vid.replace('_VIS.avi','')
    print(basename)
    cap = cv2.VideoCapture(os.path.join(video_dir, vid))
    fps = cap.get(5)
    frameskip = fps // samplePerSec
    assert cap.isOpened(),'video not opened'
    framecount = -1
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        framecount+=1
        if framecount%frameskip == 0:
            img_name = '{}_frame_{}.png'.format(basename, framecount)
            print(img_name)
            cv2.imwrite(os.path.join(out_img_dir, img_name), frame)