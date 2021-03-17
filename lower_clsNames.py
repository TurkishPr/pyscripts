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


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-cls', required=False)

args = parser.parse_args()
main_folder = args.mf
cls_name = args.cls

gt_count = {}

xml_path = os.path.join(main_folder, "Annotations")
xml_copy_path = os.path.join(main_folder, "Annotations_lower")

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
    newtxt = os.path.join(xml_copy_path,os.path.basename(xml).rsplit('.',1)[0]+'.xml')
    # print(os.path.join(img_folder_path,os.path.basename(xml).rsplit('.',1)[0]+'.jpg.result.jpg'))
    objCnt =0
    for obj in myroot.findall('object'):
        for obj in myroot.findall('object'):
            print((obj.find('name').text).lower())
            lowerCase = (obj.find('name').text).lower()
            # obj[0 = lowerCase
            # print(obj.attrib)
            for name in obj.findall('name'):
                name.text = (name.text).lower()
            #         # print(cls_idx)
            #         # print(xmin)
            #         # print(ymin)
            #         # print(xmax)
            #         # print(ymax)
            #         file.write("{} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(cls_idx, xmin, ymin, xmax, ymax))
    mytree.write(newtxt, encoding='utf-8', pretty_print=True)

    index+=1
print("file cnt " + str(index))
# for x, y in gt_count.items():
# for key, value in sorted(gt_count.items(), key=lambda item: item[1], reverse=True):
#   print("{} : {} ".format(key, value))
#     # index+=1