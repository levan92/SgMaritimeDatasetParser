import os

annot_dir = '/home/levan/Datasets/SGMaritimeDataset/VIS_Onshore/ObjectGT'

for annot_name in os.listdir(annot_dir):
    if annot_name.endswith('_ObjectGT.mat'):
        print(annot_name)
        basename = annot_name.replace('_ObjectGT.mat','')
        print(basename)
        img_name = basename+''



'''
One row for one image;
Row format: image_file_path box1 box2 ... boxN;
Box format: x_min,y_min,x_max,y_max,class_id (no space). Unnormalized. One class ships only whose index is 0
'''