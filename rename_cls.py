#! python3
'''
Reworking GT by changing Van to Truck
for M222re2 was retrained with van as truck, not car
Need to do this to test M222re2 properly
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


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-cls', required=True) #origin cls
parser.add_argument('-cls2', required=True) #dest cls


args = parser.parse_args()
main_folder = args.mf
obj_name = args.cls
obj_name2 = args.cls2

anno_folder = os.path.join(main_folder,"Annotations")
anno_copy_path = os.path.join( main_folder, "Annotations_fixed")

if not os.path.exists(anno_copy_path):
    os.mkdir(anno_copy_path)
    

xml_names = os.listdir(anno_folder)
xmlPaths = list(range(len(xml_names)))

index=0
for xml in xml_names:
    xmlPaths[index] = os.path.join(anno_folder , xml)
    index+=1


'''parse each xml file'''
parser = ET.XMLParser(remove_blank_text=True)
index=0
for xml in xmlPaths:
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    print(index)
    for obj in myroot.findall('object'):   
        for name in obj.findall('name'):
            if((name.text).lower()==obj_name.lower()):
                name.text = obj_name2.lower()

    mytree.write(os.path.join(anno_copy_path,xml_names[index]), encoding='utf-8', pretty_print=True)
    index+=1
