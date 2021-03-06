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

result_folder = os.path.join(main_folder, "FN_Analysis")
if not os.path.exists(result_folder):
    os.mkdir(result_folder)

fn_folders = os.listdir(fpfn_crop_path)
fp_folders = os.listdir(fpfn_crop_path)
# print(type(folder_names))
# print(cls_folders)

'''fp folders'''
# for folder in fp_folders:
#     if len(folder.rsplit('_'))>2:
#         fp_folders.remove(folder)
# for folder in fp_folders:
#     if folder.rsplit('_')[1] == fpfn:
#         fp_folders.remove(folder)
# print(fp_folders)

'''use <>_fn_full'''
for folder in fn_folders:
    if len(folder.rsplit('_'))>2:
        fn_folders.remove(folder)

for folder in fn_folders:
    if folder.rsplit('_')[1] != fpfn:
        fn_folders.remove(folder)

print(fn_folders)

fn_stats = {}
single_stat = {}
# fnGtCount=0
missingCnt =0 #number of GT in test DB that were not detected at all. Do not reset this for each ObjectClass. Otherwise when uploading to confluence page, there can be images with the same name despite belonging to different classes
              # and it will change the image with the same name.
confs =[] #list of detections found for a single FN. conf can be divided
confCnt =0
_IOU=0
box_fn= []
box_det= []
isTSL = 0
for folder in fn_folders: #loop through each cropped_fpfn folder
    fn_list = os.listdir(os.path.join(fpfn_crop_path,folder))
    fn_cls = folder.rsplit('_')[0].lower()
    if fn_cls == 'pedestrian':
        isTSL =0
        fn_cls = 'ped'
    elif fn_cls == 'tl':
        isTSL =1
        fn_cls = 'tl_car'
    elif fn_cls == 'tst':
        isTSL =1
        fn_cls = 'ts_t'
    elif fn_cls == 'tsr':
        isTSL =1
        fn_cls = 'ts_r'
    elif fn_cls == 'tsc':
        isTSL =1
        fn_cls = 'ts_c'
    else :
        isTSL =0

    print(fn_cls + "**************************************************************************************************************")
    new_img_path = os.path.join(result_folder,fn_cls+"_conf")
    if not os.path.exists(new_img_path):
        os.mkdir(new_img_path)
    for fn in fn_list: #loop through the list of images inside cropped_fpfn folders
        # fnGtCount+=1
        baseName = fn.rsplit('png')[0]
        fn_img_name = baseName + 'png'
        print(fn_img_name)
        xmin=float(fn.rsplit('png')[1].rsplit('_')[1]) #parse file name for the coordinates of fn
        ymin=float(fn.rsplit('png')[1].rsplit('_')[2])
        xmax=float(fn.rsplit('png')[1].rsplit('_')[3])
        ymax=float(fn.rsplit('png')[1].rsplit('_')[4][:-4])
        height_fn = ymax-ymin
        box_fn = [xmin,ymin,xmax,ymax] # box of FN image in question. FN bbox is Test GT bbox

        found_fn =False
        with open(det_file, "r") as file: #loop through every line of detection txt.
            for line in file:
                gt_jpgName = line.rsplit('/')[1].rsplit(' ')[0]
                # print(gt_jpgName)
                if fn_img_name == gt_jpgName : #only if the jpg names are identical we attempt looking at the IOU.
                    _IOU=0 #reset IOU var
                    det_cls =line.rsplit('/')[1].rsplit(' ')[1]
                    conf =float(line.rsplit('/')[1].rsplit(' ')[2])
                    xmin2=float(line.rsplit('/')[1].rsplit(' ')[3])
                    ymin2=float(line.rsplit('/')[1].rsplit(' ')[4])
                    xmax2=float(line.rsplit('/')[1].rsplit(' ')[5])
                    ymax2=float(line.rsplit('/')[1].rsplit(' ')[6])
                    box_det = [xmin2,ymin2,xmax2,ymax2]
                    _IOU = IOU(box_det,box_fn) #calculate the IOU between FN and Det Object of the same image.
                    # print(_IOU)

                    if _IOU>0.5:
                        confs.append([conf, det_cls, fn_img_name, box_fn, box_det, _IOU, height_fn]) #only if IOU is greater 0.5, we append to conf list
                        found_fn=True

        if found_fn:
            # print("BEFORE : {}".format(confs))
            confs = sorted(confs, key=lambda t : t[0], reverse=False) #sort the conf list
            # print("height is {}".format(confs[0][6]))

            # print("AFTER : {}".format(confs))
            # print("GT {} DET {}".format(fn_cls, confs[0][1]))

        #    '''here im trying to see if FN images with conf > 0.9 are actually in FP'''
            if float(confs[0][0])>=float(0.9) and fn_cls == confs[0][1].lower() : #if the detection result matching with FN has greater than 0.9 conf score, something is wrong
                print("**************************")
                print("GT {} DET {}".format(fn_cls, confs[0][1]))
                print("IOU IS : {:.3f}".format(float(confs[0][5])))
                print("SCORE IS : {:.5f}".format(float(confs[0][0])))
                print(confs[0][3])
                print(confs[0][4])
                print("**************************")
            image = cv2.imread(os.path.join(os.path.join(fpfn_crop_path,folder),fn)) #open image
            cv2.putText(image, "[{} -> {} {:.5f}]".format(fn_cls,confs[0][1],confs[0][0]),  (70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
            #for fn_full
            # cv2.putText(image, "[{} -> {} {:.5f}]".format(fn_cls,confs[0][1],confs[0][0]), (int(box_fn[0]+10), int(box_fn[1]+20)), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
            # cv2.rectangle(image,(int(confs[0][3][0]),int(confs[0][3][1])),(int(confs[0][3][2]),int(confs[0][3][3])),(0,0,255),1)
            # cv2.rectangle(image,(int(confs[0][4][0]),int(confs[0][4][1])),(int(confs[0][4][2]),int(confs[0][4][3])),(255,0,0),1)

            if float(confs[0][0])<float(0.9) and fn_cls.lower() == confs[0][1].lower(): #FN where conf score was not high enough but class was correct
                fn_category_folder = os.path.join(new_img_path, fn_cls)
                if not os.path.exists(fn_category_folder):
                    os.mkdir(fn_category_folder)
                cv2.imwrite(os.path.join(fn_category_folder,str(confs[0][0])+"_"+confs[0][2]+".jpg"),image) #save image

                if isTSL:
                    if height_fn <= 20 and height_fn > 10: 
                        if fn_cls+" Far" in single_stat:
                            single_stat[fn_cls+" Far"] +=1
                        else:
                            single_stat[fn_cls+" Far"] = 1
                        print(height_fn)
                    elif height_fn <= 30 and height_fn > 20:
                        if fn_cls+" Middle" in single_stat:
                            single_stat[fn_cls+" Middle"] +=1
                        else:
                            single_stat[fn_cls+" Middle"] = 1
                    else:
                        if fn_cls+" Near" in single_stat:
                            single_stat[fn_cls+" Near"] +=1
                        else:
                            single_stat[fn_cls+" Near"] = 1
                else:
                    if fn_cls in single_stat:
                        single_stat[fn_cls] +=1
                    else:
                        single_stat[fn_cls] = 1

            elif float(confs[0][0])>=float(0.9) and fn_cls.lower() == confs[0][1].lower(): #FN which has a det score higher than 0.9? Abnormality
                fn_category_folder = os.path.join(new_img_path, "ignore")
                if not os.path.exists(fn_category_folder):
                    os.mkdir(fn_category_folder)
                cv2.imwrite(os.path.join(fn_category_folder,str(confs[0][0])+"_"+confs[0][2]+".jpg"),image) #save image
                if "ignore" in single_stat:
                    single_stat["ignore"] +=1
                else:
                    single_stat["ignore"] = 1
            else: 
                fn_category_folder = os.path.join(new_img_path, confs[0][1].lower()) #FN where conf score was not high enough + class confusion
                print(confs[0][1].lower())
                if not os.path.exists(fn_category_folder):
                    os.mkdir(fn_category_folder)
                cv2.imwrite(os.path.join(fn_category_folder,str(confs[0][0])+"_"+confs[0][2]+".jpg"),image) #save image
                if confs[0][1].lower() in single_stat:
                    single_stat[confs[0][1].lower()] +=1
                else:
                    single_stat[confs[0][1].lower()] = 1
            confs=[]


        if not found_fn: #if fn is not found, most likely not detected at all

            fn_category_folder = os.path.join(new_img_path, "missing")
            if not os.path.exists(fn_category_folder):
                os.mkdir(fn_category_folder)
            if isTSL:
                if height_fn <= 20 and height_fn > 10: 
                    if fn_cls+" missing_Far" in single_stat:
                        single_stat[fn_cls+" missing_Far"] +=1
                    else:
                        single_stat[fn_cls+" missing_Far"] = 1
                elif height_fn <= 30 and height_fn > 20:
                    if fn_cls+" missing_Middle" in single_stat:
                        single_stat[fn_cls+" missing_Middle"] +=1
                    else:
                        single_stat[fn_cls+" missing_Middle"] = 1
                else:
                    if fn_cls+" missing_Near" in single_stat:
                        single_stat[fn_cls+" missing_Near"] +=1
                    else:
                        single_stat[fn_cls+" missing_Near"] = 1
            else:
                if 'missing' in single_stat:
                    single_stat['missing'] +=1
                else:
                    single_stat['missing'] = 1
            missingCnt+=1
            image = cv2.imread(os.path.join(os.path.join(fpfn_crop_path,folder),fn)) #open image
            h, w, c = image.shape
            cv2.putText(image, "[{} -> {} {:.2f}]".format(fn_cls,'n/a',0.00),  (70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
            #for fn_full
            # cv2.putText(image, "[{} -> {} {:.2f}]".format(fn_cls,'n/a',0.00),  (int(box_fn[0]+10), int(box_fn[1]+20)), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
        
            # cv2.imshow("new",image)
            # cv2.waitKey(0)
            # print(os.path.join(new_img_path,fn_img_name))
            cv2.imwrite(os.path.join(fn_category_folder,fn_img_name+"_"+str(missingCnt)+".jpg"),image) #save image to file

    fn_stats[fn_cls] = single_stat
    single_stat = {}


#PRINT STATISTICS
for cls in fn_folders:
    fn_cls = cls.rsplit('_')[0].lower()
    if fn_cls == "pedestrian":
        fn_cls = 'ped'
    if fn_cls == 'tl':
        fn_cls = 'tl_car'
    if fn_cls == 'tst':
        fn_cls = 'ts_t'
    if fn_cls == 'tsr':
        fn_cls = 'ts_r'
    if fn_cls == 'tsc':
        fn_cls = 'ts_c'
    print(fn_cls + " ***********************")
    for key, value in fn_stats[fn_cls].items():
        print("{} {}".format(key,value))
                    # print(fn_img_name)
                    # print(conf)
                    # print(xmin2)
                    # print(ymin2)
                    # print(xmax2)
                    # print(ymax2)