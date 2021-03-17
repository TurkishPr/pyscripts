import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from xml.etree.ElementTree import Element, SubElement, dump
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ElementTree

# def indent(elem, level=0):
#     i = "\n" + level*"  "
#     j = "\n" + (level-1)*"  "
#     if len(elem):
#         if not elem.text or not elem.text.strip():
#             elem.text = i + "  "
#         if not elem.tail or not elem.tail.strip():
#             elem.tail = i
#         for subelem in elem:
#             indent(subelem, level+1)
#         if not elem.tail or not elem.tail.strip():
#             elem.tail = j
#     else:
#         if level and (not elem.tail or not elem.tail.strip()):
#             elem.tail = j
#     return elem     


def merge_tstl_to_od(xml_tstl, xml_od):
    tree1 = parse(xml_od)
    note1 = tree1.getroot()
    tree2 = parse(xml_tstl)
    note2 = tree2.getroot()
    scale = float(note1.find("size").find("height").text) / float(note2.find("size").find("height").text)
    objects2 = note2.findall("object")
    for obj2 in objects2:
        if scale != 1:
            bbox = obj2.find("bndbox")
            bbox.find("xmin").text = '{:.2f}'.format(float(bbox.find("xmin").text) * scale)
            bbox.find("ymin").text = '{:.2f}'.format(float(bbox.find("ymin").text) * scale)
            bbox.find("xmax").text = '{:.2f}'.format(float(bbox.find("xmax").text) * scale)
            bbox.find("ymax").text = '{:.2f}'.format(float(bbox.find("ymax").text) * scale)
        note1.append(obj2)
    ElementTree(note1).write(xml_od)
    # indent(note1)
    
for src in glob.glob("C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\SOD_only_Annotations_Datateam\\labels_sod_v0.9_20210131\\*"): #tstl folder
    merge_tstl_to_od(src, "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\M551_SOD\\Annotations_GODTRAIN201223_Datateam\\" + src.split('\\')[-1]) #od folder