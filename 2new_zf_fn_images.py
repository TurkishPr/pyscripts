'''
WHAT IT DOES
tells you which class and with what conf you got your FN.
and also prints it on the cropped fn images
ex: car -> bus .87

WHAT YOU NEED
run evaluate_svnet.py and download the detection files of each class.
and also get cropped fpfn images
Prepare them as shown below!

    FOLDER Hierarchy
    [Main Folder]
    -> [fpfn_crop]
    -> [detection_txt]

HOW IT WORKS
*give main directory as -mf and fp/fn as -fpfn
1. it reads the coordinates of FN from the name of the fpfn cropped image.
2. it searches the detection files of each class for coordinates that have a match. (IOU)
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
detection_txt_path = os.path.join(main_folder,"detection_txt2")
fpfn_crop_path = os.path.join(main_folder,"fpfn_crop")
det_files = os.listdir(detection_txt_path)
cls_folders = os.listdir(fpfn_crop_path)
# print(type(folder_names))
for folder in cls_folders:
    # print(folder)
    # print(folder.rsplit('_')[1])
    if folder.rsplit('_')[1]!=fpfn:
        cls_folders.remove(folder)

print(cls_folders)

fn_stats = {}
single_stat = {}
fnGtCount=0
missingCnt =0
confs =[] #list of detections found for a single FN. conf can be divided
confCnt =0

for folder in cls_folders: #loop through each Cls_fn/fp folder
    fn_list = os.listdir(os.path.join(fpfn_crop_path,folder))
    gt_cls = folder.rsplit('_')[0].lower()
    if gt_cls == 'pedestrian':
        gt_cls = 'ped'
    print("GT CLASS : {}".format(gt_cls))
    new_img_path = os.path.join(main_folder,gt_cls+"_conf2")
    if not os.path.exists(new_img_path):
        os.mkdir(new_img_path)
    for fn in fn_list: #loop through each fn
        fnGtCount+=1
        baseName = fn.rsplit('jpg')[0]
        gt_jpgName = baseName + 'jpg'
        print(gt_jpgName)
        # print(fn)
        # txtName = baseName + 'txt'
        # xml_final_path = os.path.join(os.path.join(cls_fn_gt_xml_path,"Annotations"),txtName)
        xmin=float(fn.rsplit('jpg')[1].rsplit('_')[1]) #parse file name for the coordinates of fn
        ymin=float(fn.rsplit('jpg')[1].rsplit('_')[2])
        xmax=float(fn.rsplit('jpg')[1].rsplit('_')[3])
        ymax=float(fn.rsplit('jpg')[1].rsplit('_')[4][:-1])
        box_gt = [xmin,ymin,xmax,ymax]
        # print(box_gt)
        found_fn =False
        for det_file in det_files: #loop through det_files and find the fn
            # print(det_file)
            fn_cls = det_file.rsplit(".")[0]
            if fn_cls == 'pedestrian':
                fn_cls = 'ped'
            # print("FN CLASS : {}".format(fn_cls))

            det_file = os.path.join(detection_txt_path, det_file)
            with open(det_file, "r") as file:
                for line in file:
                    fn_img_name = line.rsplit('/')[1].rsplit(' ')[0]
                    # print(fn_img_name)
                    conf =float(line.rsplit('/')[1].rsplit(' ')[1]) 
                    xmin2=float(line.rsplit('/')[1].rsplit(' ')[2])
                    ymin2=float(line.rsplit('/')[1].rsplit(' ')[3])
                    xmax2=float(line.rsplit('/')[1].rsplit(' ')[4])
                    ymax2=float(line.rsplit('/')[1].rsplit(' ')[5])
                    box_fn = [xmin2,ymin2,xmax2,ymax2]
                    _IOU = IOU(box_gt,box_fn)
                    if fn_img_name == gt_jpgName and _IOU>0.5:
                        confs.append([conf, fn_cls, fn_img_name])

                        # print(line[:-1])
                        # print(fn_cls)
                        print(_IOU)
                        # print("\n")
                        # image = cv2.imread(os.path.join(os.path.join(fpfn_crop_path,folder),fn)) #open image
                        # h, w, c = image.shape
                        # cv2.putText(image, "[{} -> {} {:.2f}]".format(gt_cls,fn_cls,conf),  (70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
                        # cv2.imshow("new",image)
                        # cv2.waitKey(0)
                        # print(os.path.join(new_img_path,fn_img_name))
                        # cv2.imwrite(os.path.join(new_img_path,fn_img_name[:-4]+"_"+str(conf)+".jpg"),image) #save image to file

                        #for 통계


                        found_fn=True

                #     if found_fn:
                #         break
                # if found_fn:
                #     file.close()
        if found_fn:
            confs = sorted(confs, key=lambda t : t[0], reverse=True)
            print(confs)
            image = cv2.imread(os.path.join(os.path.join(fpfn_crop_path,folder),fn)) #open image
            cv2.putText(image, "[{} -> {} {:.2f}]".format(gt_cls,confs[0][1],confs[0][0]),  (70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
            cv2.imwrite(os.path.join(new_img_path,confs[0][2]+"_"+str(confs[0][0])+".jpg"),image) #save image to file
            
            if gt_cls.lower() == confs[0][1].lower(): #conf가 낮은 경우
                if gt_cls in single_stat:
                    single_stat[gt_cls] +=1
                else:
                    single_stat[gt_cls] = 1
                    
            else: # 다른 cls가 더 conf가 높은 경우
                if confs[0][1].lower() in single_stat:
                    single_stat[confs[0][1].lower()] +=1
                else:
                    single_stat[confs[0][1].lower()] = 1
            confs=[]


        if not found_fn: #if fn is not found, meaning it is most likely not detected at all. Pretty sure :/
            print("Found No Matching Detection Result")
            if 'missing' in single_stat:
                single_stat['missing'] +=1
            else:
                single_stat['missing'] = 1
            missingCnt+=1
            image = cv2.imread(os.path.join(os.path.join(fpfn_crop_path,folder),fn)) #open image
            h, w, c = image.shape
            cv2.putText(image, "[{} -> {} {:.2f}]".format(gt_cls,'n/a',0.00),  (70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
            # cv2.imshow("new",image)
            # cv2.waitKey(0)
            # print(os.path.join(new_img_path,fn_img_name))
            cv2.imwrite(os.path.join(new_img_path,gt_jpgName[:-4]+"_"+str(missingCnt)+".jpg"),image) #save image to file

    fn_stats[gt_cls] = single_stat
    single_stat = {}
# print("TL ***********************")
# for key, value in fn_stats['TL'].items():
#     print("{} {}".format(key,value))

    # print(fn_stats)
for cls in cls_folders:
    gt_cls = cls.rsplit('_')[0].lower()
    if gt_cls == "pedestrian":
        gt_cls = 'ped'
    print(gt_cls + " ***********************")
    for key, value in fn_stats[gt_cls].items():
        print("{} {}".format(key,value))
                    # print(fn_img_name)
                    # print(conf)
                    # print(xmin2)
                    # print(ymin2)
                    # print(xmax2)
                    # print(ymax2)