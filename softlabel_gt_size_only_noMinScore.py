import os, sys
import json
import numpy as np
# import cv2
import glob
import shutil
import argparse
import subprocess
import os
import glob
import shutil
from xml.etree.ElementTree import Element, SubElement, dump
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy 

def IOU(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem     

gt_conf_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}

def generate_softlabel(det_log, xml_od, new_path):
    #initialize variables
    tree = parse(xml_od)
    note = tree.getroot()

    size_ptr = note.find("size")
    img_w = float(size_ptr.find("width").text)
    img_h = float(size_ptr.find("height").text)
    img_size = img_w*img_h

    #read each object in xml
    objects = note.findall("object")
    for obj in objects:
        gt_cls = obj.find("name").text
        stat_name = gt_cls.upper() #name used for statistic analysis
        if "ignored" in gt_cls or "ts" in gt_cls or "tl" in gt_cls:
            continue
        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)
        w = round((xmax-xmin),3) /img_w
        h = round((ymax-ymin),3) /img_h
        #size of obj
        size = round((xmax-xmin)*(ymax-ymin),3)
        size_score = 0

        if "PED" in stat_name or "PERSON" in stat_name:
            stat_name = "PED"
            max_size = (img_size*0.0016) #the base size : object h / w is ~ 1/10 of image h / w  
        elif "SEDAN" in stat_name or "VAN" in stat_name or "PICKUP_TRUCK" in stat_name:
            stat_name = "CAR"
            max_size = (img_size/100.0) #the base size : object h / w is ~ 1/10 of image h / w  
        
        elif "TRUCK" in stat_name or "EXCAVAT" in stat_name or "FORK" in stat_name or "VEHICLE_ETC" in stat_name or "TRAILER" in stat_name:
            stat_name = "TRUCK"
            max_size = (img_size*0.04) #the base size : object h / w is ~ 1/10 of image h / w  
        
        elif "RIDER" in stat_name or "3-WHEELS" in stat_name:
            stat_name = "RIDER"
            max_size = (img_size/500.0) #the base size : object h / w is ~ 1/10 of image h / w  

        elif "BUS" in stat_name:
            stat_name = "BUS"
            max_size = (img_size*0.04) #the base size : object h / w is ~ 1/10 of image h / w  
        else: #ignored / ts / tl / etc that are not of interest
            continue


        if size>max_size: #if obj is larger than base size full score of 1
            size_score=1
        else: #if obj is smaller than base size, gradually decrease approaching 0.4
            size_score = round((size/max_size),3)

        gt_conf_stats[stat_name].append(size_score)
        gt_conf_stats["ALL"].append(size_score)

        softscore_elem = ET.SubElement(obj, "softscore")
        softscore_elem.text = str(size_score)

    xml_base = os.path.basename(xml_od)
    # print(os.path.join(new_path, xml_base))
    with open(os.path.join(new_path, xml_base), 'wb') as f:
        tree.write(f)
   


output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics\\size_gt_joseph_conf_statistics" #statistics output folder
count =0
for src in glob.glob("Z:\\seongjin.lee\\udb\\GODTrain200929_refine_result_ver3\\*"): #conf, trunc, occ scores
# for src in glob.glob("Z:\\seongjin.lee\\udb\\test\\*"): #conf, trunc, occ scores
    count+=1
    generate_softlabel(src, "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Diff_Annotations\\Annotations_200929\\" + src.split('\\')[-1][:-4]+".xml", "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Annotations") #od folder, new location for softlabel
    print((str)(count) + " " + src, end ='\r')

for key, value in gt_conf_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=50)
    plt.gca().set(title='Conf Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\CONF_{}_{}.png".format(key.upper(), "size_joseph")
    plt.savefig(filename)
    plt.close()
