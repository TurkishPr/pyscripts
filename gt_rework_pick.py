#! python3
'''
Reworking GT for pedestrians as an effort to reduce FPs

Removing all GT that are smaller than
36 in height
or
7 in width

SO keeping all ped GT that are larger than or equal to
37 in height
and
8 in width
'''
import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from lxml import etree as ET
import msvcrt as m



main_folder = r'C:\Users\Yoseop\Desktop\Personal\OD_Work\PyScripts\test'
anno_folder = os.path.join(main_folder,"Annotations")
# img_copy_path = os.path.join( main_folder, "JPEGImages_gt_filtered")
anno_copy_path = os.path.join( main_folder, "New_Annotations")
img_folder_path = os.path.join(main_folder, "JPEGImages")
# if not os.path.exists(img_copy_path):
#     os.mkdir(img_copy_path)
if not os.path.exists(anno_copy_path):
    os.mkdir(anno_copy_path)
    

xml_names = os.listdir(anno_folder)
img_names = os.listdir(img_folder_path)
xmlPaths = list(range(len(xml_names)))
imgPaths = list(range(len(img_names)))

index=0
for xml in xml_names:
    xmlPaths[index] = os.path.join(anno_folder , xml)
    index+=1

index=0
for jpg in img_names:
    imgPaths[index] = os.path.join(img_folder_path , jpg)
    index+=1

Ped_Erased =0
Ped_Kept =0

def wait():
    usr_input=m.getch()
    print(usr_input)
    return usr_input

'''parse each xml file'''
parser = ET.XMLParser(remove_blank_text=True)
index=0
modified=0
erased=0
cnt=0 #number of gt of a certain class in an image
cnt2=0 #cnt in the loop
usr_input =''
gt_to_del =[] #gt to delete
for xml in xmlPaths:
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    image = cv2.imread(imgPaths[index],cv2.IMREAD_COLOR)

    cnt=0
    for obj in myroot.findall('object'):   
        for name in obj.findall('name'):
            if(name.text=='pedestrian'):
                cnt+=1
    print("cnt is " + str(cnt))
    cnt2=1
    for i in range(1, cnt+1): #cnt 가 3이라면 1,2,3
        for obj in myroot.findall('object'):   
            for name in obj.findall('name'): #결국 하나인데..name은
                if(name.text=='pedestrian'):
                    xmin = int(float(obj[1][0].text))
                    ymin = int(float(obj[1][1].text))
                    xmax = int(float(obj[1][2].text))
                    ymax = int(float(obj[1][3].text))
                    # print("i is " + str(i))
                    # print("c is " + str(cnt2) + "\n")
                    if(i==cnt2):
                        cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),2)
                    else:
                        cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,255,0),2)
                    cnt2+=1
        cnt2=1
        cv2.imshow("image", image)
        cv2.waitKey(1000)   
        usr_input = wait()
        print(usr_input)
        cv2.destroyAllWindows()
        if (usr_input == 'e'):
            print("HI")
            Ped_Erased+=1
            gt_to_del.append(str(i))
        
        # if(cnt2>cnt):
        #     break
    # obj.remove(name)
    print(gt_to_del)
    if modified and erased:
        # cv2.imwrite(os.path.join(img_copy_path,img_names[index]),image)
        modified=0
        erased=0
    # mytree.write(os.path.join(anno_copy_path,xml_names[index]), encoding='utf-8', pretty_print=True)
    index+=1

print("Ped Erased " + str(Ped_Erased))
# print("Ped Kept " + str(Ped_Kept))

'''
count PED

loop through them
    show only one red
    if button 'a' pressed,
    erase
    if not
    move on
'''
