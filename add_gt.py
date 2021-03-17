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
    'rider_bicycle': 2,
    'rider_bike': 2, 
    'bicycle': -1, 
    'bike': -1, 
    '3-wheels': 2, 
    'sedan': 3,
    'van': 3, 
    'pickup_truck': 3, 
    'truck': 4, 
    'mixer_truck': 4, 
    'excavator': 4, 
    'forklift': 4, 
    'ladder_truck': 4, 
    'truck_etc': 4, 
    'vehicle_etc': 4, 
    'box_truck': 4, 
    'bus': 5, 
    'sitting_person': 1, 
    'ignored': -1,
    'rider' : 2,
    'car' : 3,
    'false_positive': 0, 
    'animal': 0,
    'bird' : 0,
    'animal_ignored':0,


    # LICENSE_PLATE = 1,


    'obstacle_cone' : 1,
    'obstacle_cylinder' : 2,
    'obstacle_drum' : 3,
    'parking_sign' : 4,
    'parking_cylinder' : 5,
    'parking_lock' : 6,
    'blocking_bar' : 7,
    'animal_ignored' : -5,
    'bird' : -5,
    'obstacle_ignored' : -1,
    'blocking_ignored' : -2,
    'parking_ignored': -3,
    'sod_ignored' : -4,


    'roadmark_stopline' : 1,
    'roadmark_arrow' : 2,
    'roadmark_speed' : 3,
    'roadmark_crosswalk' : 4,
    'roadmark__bump' : 5,
    'roadmark_triangle' : 6,
    'roadmark_diamond' : 7,
    'roadmark_ignored' : -1,
}

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
# parser.add_argument('-jpgs', required=True)
# parser.add_argument('-output', required=True)
# parser.add_argument('-type', required=False)

args = parser.parse_args()
# xml_type = args.type
# obj_name = args.name
# jpg_path = args.jpgs
main_folder = args.mf

xml_path = os.path.join(main_folder, "Annotations")
img_copy_path = os.path.join(main_folder, "images_annotations_with_gt")
img_folder_path = os.path.join(main_folder, "results/Images")
# print(img_copy_path)
# print(img_folder_path)

# single_file = r'C:\Users\YoseopKim\Desktop\Personal\OD_Work\Roadmark\roadmarktrain191002\Annotations\201706_hoo.kim_gopr1330.mp4_01190.xml'
if not os.path.exists(img_copy_path):
    os.mkdir(img_copy_path)
    
xml_names = os.listdir(xml_path)
img_names = os.listdir(img_folder_path)

xmlPaths = list(range(len(xml_names)))
imgPaths = list(range(len(img_names)))

index=0
for xml in xml_names:
    # if str(record)=="xml":
    #     continue
    xmlPaths[index] = os.path.join(xml_path , xml)
    index+=1

index=0
for jpg in img_names:
    # if str(record)=="xml":
    #     continue
    imgPaths[index] = os.path.join(img_folder_path , jpg)
    index+=1

parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
nonIgnoredCnt =0
for xml in xmlPaths:
    # print(xml)
    # print(os.path.basename(xml).rsplit('.',1)[0])
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    imgName =os.path.basename(xml).rsplit('.',1)[0]+'.jpg.result.jpg'
    # print(os.path.join(img_folder_path,os.path.basename(xml).rsplit('.',1)[0]+'.jpg.result.jpg'))
    image = cv2.imread(os.path.join(img_folder_path,imgName),cv2.IMREAD_COLOR)
    modified =1
    for obj in myroot.findall('object'):
        modified =1
        for name in obj.findall('name'):
            if('ignored' not in name.text and 'animal' not in name.text and 'bird' not in name.text and not('bike'== name.text) and 'false' not in name.text and not('bicycle' == name.text)):
                nonIgnoredCnt+=1
                modified =1
                xmin = int(float(obj[1][0].text))
                ymin = int(float(obj[1][1].text))
                xmax = int(float(obj[1][2].text))
                ymax = int(float(obj[1][3].text))
                # print(name.text)
                print_name = od_class[name.text]
                # print(ymin)
                # print(xmax)
                # print(ymax)
                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),1)
                # cv2.putText(image, "{}".format(print_name), ( min(int(xmin)+30, int(xmax)), int(ymin)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2 )
                cv2.putText(image, "[{}]".format(print_name), ( min(int(xmin)+30, int(xmax)), int(ymin)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2 )
            else:
                modified=1
                # print(name.text)
                print_name = od_class[name.text]
                xmin = int(float(obj[1][0].text))
                ymin = int(float(obj[1][1].text))
                xmax = int(float(obj[1][2].text))
                ymax = int(float(obj[1][3].text))
                # cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(161,146,137),1)
                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(161,146,137),1)
                cv2.putText(image, "[{}]".format(print_name), ( max(int(xmin)+10, int(xmax)), int(ymax)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2 )
                cv2.putText(image, "[{}]".format(print_name), ( max(int(xmin)+10, int(xmax)), int(ymax)), cv2.FONT_HERSHEY_PLAIN, 1, (161,146,137), 1 )
    if modified:
        cv2.imwrite(os.path.join(img_copy_path,imgName),image)
        print("{}/{}  {}".format(index,len(xml_names),os.path.join(img_copy_path,imgName)))
        modified=0
    index+=1
print(index)
print(nonIgnoredCnt)

    # index+=1