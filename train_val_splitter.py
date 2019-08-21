import os
import random
from collections import defaultdict

annot_fps = [
'/media/dh/DATA4TB/Datasets/SGMaritimeDataset/VIS_Onboard_annot.txt',
'/media/dh/DATA4TB/Datasets/SGMaritimeDataset/VIS_Onshore_annot.txt',
'/media/dh/DATA4TB/Datasets/SGMaritimeDataset/NIR_annot.txt',
            ]

out_train = '/media/dh/DATA4TB/Datasets/SGMaritimeDataset/SMD_train.txt'
out_val = '/media/dh/DATA4TB/Datasets/SGMaritimeDataset/SMD_val.txt'
train_split = 0.8

train_strs = []
val_strs = []
total_train_vid = 0
total_train_img = 0
total_val_img = 0
total_val_vid = 0
for annot_fp in annot_fps:
    with open(annot_fp,'r') as f:
        lines = f.readlines()

    frames_dict = defaultdict(list)
    for line in lines:
        split = line.strip().replace(';','').split()
        img_name = split[0]
        assert '_frame_' in img_name
        vid_basename = img_name.split('_frame_')[0]
        frames_dict[vid_basename].append(line)

    vid_names = list(frames_dict.keys())
    val_target = max(1, round((1-train_split)*len(vid_names))) # at least want 1 vid to be in validation set
    random.shuffle(vid_names)

    train_vid_count = 0
    train_img_count = 0
    val_img_count = 0
    val_vid_count = 0
    for vidname in vid_names[:val_target]:
        val_strs.extend(frames_dict[vidname])
        val_vid_count += 1
        val_img_count += len(frames_dict[vidname])
    for vidname in vid_names[val_target:]:
        train_strs.extend(frames_dict[vidname])
        train_vid_count += 1
        train_img_count += len(frames_dict[vidname])
    
    print(os.path.basename(annot_fp))
    print('\tTrain: {} frames from {} videos'.format(train_img_count, train_vid_count))
    print('\tVal: {} frames from {} videos'.format(val_img_count, val_vid_count))
    total_train_img += train_img_count
    total_train_vid += train_vid_count
    total_val_img += val_img_count
    total_val_vid += val_vid_count

with open(out_train,'w') as f:
    f.writelines(train_strs)
with open(out_val,'w') as f:
    f.writelines(val_strs)

print('Combined')
print('\tTrain: {} frames from {} videos'.format(total_train_img, total_train_vid))
print('\tVal: {} frames from {} videos'.format(total_val_img, total_val_vid))

        # im = Image.open(img_path)
        # iw, ih = im.size
        # bbs = split[1:]
        # #x_min,y_min,x_max,y_max,class_id
        # txt_strs = []
        # is_too_big = False
        # for bb in bbs:
        #     x_min, y_min, x_max, y_max, class_id = [int(x) for x in bb.split(',')]

        #     w = x_max - x_min + 1
        #     h = y_max - y_min + 1
        #     cx = x_min + w/2 - 1
        #     cy = y_min + h/2 - 1
            
        #     ncx = cx / iw
        #     ncy = cy / ih
        #     nw = w / iw
        #     nh = h / ih

        #     if nh > max_height:
        #         is_too_big = True
        #         break

        #     txt_strs.append('{} {} {} {} {}\n'.format(class_id, ncx, ncy, nw, nh))

        # img_basename = os.path.basename(img_path)
        # basename = img_basename.split('.')[0]



