#! python3
import os, sys
from os import system, name
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from lxml import etree as ET
# import call method from subprocess module
from subprocess import call

# import sleep to show output for some time period
from time import sleep


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)

args = parser.parse_args()
main_folder = args.mf

gt_count = {}

xml_path = os.path.join(main_folder, "Annotations")

img_path = os.path.join(main_folder, "JPEGImages")

img_copy_path = os.path.join(main_folder, "gt_images")
if not os.path.exists(img_copy_path):
    os.mkdir(img_copy_path)


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
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    objCnt =0
    for obj in myroot.findall('object'):
        objCnt+=1

        for name in obj.findall('name'):
                modified =1
                if "pedestrian" in name.text and "ignored" not in name.text:
                    print(xml.rsplit('\\')[-1][:-4])
                    if len(obj)<=6:
                        print("{} {} {} ".format(name.text, obj[1].text, obj[5].text))
                        # if obj[5].text == '1':
                        if name.text in gt_count:
                            gt_count[name.text] +=1
                        else:
                            gt_count[name.text]=1
                    else :
                        print("{} {} {} {}".format(name.text, obj[1].text, obj[5].text, obj[6].text))
                        # if obj[6].text=="road":
                        if name.text in gt_count:
                            gt_count[name.text] +=1
                        else:
                            gt_count[name.text]=1
                        # print("{} {} ".format(name.text, obj[1].text))
                        # print("{}/{}  {} \r".format(index,len(xml_names),xml), end='\r', flush=True)
                        # print(xml.rsplit('\\')[-1][:-4])
                            jpgName = xml.rsplit('\\')[-1][:-4]+'.jpg'
                        # shutil.copy( os.path.join(img_path, jpgName), img_copy_path )
                # if "ts_sup" in name.text and "ignored" not in name.text:
                #     print(xml.rsplit('\\')[-1][:-4])
                #     print("{} {} ".format(name.text, obj[1].text))
                #     # if obj[5].text == '0':
                #     if name.text in gt_count:
                #         gt_count[name.text] +=1
                #     else:
                #         gt_count[name.text]=1

        if modified:
            modified=0

    # clear()
    index+=1
# print("file cnt : " + str(index))

# for x, y in gt_count.items():
total =0
for key, value in sorted(gt_count.items(), key=lambda item: item[0], reverse=False):
# for key, value in sorted(gt_count.items(), key=lambda item: item[1], reverse=True):
    total += value
    print("{} : {} ".format(key, value))
    # index+=1
print("total: {}\nsize: {}".format(total,len(gt_count)))