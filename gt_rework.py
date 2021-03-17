#! python3
'''
Reworking GT for pedestrians as an effort to reduce FPs

Removing all GT that are smaller than
36 in height
or
7 in width

SO keeping all ped GT that are larger than or equal to
37 in height
and
8 in width
'''
import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from lxml import etree as ET

height = 80

main_folder = r'C:\Users\Yoseop\Desktop\Personal\OD_Work\FA\GODTrain190131_Movon'
anno_folder = os.path.join(main_folder,"Annotations")
img_copy_path = os.path.join( main_folder, "JPEGImages_gt_filtered")
anno_copy_path = os.path.join( main_folder, "Annotations_{}".format(height))
img_folder_path = os.path.join(main_folder, "JPEGImages")
if not os.path.exists(img_copy_path):
    os.mkdir(img_copy_path)
if not os.path.exists(anno_copy_path):
    os.mkdir(anno_copy_path)
    

xml_names = os.listdir(anno_folder)
img_names = os.listdir(img_folder_path)
xmlPaths = list(range(len(xml_names)))
imgPaths = list(range(len(img_names)))

index=0
for xml in xml_names:
    xmlPaths[index] = os.path.join(anno_folder , xml)
    index+=1

index=0
for jpg in img_names:
    imgPaths[index] = os.path.join(img_folder_path , jpg)
    index+=1

Ped_Erased =0
Ped_Kept =0

'''parse each xml file'''
parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
erased=0
for xml in xmlPaths:
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    image = cv2.imread(imgPaths[index],cv2.IMREAD_COLOR)
    print(index)
    for obj in myroot.findall('object'):   
        for name in obj.findall('name'):
            if(name.text=='pedestrian'):
                modified =1
                xmin = int(float(obj[1][0].text))
                ymin = int(float(obj[1][1].text))
                xmax = int(float(obj[1][2].text))
                ymax = int(float(obj[1][3].text))
                if ((ymax-ymin)>height): #and (xmax-xmin)>8):
                    # print(xml)
                    cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(102,255,51),1)
                    # print(ymax-ymin)
                    Ped_Kept+=1
                    # print("Ped Kept " + str(Ped_Kept))

                if not((ymax-ymin)>height): #and (xmax-xmin)>8):
                    cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(102, 51, 255),2)
                    Ped_Erased+=1
                    erased=1
                    # print("Ped Erased " + str(Ped_Erased))
                    # print(xml)
                    obj.remove(name)

    if modified and erased:
        cv2.imwrite(os.path.join(img_copy_path,img_names[index]),image)
        modified=0
        erased=0
    mytree.write(os.path.join(anno_copy_path,xml_names[index]), encoding='utf-8', pretty_print=True)
    index+=1

print("Ped Erased " + str(Ped_Erased))
print("Ped Kept " + str(Ped_Kept))