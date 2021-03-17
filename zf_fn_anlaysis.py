#! python3
import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from lxml import etree as ET
od_class = {
    'pedestrian': 1,
    'sedan': 3,
    'rider_bicycle': 2,
    'van': 3,
    'sedan':3, 
    'rider_bike': 2,
    'rider': 2,
    'car':3,
    'truck_etc': 4, 
    'pickup_truck': 3, 
    'bike': -1, 
    'vehicle_etc': 4, 
    'box_truck': 4, 
    'bicycle': -1, 
    'false_positive': -2, 
    'bus': 5, 
    'sitting_person': -1, 
    'excavator': 4, 
    'mixer_truck': 4, 
    'forklift': 4, 
    'truck': 4, 
    '3-wheels': 2, 
    'ladder_truck': 4, 
    'special_vehicle':4,
    'animal': 11,
    'ignored': -1,

    # LICENSE_PLATE = 1,
    'obstacle_cone' : 1,
    'obstacle_cylinder' : 2,
    'obstacle_drum' : 3,
    'parking_sign' : 6,
    'parking_cylinder' : 5,
    'parking_lock' : 7,
    'blocking_bar' : 9,
    'animal_ignored' : 13,
    'bird' : 12,
    'obstacle_ignored' : 4,
    'blocking_ignored' : 10,
    'parking_ignored': 8,
    'sod_ignored' : 14,
      

    'roadmark_stopline' : 1,
    'roadmark_arrow' : 2,
    'roadmark_speed' : 3,
    'roadmark_crosswalk' : 4,
    'roadmark__bump' : 5,
    'roadmark_triangle' : 6,
    'roadmark_diamond' : 7,
    'roadmark_ignored' : 8,
    'tl' : 9,
    'tsc': 6, 
    'tsr':8,
    'tst':7,
}


'''receive and parse arguments'''
parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
# parser.add_argument('-cls', required=False)
parser.add_argument('-fpfn', required=True)

args = parser.parse_args()
main_folder = args.mf
obj_name = args.cls
fpfn = args.fpfn
workingFolder = main_folder.rsplit('\\',1)[0]
# print(os.path.join(main_folder.rsplit('\\',1)[0],'for_gt_checker'))
copy_path = os.path.join(workingFolder,'fn_gt_xml')
JPEGPath = os.path.join(workingFolder,'JPEGImages')
if not os.path.exists(copy_path):
    os.mkdir(copy_path)

if fpfn == None:
    print("you did not specify either fp or fn")
# else: 
#     print(fpfn)

'''erase the other category that is NOT desired'''
folder_names = os.listdir(main_folder)
# print(type(folder_names))
for folder in folder_names:
    # print(folder)
    # print(folder.rsplit('_')[1])
    if folder.rsplit('_')[1]!=fpfn:
        folder_names.remove(folder)

'''
from either FP or FN folders we now create xml files
to be used for od_gt_checker
'''
filecount=0
fnGtCount=0
for folder in folder_names:
    cls_idx = od_class[(folder.rsplit('_')[0]).lower()]
    cls_fn_gt_xml_path = os.path.join(copy_path,folder.rsplit('_')[0])
    if not os.path.exists(cls_fn_gt_xml_path):
        os.mkdir(cls_fn_gt_xml_path)
    if not os.path.exists(os.path.join(cls_fn_gt_xml_path,"JPEGImages")):
        os.mkdir(os.path.join(cls_fn_gt_xml_path,"JPEGImages"))
    if not os.path.exists(os.path.join(cls_fn_gt_xml_path,"Annotations")):
        os.mkdir(os.path.join(cls_fn_gt_xml_path,"Annotations"))
    fn_list = os.listdir(os.path.join(main_folder,folder))
      
    for fn in fn_list:
        fnGtCount+=1
        baseName = fn.rsplit('jpg')[0]
        jpgName = baseName + 'jpg'
        txtName = baseName + 'txt'
        xml_final_path = os.path.join(os.path.join(cls_fn_gt_xml_path,"Annotations"),txtName)
        xmin=float(fn.rsplit('jpg')[1].rsplit('_')[1])
        ymin=float(fn.rsplit('jpg')[1].rsplit('_')[2])
        xmax=float(fn.rsplit('jpg')[1].rsplit('_')[3])
        ymax=float(fn.rsplit('jpg')[1].rsplit('_')[4][:-1])
        if os.path.exists(xml_final_path):
            # print(baseName)
            # print("file exists")
            with open(xml_final_path, "r") as file:
                count = int(file.readline())+1 #gt count
                restOfFile = file.read()
                # print(count)
                # print(restOfFile)
            with open(xml_final_path, "w+") as file:
                file.write(str(count)+"\n")
                file.write(restOfFile)
                file.write("{} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(cls_idx, xmin, ymin, xmax, ymax))
        else:
            filecount+=1
            shutil.copy(os.path.join(JPEGPath,jpgName), os.path.join(os.path.join(cls_fn_gt_xml_path,"JPEGImages"), jpgName))
            with open(xml_final_path, "w") as file:
                file.write("1\n")
                file.write("{} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(cls_idx, xmin, ymin, xmax, ymax))
    print((folder.rsplit('_')[0]).lower() + " file cnt : " + str(filecount))
    print((folder.rsplit('_')[0]).lower() + " gt cnt : " + str(fnGtCount))
    filecount=0
    fnGtCount=0



# os.path.join(main_folder, )