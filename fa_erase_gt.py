#! python3
'''
Reworking GT for pedestrians as an effort to reduce FPs

I have picked out all images with ped gt that I want.
This program removes all ped gt other than the ones included in images mentioned above
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


main_folder = r'C:\Users\Yoseop\Desktop\Personal\OD_Work\FA\GODTrain191122_Freetech2'
anno_folder = os.path.join(main_folder,"Annotations_orig")
# img_copy_path = os.path.join( main_folder, "JPEGImages_gt_filtered")
anno_copy_path = os.path.join( main_folder, "Annotations")
img_folder_path = os.path.join(main_folder, "JPEGImages")
refined_gt_path = os.path.join(main_folder, "gt_refined")

# if not os.path.exists(img_copy_path):
#     os.mkdir(img_copy_path)
if not os.path.exists(anno_copy_path):
    os.mkdir(anno_copy_path)
    
# xmls = glob.glob(anno_folder+"/*.xml")
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
    # firsttime =1
    # print(xml)
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    # print(index)
    for obj in myroot.findall('object'):   
        for name in obj.findall('name'):
            if(name.text=='pedestrian'):
                # print(os.path.join(refined_gt_path, img_names[index]))
                if not os.path.isfile(os.path.join(refined_gt_path, img_names[index])):
                    # firsttime=0
                    myroot.remove(obj)
                    print(os.path.join(refined_gt_path, img_names[index]))
                    Ped_Erased+=1
                # xmin = int(float(obj[1][0].text))
                # ymin = int(float(obj[1][1].text))
                # xmax = int(float(obj[1][2].text))
                # ymax = int(float(obj[1][3].text))

                # obj.remove(name)

    # if modified and erased:
    #     modified=0
    #     erased=0
    mytree.write(os.path.join(anno_copy_path,xml_names[index]), encoding='utf-8', pretty_print=True)
    index+=1

# print("Ped Erased " + str(Ped_Erased))
print("Erased Ped GT " + str(Ped_Erased))