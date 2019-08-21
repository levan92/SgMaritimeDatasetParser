import os

context = '/media/dh/DATA4TB/Datasets/SGMaritimeDataset/'
annot_file = '/media/dh/DATA4TB/Datasets/SGMaritimeDataset/SMD_train.txt'
# contexted_annot_file = '/media/dh/DATA4TB/Datasets/SGMaritimeDataset/VIS_Onshore_annot.txt'
contexted_annot_file = annot_file.replace('.txt','_contexted.txt')
assert not os.path.exists(contexted_annot_file)

assert os.path.exists(annot_file),'Annotation txt file does not exist'
assert os.path.isdir(context),'Directory given is not a directory'

with open(annot_file,'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    splits = line.split()
    img_name = splits[0]

    if 'NIR' in img_name:
        set_name = 'NIR'
    elif 'VIS_OB' in img_name:
        set_name = 'VIS_Onboard'
    else:
        set_name = 'VIS_Onshore'

    rest = splits[1:]
    img_path = os.path.join(*[context, set_name, 'Imgs', img_name])
    assert os.path.exists(img_path),'Image {} does not exists!'.format(img_path)
    rest.insert(0, img_path)
    newline = ' '.join(rest)
    print(newline)
    new_lines.append(newline+'\n')

with open(contexted_annot_file,'w') as f:
    f.writelines(new_lines)
