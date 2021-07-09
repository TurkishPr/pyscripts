
import os
import glob
import shutil
from xml.etree.ElementTree import Element, SubElement, dump
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ElementTree

import cv2
import argparse
import xml.etree.ElementTree as ET
 
import numpy as np
import re
import tempfile
 
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
 
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
    indent(note1)
    ElementTree(note1).write(xml_od)


parser = argparse.ArgumentParser()
parser.add_argument('-xml1', required=True)
parser.add_argument('-xml2', required=True)
parser.add_argument('-output', required=True)
args = parser.parse_args()
 
xml1_path = args.xml1
xml2_path = args.xml2
output_path = args.output
 
if not os.path.isdir( output_path ):
    os.makedirs(output_path)
 
xmls1 = glob.glob( os.path.join(xml1_path, "*.xml") )
 
for xml1 in xmls1:
    xml_one = ET.parse(xml1)
    root_one = xml_one.getroot()
 
    xml2 = os.path.join( xml2_path, os.path.basename(xml1) )
    xml_two = ET.parse(xml2)
    root_two = xml_two.getroot()
    objs_two = root_two.findall('object')
 
    root_one.extend(objs_two)
 
    xml_one.write( os.path.join(output_path, os.path.basename(xml1)) )