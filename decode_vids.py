import os
import cv2

video_dir = '/media/dh/Data/SGMaritimeDataset/NIR/Videos'
out_img_dir = '/media/dh/Data/SGMaritimeDataset/NIR/Imgs'
samplePerSec = 1 

print('Sampling videos in {} at {} frame per second'.format(video_dir, samplePerSec))

if not os.path.isdir(out_img_dir):
    os.makedirs(out_img_dir)
assert os.path.isdir(out_img_dir),'out_img_dir is not a directory!'

for vid in os.listdir(video_dir):
    basename = '_'.join(vid.split('_')[:2])
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