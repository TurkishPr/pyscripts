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

'''
extracts GT images into each newly created respective folders
If -cls is given as "parking" and there are classes such as "parking_block" "parking_marker"
then all these GT's will be extracted into folders of the corresponding cls names.
'''

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-cls', required=True)
parser.add_argument('-type', required=False)

args = parser.parse_args()
xml_type = args.type
main_folder = args.mf
obj_name = args.cls

annotation_folder_name = "Annotations"
img_folder_name = "JPEGImages"
img_ext =".jpg"

xml_path = os.path.join(main_folder, annotation_folder_name)
img_folder_path = os.path.join(main_folder, img_folder_name)

xmlPaths = glob.glob(xml_path+"/*.xml")
imgPaths = glob.glob(img_folder_path+"/*.")

height_stat =0
'''parse each normal xml file'''

parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
foundCnt={}

with open(os.path.join(main_folder, os.path.join("ImageSets", 'all.txt'))) as f:
    lines = f.readlines()
    for imageName in lines:
        # print(line)
        xml = os.path.join(main_folder, os.path.join("Annotations", imageName[:-1]+".xml"))
        print(xml)    
        mytree = ET.parse(xml, parser)
        myroot = mytree.getroot()
        image = cv2.imread(xml.rsplit(annotation_folder_name)[0] + img_folder_name + xml.rsplit(annotation_folder_name)[1][:-4] + img_ext, cv2.IMREAD_COLOR)
        for obj in myroot.findall('object'):
            # modified =1
            for name in obj.findall('name'):
                # print(name.text)
                # print(obj_name)
                # print(obj[1].text)
                gt_name = (name.text).lower()
                # if((name.text).lower()==obj_name.lower()): #and obj[1].text=='box_truck'):
                if(obj_name.lower() in gt_name): #and obj[1].text=='normal'):  #when we found a matching GT
                    img_copy_path = os.path.join(main_folder, "GT_"+gt_name)
                    # print(img_copy_path)
                    # print(xml.rsplit(annotation_folder_name)[1][1:-4] + img_ext)
                    # print(os.path.join(img_copy_path, xml.rsplit(annotation_folder_name)[1][1:-4] + img_ext)) 
                    if not os.path.exists(img_copy_path): #create folder for the GT if does not exist
                        os.mkdir(img_copy_path)

                    if name.text in foundCnt:  #keep count of the gt
                        foundCnt[gt_name] +=1
                    else:
                        foundCnt[gt_name]=1

                    print('found ' + gt_name +  ': ' + str(foundCnt[gt_name])) #print cur stat
                    # print(xml.rsplit(annotation_folder_name)[0] + img_folder_name + xml.rsplit(annotation_folder_name)[1][:-4] + img_ext)
                    # print(os.path.join(img_copy_path, xml.rsplit(annotation_folder_name)[1][:-4] + img_ext))
                    # print(obj[1].text)

                    # #if xml has subclasses
                    # xmin = int(float(obj[2][0].text))
                    # ymin = int(float(obj[2][1].text))
                    # xmax = int(float(obj[2][2].text))
                    # ymax = int(float(obj[2][3].text))
                    # # if xml does not have subclasses
                    xmin = int(float(obj[1][0].text))
                    ymin = int(float(obj[1][1].text))
                    xmax = int(float(obj[1][2].text))
                    ymax = int(float(obj[1][3].text))

                    #put rider direction text on image
                    print(obj[2].text)
                    cv2.putText(image,obj[2].text, (xmax,ymin), 1, 2, (0,0,255), 2)
                    modified =1

                    cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),3)
                    '''for box truck'''
                    # if(ymax-ymin<110 and ymax-ymin>=51):
                    #     if(obj[1].text == 'box_truck'):
                    #         cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),1)
                    #         print(xml)
                    #         print(ymax-ymin)
                    #         height_stat +=1
                    #         modified =1
                    # print(xmin)
                    # print(ymin)
                    # print(xmax)
                    # print(ymax)

        if modified:
            cv2.imwrite(os.path.join(img_copy_path, xml.rsplit(annotation_folder_name)[1][1:-4] + img_ext),image)
            modified=0
        index+=1
        print(index, end='\r' ,flush=True)
    print(index)
    # print("height_stat : {}".format(height_stat))

    # print(xml)
    # print(xml.rsplit('Annotations')[0])
    # print(xml.rsplit(annotation_folder_name)[0] + img_folder_name + xml.rsplit(annotation_folder_name)[1][:-4] + ".jpg")