import os, sys
import json
import numpy as np
import cv2
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

# det_log_analysis
gt_conf_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}
# det_log_analysis end


def generate_softlabel(det_log, xml_od, new_path):
    #initialize variables
    tree = parse(xml_od)
    note = tree.getroot()
    #read each object in xml
    objects = note.findall("object")
    for obj in objects:
        gt_cls = obj.find("name").text

        name = gt_cls.upper()
        if "PED" in name or "PERSON" in name:
            name = "PED"
        elif "SEDAN" in name or "VAN" in name or "PICKUP_TRUCK" in name:
            name = "CAR"
        
        elif "TRUCK" in name or "EXCAVAT" in name or "FORK" in name or "VEHICLE_ETC" in name or "TRAILER" in name:
            name = "TRUCK"
        
        elif "RIDER" in name or "3-WHEELS" in name:
            name = "RIDER"

        elif "BUS" in name:
            name = "BUS"
        else: #ignored / ts / tl / etc that are not of interest
            continue

        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)
        xml_bbox = [xmin, ymin, xmax, ymax]
        size = round((xmax-xmin)*(ymax-ymin),3)
        # print(gt_cls, xmin, ymin, xmax, ymax, size)
    
        max_iou=0
        max_iou_softscore=0
        #open det_log and read and parse each line
        f = open(det_log, "r")
        for line in f:
            info = line.split()
            det_box = [float(info[2]),float(info[3]),float(info[4]),float(info[5])]
            conf = float(info[1])
            occ = float(info[6])
            trunc = float(info[7])
            # print(gt_cls, xmin, ymin, xmax, ymax, size)

            #consider that detected obj belongs to a GT with max IOU match or at least of a match > 0.5
            if IOU(det_box, xml_bbox) > max_iou and IOU(det_box, xml_bbox) > 0.5:
                max_iou = IOU(det_box, xml_bbox)
                
        
                #save that conf score of detected obj with max iou match with GT
                max_iou_softscore = conf
                
        if max_iou_softscore > 0: #if it is 0, it means that there was not a single detected obj that overlapped with GT with an IOU over 0.5.
            gt_conf_stats[name].append(max_iou_softscore)
            gt_conf_stats["ALL"].append(max_iou_softscore)

   

count =0
for src in glob.glob("Z:\\seongjin.lee\\udb\\GODTrain200929_refine_result_ver3\\*"): #conf, trunc, occ scores
    count+=1
    generate_softlabel(src, "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Diff_Annotations\\Annotations_200929\\" + src.split('\\')[-1][:-4]+".xml", "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Annotations_0.6") #od folder, new location for softlabel
    print((str)(count) + " " + src, end ='\r')



# det_log_analysis
# main_folder = r"Z:\seongjin.lee\udb\GODTrain200929_refine_result_ver3"
output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics"


for key1, value1 in gt_conf_stats.items():
    print(key1 + " " + str(len(value1)))

for key, value in gt_conf_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=50)
    plt.gca().set(title='Conf Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\CONF_{}_{}.png".format(key.upper(), "M523_gt")
    plt.savefig(filename)
    plt.close()

with open(output_folder + "\\conf.txt", 'w') as f:
    for key, value in gt_conf_stats.items():
        f.write("%s\n" % key)
        for item in value:
            f.write("%s," % item)
        f.write("\n")
    f.close()
# det_log_analysis end
