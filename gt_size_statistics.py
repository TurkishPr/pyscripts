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

gt_size_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}

gt_wh_stats = {
    "PED" : {"width":[], "height":[]},
    "RIDER" : {"width":[], "height":[]},
    "CAR" : {"width":[], "height":[]},
    "TRUCK" : {"width":[], "height":[]},
    "BUS" : {"width":[], "height":[]},
    "ALL" : {"width":[], "height":[]},
}


def analyze(xml_od):
    #initialize variables
    tree = parse(xml_od)
    note = tree.getroot()
    
    #read each object in xml
    sizeInfo = note.find("size")
    img_w = int(sizeInfo.find("width").text)
    img_h = int(sizeInfo.find("height").text)
    # print(str(img_w))
    # print(str(img_h))
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
        w = round((xmax-xmin),3) /img_w
        h = round((ymax-ymin),3) /img_h
        size = round((xmax-xmin)*(ymax-ymin),3)
        # xml_bbox = [xmin, ymin, xmax, ymax]
        # print(gt_cls, xmin, ymin, xmax, ymax, size)
    
        gt_size_stats[name].append(size)
        gt_size_stats["ALL"].append(size)

        gt_wh_stats[name]["width"].append(w)
        gt_wh_stats[name]["height"].append(h)

        gt_wh_stats["ALL"]["width"].append(w)
        gt_wh_stats["ALL"]["height"].append(h)

   

count =0
# for src in glob.glob("C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Diff_Annotations\\subset\\*"): #GT SUBSET FOR TEST 
for src in glob.glob("C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Diff_Annotations\\Annotations_200929\\*"): #GT ALL
    count+=1
    analyze(src)
    print((str)(count) + " " + src, end ='\r')



# det_log_analysis
# main_folder = r"Z:\seongjin.lee\udb\GODTrain200929_refine_result_ver3"
output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics\\Annotations_200929_GT_size_statistics\\wh_to_image_size_ratio"


#print how many obj of each class there are
for key1, value1 in gt_size_stats.items():
    print(key1 + " " + str(len(value1)))

#plot size as bar graph
for key, value in gt_size_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=200)
    plt.gca().set(title='SIZE Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\SIZE_{}_{}.png".format(key.upper(), "annotated_gt")
    plt.savefig(filename)
    plt.close()

#plot width height of each class as scatter plot
for key, value in gt_wh_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
    plt.gca().set(title='Width Height Plot of {}'.format(key))
    # Plot width and height
    w = numpy.array(value["width"])
    h = numpy.array(value["height"])
    plt.scatter(w, h, s=2)
    # plt.show()
    filename = output_folder + "\\WH_{}_{}.png".format(key.upper(), "annotated_gt")
    plt.savefig(filename)
    plt.close()

# with open(output_folder + "\\conf.txt", 'w') as f:
#     for key, value in gt_size_stats.items():
#         f.write("%s\n" % key)
#         for item in value:
#             f.write("%s," % item)
#         f.write("\n")
#     f.close()
# det_log_analysis end
