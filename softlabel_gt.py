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


def generate_softlabel(det_log, xml_od, new_path):
    #initialize variables
    tree = parse(xml_od)
    note = tree.getroot()
    #read each object in xml
    objects = note.findall("object")
    for obj in objects:
        gt_cls = obj.find("name").text
        if "ignored" in gt_cls or "ts" in gt_cls or "tl" in gt_cls:
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

            #if IOU is greater than 0.5, consider them the same obj
            #combine [ occ, trunc, size, conf ] into a single softlabel score and add it to the object
            if IOU(det_box, xml_bbox) > max_iou and IOU(det_box, xml_bbox) > 0.5:
                max_iou = IOU(det_box, xml_bbox)
                # max_obj = obj

                if occ > 0 and trunc > 0:
                    max_iou_softscore = str(conf * (1 - max(occ, trunc)*.6))
                elif occ > 0:
                    max_iou_softscore = str(conf * (1 - occ *.6))
                elif trunc > 0:
                    max_iou_softscore = str(conf * (1 - trunc *.6))
                else:
                    max_iou_softscore = str(conf)

        # print(line, max_iou_softscore)
        # softscore_elem = Element.Element("softscore")
        # softscore_elem.text = softscore
        # obj.set("softscore")
        # if max_iou_softscore != -1:
        softscore_elem = ET.SubElement(obj, "softscore")
        softscore_elem.text = max_iou_softscore

    xml_base = os.path.basename(xml_od)
    # print(os.path.join(new_path, xml_base))
    with open(os.path.join(new_path, xml_base), 'wb') as f:
        tree.write(f)
   

count =0
for src in glob.glob("Z:\\seongjin.lee\\udb\\GODTrain200929_refine_result_ver3\\*"): #conf, trunc, occ scores
    count+=1
    generate_softlabel(src, "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Diff_Annotations\\Annotations_200929\\" + src.split('\\')[-1][:-4]+".xml", "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Annotations_0.6") #od folder, new location for softlabel
    print((str)(count) + " " + src, end ='\r')