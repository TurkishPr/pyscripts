#! python3
import os, sys
# from posix import XATTR_SIZE_MAX
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from lxml import etree as ET
import random

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-img_folder', required=True)
parser.add_argument('-json_folder', required=True)

args = parser.parse_args()
main_folder = args.mf
img_folder = args.img_folder
json_folder = args.json_folder

if not os.path.exists(os.path.join(main_folder, "output")):
    os.mkdir(os.path.join(main_folder, "output"))

json_list = glob.glob(json_folder+"\*")
img_list = glob.glob(img_folder+"\*")

image_resize_ratio = 2
for json_f in json_list:
    img_resized = False #true if image was resized
    print(json_f)

    #load json
    f = open(json_f)
    data = json.load(f)

    orig_width = 0
    orig_height = 0 
    resized_width = 0
    resized_height = 0 

    if "width" in data:
        orig_width = data["width"]
        orig_height = data["height"]
    elif "imgHeight" in data:
        orig_width = data["imgWidth"]
        orig_height = data["imgHeight"]

    #read image
    imgName = os.path.basename(json_f).rsplit('.',1)[0]+'.jpg'
    image = cv2.imread(os.path.join(img_folder,imgName),cv2.IMREAD_COLOR)

    if orig_width > 2000 or orig_height > 2000 : #if image is a bit big, resize it
        resized_width =  orig_width / image_resize_ratio
        resized_height =  orig_height / image_resize_ratio
        img_resized = True

    print(orig_height)
    print(orig_width)
    print(int(resized_width))
    print(int(resized_height))

    if img_resized:
        image = cv2.resize(image, (int(resized_width), int(resized_height)) )
    for obj in data['objects']: #traverse all info of all objects
        x = y = x2 = y2 = 0
        color = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
        name = obj["label"]
        if "human" in name or "vehicle" in name and "group" not in name and "bicycle" not in name: #if the obj if of a class we want
            print(name)
            x_max = 0
            y_max = 0
            x_min = 10000
            y_min = 10000
            for point in obj["polygon"]: #for obj's of interest, traverse polygon coord to extract bbox
                x = point[0]
                y = point[1]
                if  x2 != 0 :
                    cv2.line(image, (int(x/image_resize_ratio), int(y/image_resize_ratio)), (int(x2/image_resize_ratio), int(y2/image_resize_ratio)), color, 2)
                x2 = x
                y2 = y
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                
            obj_w = x_max - x_min
            obj_h = y_max - y_min
            print(obj_w)
            print(obj_h)
            if obj_w < orig_width/90 or obj_h < orig_height/90 or (y_max > orig_height*0.9 and obj_w > orig_width*0.5):
                continue
            
            if img_resized: #if image was resized, resize coordinates also
                x_max = x_max / image_resize_ratio
                y_max = y_max / image_resize_ratio
                x_min = x_min / image_resize_ratio
                y_min = y_min / image_resize_ratio


            cv2.rectangle(image,(int(x_min),int(y_min)),(int(x_max),int(y_max)),(0,0,255),2)
        cv2.imshow("test", image)
        cv2.waitKey(0)
