import os
import cv2
import glob
import argparse
import xml.etree.ElementTree as ET
​
import numpy as np
import re
import tempfile
import shutil
​
gt_color = (0, 0, 255)
ignored_color = (128, 128, 128)
fp_color = (255, 255, 255)
​
od_class = {
    'pedestrian': 1,
    'sedan': 3,
    'rider_bicycle': 2,
    'van': 3, 
    'rider_bike': 2, 
    'truck_etc': 4, 
    'pickup_truck': 3, 
    'bike': -1, 
    'vehicle_etc': 4, 
    'box_truck': 4, 
    'bicycle': -1, 
    'false_positive': -2, 
    'bus': 5, 
    'sitting_person': -1, 
    'excavator': 4, 
    'mixer_truck': 4, 
    'forklift': 4, 
    'truck': 4, 
    '3-wheels': 2, 
    'ladder_truck': 4, 
    'animal': -1,
    'ignored': -1,

    # LICENSE_PLATE = 1,


    'obstacle_cone' : 1,
    'obstacle_cylinder' : 2,
    'obstacle_drum' : 3,
    'parking_sign' : 6,
    'parking_cylinder' : 5,
    'parking_lock' : 7,
    'blocking_bar' : 9,
    'animal_ignored' : -1,
    'bird' : -1,
    'obstacle_ignored' : -7000
    'blocking_ignored' : -8000,
    'parking_ignored': -9000,
    'sod_ignored' : -10000,


    'roadmark_stopline' : 1,
    'roadmark_arrow' : 2,
    'ROADMARK_SPEED' : 3,
    'roadmark_crosswalk' : 4,
    'roadmark__bump' : 5,
    'roadmark_triangle' : 6,
    'roadmark_diamond' : 7,
    'roadmark_ignored' : -10000,
}
​
def imreadEX(image_path):
    if re.compile('[^ㄱ-ㅣ가-힣]+').sub('', image_path):
            stream = open(image_path, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            if not img is None:
                return img
            else:
                file_tmp=tempfile.NamedTemporaryFile().name
                shutil.copy(image_path,file_tmp)
                image_path=file_tmp
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    return img
​
def draw_xml(img, xml):
    one_xml = ET.parse(xml)
    root = one_xml.getroot()
    objs = root.findall('object')
​
    for obj in objs:
        draw_obj(img, obj)       
​
def draw_obj(img, obj):
    bbox = obj.find('bndbox')
    name = obj.find('name')
    print_name = od_class[name.text]
    color = gt_color
    if bbox != None:
        xmin = float(bbox[0].text)
        ymin = float(bbox[1].text)
        xmax = float(bbox[2].text)
        ymax = float(bbox[3].text)
        if print_name == -1:
            color = ignored_color
        elif print_name == -2:
            color = fp_color   
        cv2.putText(img, "{}".format(print_name), ( min(int(xmin)+10, int(xmax)), int(ymin)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2 )
        cv2.putText(img, "{}".format(print_name), ( min(int(xmin)+10, int(xmax)), int(ymin)), cv2.FONT_HERSHEY_PLAIN, 1, color, 1 )
        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax),int(ymax)), color, 1)
​
parser = argparse.ArgumentParser()
parser.add_argument('-xml', required=True)
args = parser.parse_args()
​
xml_path = args.xml
xmls = glob.glob( xml_path + "/*.xml" )
​
for xml in xmls:
    jpg_name = os.path.join( os.path.join( os.path.dirname(xml), "..") , os.path.join( "od_output", os.path.basename(xml).rsplit('.xml',1)[0])+".jpg.result.jpg" )
    img = imreadEX( jpg_name )
    draw_xml(img, xml)
    #cv2.imshow("img", img)
    cv2.imwrite(os.path.join( os.path.join( os.path.dirname(xml), "..") , os.path.join( "od_output_result", os.path.basename(xml).rsplit('.xml',1)[0])+".jpg.result.jpg" ), img)
​
print('Done')