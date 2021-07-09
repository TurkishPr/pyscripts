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
parser.add_argument('-out', required=False)
parser.add_argument('-single_file', required=False)

args = parser.parse_args()
main_folder = args.mf
output_folder_name = args.out
single_file = args.single_file
xml_path = glob.glob(main_folder + '/Annotations/*')
img_folder_path = os.path.join(main_folder, 'JPEGImages')


if single_file != None:
    xml_path = os.path.join(main_folder, 'Annotations')
    xml = os.path.join(xml_path, single_file+'.xml')
    print(xml)
    local_file_name = os.path.basename(xml)
    print(local_file_name)

    # print(os.path.basename(xml).rsplit('.',1)[0])
    imgName = os.path.basename(xml).rsplit('.',1)[0]+'.png'
    # print(os.path.join(img_fold
    # er_path,imgName))
    image = cv2.imread(os.path.join(img_folder_path,imgName),cv2.IMREAD_COLOR)

    parser = ET.XMLParser(remove_blank_text=True)
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    modified =0

    for obj in myroot.findall('object'):
        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0
        for name in obj.findall('name'):
            if('ignored' not in name.text and 'animal' not in name.text and 'bird' not in name.text and not('bike'== name.text) and 'false' not in name.text and not('bicycle' == name.text)):
                modified =1
                xmin = int(float(obj[1][0].text))
                ymin = int(float(obj[1][1].text))
                xmax = int(float(obj[1][2].text))
                ymax = int(float(obj[1][3].text))
                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),1)
            else:
                modified=1
                xmin = int(float(obj[1][0].text))
                ymin = int(float(obj[1][1].text))
                xmax = int(float(obj[1][2].text))
                ymax = int(float(obj[1][3].text))
                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(161,146,137),1)

            width = xmax - xmin 
            height = ymax - ymin
            w_unit_seg = width / 32 #segmentation data divides the obj bbox into 32 * 32 grid.
            h_unit_seg = height / 32
            w_unit_part_conf = width/5 #for part confidence map 
            h_unit_part_conf = height/5
            
            seg_point_area = w_unit_seg * h_unit_seg
            part_conf_area = w_unit_part_conf * h_unit_part_conf

            seg_point_count= [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]

            part_conf = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]


            '''overlay segmentation data'''
            boxseg = obj.find('boxseg').text
            seg_x_cnt = 0
            seg_y_cnt = 0
            for count in range(len(boxseg)):
                if boxseg[count] != '0' and boxseg[count] != 'x' :
                    x_component = int(xmin+(w_unit_seg*seg_x_cnt))-2
                    y_component = int(ymin+(h_unit_seg*seg_y_cnt))+4

                    '''figure out which part_conf box this segmentation point falls into'''
                    for j in range(0, 5):
                        for i in range(0, 5):
                            if x_component > (xmin+(i*w_unit_part_conf)) and x_component < (xmin+((i+1)*w_unit_part_conf)) and y_component > (ymin+(j*h_unit_part_conf)) and y_component < (ymin+((j+1)*h_unit_part_conf)):
                                seg_point_count[i+(j*5)] += 1

                    coordinate = (x_component, y_component)
                    cv2.putText(image, '.', coordinate, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
                seg_x_cnt+=1
                if seg_x_cnt%32==0:
                    seg_x_cnt = 0
                    seg_y_cnt += 1

            '''also roughly calculate how much of the part_conf_box is covered up by seg points'''
            for j in range(0, 5):
                for i in range(0, 5):
                        if ((seg_point_count[i+(j*5)] * seg_point_area) / part_conf_area) > 1: #if score is over 1, just give it a 9
                            part_conf[i+(j*5)] = 9
                        else :
                            part_conf[i+(j*5)] = int(((seg_point_count[i+(j*5)] * seg_point_area) / part_conf_area)*10%10) # if score ranges from 0.0 ~ .9 turn it into 0~9
            # print(part_conf)    
            '''add and save the part_conf into the xml for the object''' 
            name = ET.SubElement(obj, "partconf")
            name.text = ",".join([str(int) for int in part_conf])
            # mytree.write(os.path.join(new_xml_path,local_file_name), encoding='utf-8', pretty_print=True)


            '''draw 5x5 grid'''
            for i in range(0, 5):
                cv2.line(image, (int(xmin+(i*w_unit_part_conf)), int(ymin)), (int(xmin+(i*w_unit_part_conf)), int(ymax)), (0, 0, 255), 1)
            for j in range(0, 5):
                cv2.line(image, (int(xmin), int(ymin+(j*h_unit_part_conf))), (int(xmax), int(ymin+(j*h_unit_part_conf))), (0, 0, 255), 1)

        cv2.imshow("test", image)
        cv2.waitKey(1)

else :

    new_xml_path = os.path.join(main_folder, output_folder_name)
    if not os.path.exists(new_xml_path):
        os.mkdir(new_xml_path)

    total = len(xml_path)
    count_var = 0

    parser = ET.XMLParser(remove_blank_text=True)
    for xml in xml_path:
        count_var+=1
        # print(xml)
        local_file_name = os.path.basename(xml)
        # print(local_file_name)

        # print(os.path.basename(xml).rsplit('.',1)[0])
        imgName = os.path.basename(xml).rsplit('.',1)[0]+'.jpg'
        print(os.path.join(img_folder_path,imgName))
        image = cv2.imread(os.path.join(img_folder_path,imgName),cv2.IMREAD_COLOR)

        mytree = ET.parse(xml, parser)
        myroot = mytree.getroot()
        modified =0


        x = [0, 0, 0, 0, 0, 0]
        y = [0, 0, 0, 0, 0, 0]
  
        show =1
        
        for car in myroot.findall('Car3D'):
            x1 = 10000
            y1 = 10000
            x2 = 0
            y2 = 0

            direction = int(car.get('Direction'))
            # print("Direction : " + str(direction))
            shape = int(car.get('Shape'))
            # print("Shape : " + str(shape))
            pt_cnt = 1
            for Point in car.findall('Point'):
                x[pt_cnt-1] = int(Point.get('x'))
                y[pt_cnt-1] = int(Point.get('y'))
                if(x1 > int(Point.get('x'))):
                    x1 = int(Point.get('x'))
                if(x2 < int(Point.get('x'))):
                    x2 = int(Point.get('x'))
                if(y1 > int(Point.get('y'))):
                    y1 = int(Point.get('y'))
                if(y2 < int(Point.get('y'))):
                    y2 = int(Point.get('y'))
                # print(x)
                # print(y)
                pt_cnt+=1
            # print("pt_cnt " + str(pt_cnt))
            cv2.putText(image, (str(shape) + " " + str(direction)), (x[0]+5,y[0]+15), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255))
            cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0), 2)
            if(shape == 2):
                if(pt_cnt-1==4):
                    cv2.line(image, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[0], y[0]), (x[2], y[2]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[1], y[1]), (0, 0, 255), 1)
                elif(pt_cnt-1==6):
                    cv2.line(image, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[0], y[0]), (x[2], y[2]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[4], y[4]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[5], y[5]), (0, 0, 255), 1)
                    cv2.line(image, (x[4], y[4]), (x[5], y[5]), (0, 0, 255), 1)
            elif(shape == 1):
                if(pt_cnt-1==4):
                    cv2.line(image, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[0], y[0]), (x[2], y[2]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[1], y[1]), (0, 0, 255), 1)
                elif(pt_cnt-1==6):
                    cv2.line(image, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[0], y[0]), (x[2], y[2]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[4], y[4]), (x[0], y[0]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[5], y[5]), (0, 0, 255), 1)
                    cv2.line(image, (x[4], y[4]), (x[5], y[5]), (0, 0, 255), 1)
            elif(shape == 0):
                if(pt_cnt-1==4):
                    cv2.line(image, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 1)
                    cv2.line(image, (x[0], y[0]), (x[2], y[2]), (0, 0, 255), 1)
                    cv2.line(image, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 1)
                    cv2.line(image, (x[3], y[3]), (x[1], y[1]), (0, 0, 255), 1)
            elif(shape == 3):
                show =1 
                print("3 ***********************")
            

        if show == 1:
            cv2.imshow("test", image)
            cv2.waitKey(0)

        # if modified: 
        #     cv2.imwrite(os.path.join(img_copy_path,imgName),image)
        #     print("{}/{}  {}".format(index,len(xml_names),os.path.join(img_copy_path,imgName)))
        #     modified=0
        print("total: {} count: {}".format(total,count_var), end='\r', flush=True)

