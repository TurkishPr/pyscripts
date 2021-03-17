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
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


'''receive and parse arguments'''
parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)

args = parser.parse_args()
main_folder = args.mf

xml = os.path.join(main_folder, 'aachen_000000_000019_leftImg8bit.xml')
image = cv2.imread(os.path.join(main_folder,'aachen_000000_000019_leftImg8bit.png'))
plt.rcParams["figure.figsize"] = (20,14)
im = plt.imread(os.path.join(main_folder,'aachen_000000_000019_leftImg8bit.png'))
implot = plt.imshow(im)
# plt.figure(figsize=(50,50))
xml = ET.parse(xml)
root = xml.getroot()
objs = root.findall('object')
for obj in objs:
    name = obj.find('name').text
    bndbox = obj.find('bndbox')
    xmin = int(float(bndbox.find('xmin').text))
    ymin = int(float(bndbox.find('ymin').text))
    xmax = int(float(bndbox.find('xmax').text))
    ymax = int(float(bndbox.find('ymax').text))
    cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),1)
    seg = obj.find('boxseg').text
    width = int(xmax - xmin)
    height =int(ymax - ymin)

    # for y in range (0, 32):
        # for x in range (0, 32):
            # print((y*32)+x)
            # plt.scatter(x=[xmin+(width/32*x)], y=[ymin+(height/32*y)], c=(float(seg[y*32+x])/10, 0, 0 ), s=5)
        # print(seg[y*32:y*32+32])




    # put a blue dot at (10, 20)
    # plt.scatter([10], [20])
    
    # put a red dot, size 40, at 2 locations:

plt.show()
    
# cv2.imshow("resized",image)
# cv2.waitKey(0)
