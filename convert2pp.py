import os
import scipy.io
from collections import defaultdict

# annot_dir = '/media/dh/Data/SGMaritimeDataset/VIS_Onshore/ObjectGT'
# img_dir = '/media/dh/Data/SGMaritimeDataset/VIS_Onshore/Imgs'
# out_filepath = '/media/dh/Data/SGMaritimeDataset/VIS_Onshore_annot.txt'

# annot_dir = '/media/dh/Data/SGMaritimeDataset/VIS_Onboard/ObjectGT'
# img_dir = '/media/dh/Data/SGMaritimeDataset/VIS_Onboard/Imgs'
# out_filepath = '/media/dh/Data/SGMaritimeDataset/VIS_Onboard_annot.txt'

annot_dir = '/media/dh/Data/SGMaritimeDataset/NIR/ObjectGT'
img_dir = '/media/dh/Data/SGMaritimeDataset/NIR/Imgs'
out_filepath = '/media/dh/Data/SGMaritimeDataset/NIR_annot.txt'


wanted_indices = [1,3,4,5,6,7] # Ferry, Vessel/ship, Speed boat, Boat, Kayak, Sail boat

'''
One row for one image;
Row format: image_file_path box1 box2 ... boxN;
Box format: x_min,y_min,x_max,y_max,class_id (no space). Unnormalized. One class ships only whose index is 0
'''

image_names = [name for name in os.listdir(img_dir) if name.endswith('.png')]

img_dict = defaultdict(list)
img_count = 0
for imname in os.listdir(img_dir):
    basename = '_'.join(imname.split('_')[:2])
    frame_num = int(imname.split('frame_')[-1].split('.')[0])
    img_dict[basename].append((frame_num, imname))
    img_count+=1

annot_strings = []
bb_count = 0
img_count = 0
annot_basenames = []
for annot_name in os.listdir(annot_dir):
    if annot_name.endswith('_ObjectGT.mat'):
        basename = '_'.join(annot_name.split('_')[:2])
        mat = scipy.io.loadmat(os.path.join(annot_dir, annot_name))
        annots = mat['structXML'].flatten()
        annot_basenames.append(basename)
        for frame_num, imname in img_dict[basename]:
            img_count += 1
            annot_string = '{}'.format(imname)
            bbs = annots[frame_num][-1]
            classes = annots[frame_num][1].flatten()
            positive = False
            for bb, label in zip(bbs, classes):
                if label in wanted_indices:
                    positive = True
                    x,y, w, h = bb
                    x_min = int(round(x))
                    y_min = int(round(y))
                    x_max = int(round(x+w-1))
                    y_max = int(round(y+h-1))
                    annot_string += ' {},{},{},{},0'.format(x_min, y_min, x_max, y_max)
                    bb_count+=1
            if positive:
                annot_string+=';\n'
                annot_strings.append(annot_string)
                print(annot_string.replace('\n',''))
            else:
                print('{} [Not a positive frame]'.format(imname))

print('Num of annotated sets: {}/{}'.format(len(set(annot_basenames)), len(set(img_dict.keys()))))
print('Sets without annotations: {}'.format(set(img_dict.keys())-set(annot_basenames)))
print('Total annotated images in this set: {}'.format(len(annot_strings)))
print('Total annotated bbs in this set: {}'.format(bb_count))
with open(out_filepath, 'w') as f:
    f.writelines(annot_strings)
