import os
import cv2
import glob
import argparse
import xml.etree.ElementTree as ET

import numpy as np
import re
import tempfile
import shutil

od_class = {
    'pedestrian' : 1,
    'rider_bicycle' : 2,
    'rider_bike' : 3,
    'sedan' : 4,
    'van' : 5,
    'truck' : 6,
    'box_truck' : 7,
    'bus' : 8,
    'sitting_person' : 9,
    'ignored' : 10,
    'bicycle' : 11,
    'bike' : 12,
    '3-wheels' : 13,
    'pickup_truck' : 14,
    'mixer_truck' : 15,
    'excavator' : 16,
    'forklift' : 17,
    'ladder_truck' : 18,
    'truck_etc' : 19,
    'vehicle_etc' : 20,
    'false_positive' : 21,
    'animal' : 22,
    'bird' : 23,
    'animal_ignored' : 24
}

tstld_class = {
    'ts_circle': 1,
    'ts_circle_speed': 2, 
    'ts_triangle': 3,
    'ts_Inverted_triangle': 4, 
    'ts_rectangle': 5,
    'ts_rectangle_speed': 6,
    'ts_diamonds': 7,
    'ts_ignored': 8,
    'tl_car': 9, 
    'tl_ped': 10, 
    'tl_special': 11,
    'tl_ignored': 12,
    'tl_light_only': 13,
    'ts_supplementary': 14
} 



parser = argparse.ArgumentParser()
parser.add_argument('-xml', required=True)
args = parser.parse_args()

xml_path = args.xml
txt_path = os.path.join( os.path.dirname(xml_path), os.path.basename(xml_path)+".txt" )
print(txt_path)

txt_file = open( txt_path, 'w')
xmls = glob.glob( xml_path + "/*.xml" )

obj_count = dict()
class_occ_count = dict()

for xml in xmls:
    txt_file.write(os.path.basename(xml).rsplit('.xml', 1)[0]+'.jpg\n')

    one_xml = ET.parse(xml)
    root = one_xml.getroot()
    objs = root.findall('object')

    txt_file.write(str(len(objs))+'\n')

    for obj in objs:
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text

        txt_file.write('{} {} {} {} {} ""\n'.format(od_class[name], xmin, ymin, xmax, ymax))
    
txt_file.close()
