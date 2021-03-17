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
    # 'pedestrian': 1,
    # 'sedan': 3,
    # 'rider_bicycle': 2,
    # 'van': 3, 
    # 'rider_bike': 2,
    # 'rider': 2,
    # 'car':3,
    # 'truck_etc': 4, 
    # 'pickup_truck': 3, 
    # 'bike': -1, 
    # 'vehicle_etc': 4, 
    # 'box_truck': 4, 
    # 'bicycle': -1, 
    # 'false_positive': -2, 
    # 'bus': 5, 
    # 'sitting_person': -1, 
    # 'excavator': 4, 
    # 'mixer_truck': 4, 
    # 'forklift': 4, 
    # 'truck': 4, 
    # '3-wheels': 2, 
    # 'ladder_truck': 4, 
    # 'special_vehicle':4,
    # 'animal': 11,
    # 'ignored': -1,
    'pedestrian' : 1,
    'rider_bicycle' : 2,
    'rider_bike' : 3,
    'sedan' : 4,
    'van' : 5,
    'truck' : 6,
    'box_truck' : 7,
    'bus' : 8,
    'sitting_person' : 9,
    'ignored' : 10,
    'bicycle' : 11,
    'bike' : 12,
    '3-wheels' : 13,
    'pickup_truck' : 14,
    'mixer_truck' : 15,
    'excavator' : 16,
    'forklift' : 17,
    'ladder_truck' : 18,
    'truck_etc' : 19,
    'vehicle_etc' : 20,
    'false_positive' : 21,
    'animal' : 22,
    'bird' : 23,
    'animal_ignored' : 24,
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
    # 'obstacle_cone' : 1,
    # 'obstacle_cylinder' : 2,
    # 'obstacle_drum' : 3,
    # 'parking_sign' : 4,
    # 'parking_cylinder' : 5,
    # 'parking_lock' : 6,
    # 'blocking_bar' : 7,
    # 'animal_ignored' : -5,
    # 'bird' : -5,
    # 'obstacle_ignored' : -1,
    # 'blocking_ignored' : -2,
    # 'parking_ignored': -3,
    # 'sod_ignored' : -4,
    

    'roadmark_stopline' : 1,
    'roadmark_arrow' : 2,
    'roadmark_speed' : 3,
    'roadmark_crosswalk' : 4,
    'roadmark__bump' : 5,
    'roadmark_triangle' : 6,
    'roadmark_diamond' : 7,
    'roadmark_ignored' : 8,
    # 'roadmark_ignored' : -1,
}


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-cls', required=False)

args = parser.parse_args()
main_folder = args.mf
cls_name = args.cls

gt_count = {}



xml_path = os.path.join(main_folder, "Annotations")
xml_copy_path = os.path.join(main_folder, "for_gt_checker")

if not os.path.exists(xml_copy_path):
    os.mkdir(xml_copy_path)
    
xml_names = os.listdir(xml_path)

xmlPaths = list(range(len(xml_names)))

index=0
for xml in xml_names:
    xmlPaths[index] = os.path.join(xml_path , xml)
    index+=1


parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
found_cls=0
for xml in xmlPaths:
    # print(xml)
    # print(os.path.basename(xml).rsplit('.',1)[0])
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    newtxt = os.path.join(xml_copy_path,os.path.basename(xml).rsplit('.',1)[0]+'.txt')
    # print(os.path.join(img_folder_path,os.path.basename(xml).rsplit('.',1)[0]+'.jpg.result.jpg'))
    objCnt =0
    for obj in myroot.findall('object'):
        objCnt+=1
    with open(newtxt , "a") as file:
        file.write(str(objCnt) + '\n')
        for obj in myroot.findall('object'):
            for name in obj.findall('name'):
                    modified =1
                    xmin = float(obj[1][0].text)
                    ymin = float(obj[1][1].text)
                    xmax = float(obj[1][2].text)
                    ymax = float(obj[1][3].text)
                    if name.text in gt_count:
                        gt_count[name.text] +=1
                    else:
                        gt_count[name.text]=1
                    
                    cls_idx = od_class[(name.text).lower()]
                    # print(cls_idx)
                    # print(xmin)
                    # print(ymin)
                    # print(xmax)
                    # print(ymax)
                    file.write("{} {:.2f} {:.2f} {:.2f} {:.2f} \"\"\n".format(cls_idx, xmin, ymin, xmax, ymax))
        if modified:
            print(newtxt)
            modified=0
    index+=1
print("file cnt " + str(index))
# for x, y in gt_count.items():
total =0
for key, value in sorted(gt_count.items(), key=lambda item: item[0], reverse=False):
# for key, value in sorted(gt_count.items(), key=lambda item: item[1], reverse=True):
    total += value
    print("{} : {} ".format(key, value))
    # index+=1
print("total: {}".format(total))