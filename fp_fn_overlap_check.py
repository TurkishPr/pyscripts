'''
                                ***   WHAT IT DOES  ***
FN can happen when an object is detected as another class, commonly known as class confusion.
But, the conf score has to be less than .9 because, otherwise, it would become an FP.

So this script tells you which class and with what conf an FN occured.
This information is also printed on the cropped FN images
ex: car -> bus .87

                                ***  WHAT YOU NEED  ***
run ZF_object_prediction.exe and download the detection files of each class.
The local branch R5_ZF_FN_Analysis contains the code.
and also get cropped fpfn images

Prepare Required Data As Shown Below ****

    FOLDER Hierarchy
    [Main Folder]
    -> [fpfn_crop]
       -> bus_fn
       -> car_fn
       ...
    -> [detection_txt]
       -> det.txt

                                   ***  HOW IT WORKS  ***
*give main directory as -mf and fp/fn as -fpfn
1. it reads the coordinates of FN from the name of the fpfn cropped image.
2. it searches the detection file for coordinates that have a match. (IOU > 0.5)
3. when found it prints [gt class] -> [fn class] [conf] onto the image
'''

import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageOps

def IOU(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


od_class = {
    'ped': 1,
    'rider':2,
    'car':3, 
    'truck':4,
    'bus':5,
    'TSC':6,
    'TST':7,
    'TSR':8,
    'TL':9,
    '0':0,
    'TS_etc':12,
    'TL_etc':13,
    'TS_fa':14,
    'TL_fa':15,
}

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-fpfn', required=True)
args = parser.parse_args()
main_folder = args.mf
fpfn = args.fpfn

'''erase the other category(fp or fn) that is NOT desired'''
detection_txt_path = os.path.join(main_folder,"detection_txt")
fpfn_crop_path = os.path.join(main_folder,"fpfn_crop")
det_file = os.path.join(detection_txt_path,"only_obj.txt")
fn_full_folders = os.listdir(fpfn_crop_path)
fp_folders = os.listdir(fpfn_crop_path)
# print(type(folder_names))
# print(cls_folders)

'''fp folders'''
for folder in fp_folders:
    if len(folder.rsplit('_'))>2:
        fp_folders.remove(folder)

for folder in fp_folders:
    if folder.rsplit('_')[1] == fpfn:
        fp_folders.remove(folder)

print(fp_folders)

'''use <>_fn_full'''
for folder in fn_full_folders:
    if len(folder.rsplit('_'))<3:
        fn_full_folders.remove(folder)

for folder in fn_full_folders:
    if folder.rsplit('_')[1] != fpfn:
        fn_full_folders.remove(folder)


print(fn_full_folders)

fn_stats = {}
single_stat = {}
fnGtCount=0
missingCnt =0
confs =[] #list of detections found for a single FN. conf can be divided
confCnt =0
_IOU=0
box_fn= []
box_det= []
for folder in fn_full_folders: #loop through each cropped_fpfn folder
    fn_list = os.listdir(os.path.join(fpfn_crop_path,folder))
    fn_cls = folder.rsplit('_')[0].lower()
    if fn_cls == 'pedestrian':
        fn_cls = 'ped'
    print(fn_cls + "**************************************************************************************************************")
    new_img_path = os.path.join(main_folder,fn_cls+"_conf")
    if not os.path.exists(new_img_path):
        os.mkdir(new_img_path)
    for fn in fn_list: #loop through the list of images inside cropped_fpfn folders
        fnGtCount+=1
        baseName = fn.rsplit('jpg')[0]
        fn_img_name = baseName + 'jpg'

        for folder in fp_folders: #loop through each cropped_fpfn folder
            fp_list = os.listdir(os.path.join(fpfn_crop_path,folder))
            fp_cls = folder.rsplit('_')[0].lower()
            if fp_cls == 'pedestrian':
                fp_cls = 'ped'
            for fp in fp_list: #loop through the list of images inside cropped_fpfn folders
                baseName = fp.rsplit('jpg')[0]
                fp_img_name = baseName + "jpg"
                # print(fn)
                # print(fp)
                # print("\n")

                if fn_img_name == fp_img_name:
                    print("same img exists ")
                    print(fn)
                    print(fp)
                    print("\n")
                    if fn == fp :
                        print("BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEP")

