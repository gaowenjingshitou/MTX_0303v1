import torch
import os, glob
import random, csv
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from PIL import ImageFilter
import re
import pandas  as pd
import numpy  as np
import random
import seaborn as sns
import matplotlib.pyplot as plt


def load_csv(root, filename):
    name2label = {}  # "sq...":0

    for name in sorted(os.listdir(os.path.join(root)), reverse=True):

        if not os.path.isdir(os.path.join(root, name)):
            print("不是目录", os.path.join(root, name))
            continue
        elif os.path.exists(os.path.join(root, '.ipynb_checkpoints')):
            os.removedirs(os.path.join(root, '.ipynb_checkpoints'))
        name2label[name] = len(name2label.keys())
    print("name2label", name2label)

    if not os.path.exists(os.path.join(root, filename)):
        print("文件{}不存在".format(filename))
        images = []
        for name in name2label.keys():
            print("name", name)
            # 'pokemon\\mewtwo\\00001.png

            images += glob.glob(os.path.join(root, name, '*.png'))

        # 1167, 'pokemon\\bulbasaur\\00000000.png'
        print('len(images)', len(images))

        random.shuffle(images)

        # NONEC_NEC0921_X_Inhosp = pd.read_excel("NONEC_NEC0921_X_Inhosp.xls", converters={"EXAM_NO": str})
        NONEC_NEC0921_X_Inhosp = pd.read_excel("NONEC_NEC0921_X_InhospV3.xlsx",
                                               converters={"EXAM_NO": str})  # 20201114注释掉

        NONEC_NEC0921_X_Inhosp = NONEC_NEC0921_X_Inhosp.set_index("EXAM_NO")  # 20201114注释掉

        # images_csv1_remain_again_NEC_NONEC_index=pd.read_csv("images_csv1_remain_again_NEC_NONEC_index.csv",index_col=0,converters={"EXAM_NO": str})
        #         images_csv1_remain_again_NEC_NONEC_index=pd.read_csv("images_csv1_remain_again_NEC_NONEC_index.csv",converters={"EXAM_NO": str})
        #         images_csv1_remain_again_NEC_NONEC_index=images_csv1_remain_again_NEC_NONEC_index.set_index("EXAM_NO")

        with open(os.path.join(root, filename), mode='w', newline='') as f:
            writer = csv.writer(f)
            for img in images:  # 'pokemon\\bulbasaur\\00000000.png'  /workspace/NEW_DATA_1020/NONEC/0005068972.png  /workspace/NEW_DATA_1020/NONEC/0001572670_0.png
                # print("******img*******", img)
                img1 = img.split("/")[-1].split(".")[0]
                if img1.find("_"):
                    # print('img1_find',img1)
                    img1 = img.split("/")[-1].split(".")[0].split("_")[0]
                    # print("******img1_split**********", img1)

                if img1 in NONEC_NEC0921_X_Inhosp.index:
                    # print("EXAM_NO",img1)
                    name = img.split(os.sep)[-2]

                    Inhosp_No = NONEC_NEC0921_X_Inhosp.loc[img1, 'Inhosp_No']

                    # print('name',name)
                label = name2label[name]
                # print("label",label)
                # 'pokemon\\bulbasaur\\00000000.png', 0
                writer.writerow([Inhosp_No, img1, img, label])
            print('writen into csv file:', filename)


    else:

        print("文件{}已经存在".format(filename))


def main():
    load_csv(root='/workspace/NEW_DATA_1020', filename="images.csv")

    images_csv1 = pd.read_csv(os.path.join('/workspace/NEW_DATA_1020', 'images.csv'),
                              names=['Inhosp_No', 'EXAM_NO', 'img', 'label'],
                              converters={"EXAM_NO": str}, index_col=0)

    train_val_index = random.sample(list(set(images_csv1.index)), int(0.9* len(list(set(images_csv1.index)))))
    train_index = random.sample(list(set(train_val_index)), int(0.8 * len(list(set(train_val_index)))))

    val_index = list(set(train_val_index).difference(set(train_index)))

    test_index = list(set(images_csv1.index).difference(set(train_val_index)))

    print("train_val_index", len(train_val_index))
    print("train_index", len(train_index))

    print("val_index", len(val_index))
    print("test_index", len(test_index))

    print("共{}人".format(len(train_index) + len(val_index) + len(test_index)))
    train_data = images_csv1.loc[train_index, :]

    #train_data.to_csv("train_data.csv")

    print(train_data.shape)
    val_data = images_csv1.loc[val_index, :]
    #val_data.to_csv("val_data.csv")
    print(val_data.shape)
    test_data = images_csv1.loc[test_index, :]
    #test_data.to_csv("test_data.csv")
    print(test_data.shape)