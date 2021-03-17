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

xml_path = os.path.join(main_folder, "Annotations_200202")
    
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
                if name.text in gt_count:
                    gt_count[name.text] +=1
                else:
                    gt_count[name.text]=1
        if modified:
            modified=0
    print("{}/{}  {} ".format(index,len(xml_names),xml), end='\r', flush=True)
    # clear()s
    index+=1
# print("file cnt : " + str(index))

# for x, y in gt_count.items():
total =0
for key, value in sorted(gt_count.items(), key=lambda item: item[0], reverse=False):
# for key, value in sorted(gt_count.items(), key=lambda item: item[1], reverse=True):
    total += value
    print("{} : {} ".format(key, value))
    # index+=1
print("total: {}\nsize: {}".format(total,len(gt_count)), end ='\r')