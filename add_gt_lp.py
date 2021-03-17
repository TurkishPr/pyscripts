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

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
# parser.add_argument('-jpgs', required=True)
# parser.add_argument('-output', required=True)
# parser.add_argument('-type', required=False)

args = parser.parse_args()
# xml_type = args.type
# obj_name = args.name
# jpg_path = args.jpgs
main_folder = args.mf

xml_path = os.path.join(main_folder, "Annotations")
img_copy_path = os.path.join(main_folder, "images_annotations_with_gt")
# img_copy_path = os.path.join( "C:/Users/Yoseop/Desktop/Personal/OD_Work/NewFeat_Ger/results_gt/lp", "images_annotations_with_gt")
img_folder_path = os.path.join(main_folder, "JPEGImages")
# print(img_copy_path)
# print(img_folder_path)

# single_file = r'C:\Users\YoseopKim\Desktop\Personal\OD_Work\Roadmark\roadmarktrain191002\Annotations\201706_hoo.kim_gopr1330.mp4_01190.xml'
if not os.path.exists(img_copy_path):
    os.mkdir(img_copy_path)
    
xml_names = os.listdir(xml_path)
img_names = os.listdir(img_folder_path)

xmlPaths = list(range(len(xml_names)))
imgPaths = list(range(len(img_names)))

index=0
for xml in xml_names:
    # if str(record)=="xml":
    #     continue
    xmlPaths[index] = os.path.join(xml_path , xml)
    index+=1

index=0
for jpg in img_names:
    # if str(record)=="xml":
    #     continue
    imgPaths[index] = os.path.join(img_folder_path , jpg)
    index+=1

parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
nonIgnoredCnt =0

xmin = 3000
ymin = 3000
xmax = -1000
ymax = -1000
platecnt = 0
twoplateCnt = 0
for xml in xmlPaths:
    # print(xml)
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    imgName =os.path.basename(xml).rsplit('.',1)[0]+'.jpg.result.jpg'
    image = cv2.imread(os.path.join(img_folder_path,imgName),cv2.IMREAD_COLOR)
    for obj in myroot.findall('object'):

        # modified =1
        for plate in obj.findall('LicensePlate'):
            xmin = 3000
            ymin = 3000
            xmax = -1000
            ymax = -1000
            platecnt+=1
            # print("Platecnt " + str(platecnt))
            if platecnt ==2:
                twoplateCnt+=1
            for point in plate.findall('Point'):
                # print(imgName)
            # if('ignored' not in name.text and 'animal' not in name.text and 'bird' not in name.text):
                # nonIgnoredCnt+=1
                modified =1
                # x = int(float(obj[1][0].text))
                # y = int(float(obj[1][1].text))
                # x2 = int(float(obj[1][2].text))
                # y2 = int(float(obj[1][3].text))
                # print(x)
                # print(y)
                # print("point")
                x = float(point.get('x'))
                y = float(point.get('y'))
                
                # print(point.attrib)
                # print(x)
                # print(y)
                # print(x2)
                # print(y2)

                if(int(x) > int(xmax)):
                    xmax = int(x)
                if(int(y) > int(ymax)):
                    ymax = int(y)
                if(int(y) < int(ymin)):
                    ymin = int(y)
                if(int(x) < int(xmin)):
                    xmin = int(x)
                # print(point)
                # print(xmin)
                # print(ymin)
                # print(xmax)
                # print(ymax)

            if modified:
                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),1)
                cv2.putText(image, "[{}]".format(1), ( min(int(xmin)+30, int(xmax)), int(ymin)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2 )
                cv2.imwrite(os.path.join(img_copy_path,imgName),image)
                modified=0



        platecnt=0
    print(xml + ": " + str(index))
    # print(index)
    


    index+=1

print(index)
print(nonIgnoredCnt)
print(twoplateCnt)
