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


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-det', required=True)
parser.add_argument('-out', required=False)

args = parser.parse_args()
main_folder = args.mf
det_folder = args.det
output_folder_name = args.out
gt_xmls = glob.glob(main_folder + '/Annotations/*')
det_results_ = glob.glob(det_folder + '/*')
det_results = []
img_folder_path = os.path.join(main_folder, 'JPEGImages')


'''Remove files that are not of interest files'''
for i, det_ in enumerate(det_results_):
    # print(det_)
    if "CAR" in det_ or "TRUCK" in det_ or "BUS" in det_:
        det_results.append(det_)
print("\nFiles to Process")
for i, det_ in enumerate(det_results):
    print(det_results[i])


'''
detection_boxes = { 'img_name_1' : [ [ x1, y1, y1, y2, score, direction, class ], [ x1, y1, y1, y2, score, direction, class ], ...  ]}
gt_boxes = { 'img_name_1' : [ [ x1, y1, y1, y2, score, direction ], [ x1, y1, y1, y2, score, direction ], ...  ]}

'''

direction_map = [ -1, 6, 5, 4, 7, 0, 3, 8, 1, 2 ] #direction mapping from annotated direction to trained direction

num_classes = 3 # car, truck, bus
class_names = ["CAR", "TRUCK", "BUS"]

detection_boxes = {}
gt_boxes = {}
# detection_boxes = [[] for _ in range(len(gt_xmls))]
# gt_boxes = [[] for _ in range(len(gt_xmls))]

'''READ 3D GT DATA FROM XML FILES '''
total = len(gt_xmls)
count_var = 0
parser = ET.XMLParser(remove_blank_text=True)
print("\nReading 3D GT DATA")
for i, xml in enumerate(gt_xmls):
    first_item = True
    count_var+=1
    # local_file_name = os.path.basename(xml)
    imgName = os.path.basename(xml).rsplit('.',1)[0]+'.jpg'
    
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    modified =0
    
    for car in myroot.findall('Car3D'):
        x1 = 10000
        y1 = 10000
        x2 = 0
        y2 = 0
       
        direction = int(car.get('Direction'))
        # print("Direction : " + str(direction))
        shape = int(car.get('Shape'))
        # print("Shape : " + str(shape))

        for Point in car.findall('Point'):
            if(x1 > int(Point.get('x'))):
                x1 = int(Point.get('x'))
            if(x2 < int(Point.get('x'))):
                x2 = int(Point.get('x'))
            if(y1 > int(Point.get('y'))):
                y1 = int(Point.get('y'))
            if(y2 < int(Point.get('y'))):
                y2 = int(Point.get('y'))
        dummy_list = [x1, y1, x2, y2, direction]
        if  first_item:
            first_item = False
            gt_boxes[imgName]=[]
            gt_boxes[imgName].append(dummy_list)        
            detection_boxes[imgName]=[] #create copy with same img names as key
        else:
            gt_boxes[imgName].append(dummy_list)        

    print("total: {} count: {}".format(total,count_var), end='\r', flush=True)

# print(detection_boxes)
'''print GT Data'''
# for img in gt_boxes:
#     print(str(img) + " " + str(gt_boxes[img]))


'''READ DET RESULTS FROM TXT FILES in ZF FORMAT'''
print("\n\nReading Detection Log")
obj_count = 0
total_ = 0
for i, det in enumerate(det_results):
    local_file_name = os.path.basename(det)
    print(local_file_name)
    class_ = local_file_name.split('OBJECTCLASS_')[1][:-4].lower()
    # print(class_)
    file1 = open(det, 'r')
    Lines = file1.readlines()

    count = 0
    prev_name = ""
    # Strips the newline character
    total_ += len(Lines)
    cur_cnt_ = 0
    for line in Lines:
        image_name = line.split('JPEGImages\\')[1].split(' ')[0]
        obj_count+=1
        # print(image_name)
        split_data = line.split(' ')
        score = float(split_data[1])
        x1 = int(split_data[2])
        y1 = int(split_data[3])
        x2 = int(split_data[4])
        y2 = int(split_data[5])
        shape = int(split_data[6])
        direction = int(split_data[7][:-1]) #get rid of newline char
        # print(split_data)
        # print(str(shape) + " " + str(direction))
        dummy_list = [x1, y1, x2, y2, direction, shape, score]
        detection_boxes[image_name].append(dummy_list)
        print("total: {} count: {}".format(total_,obj_count), end='\r', flush=True)

'''print Detection Result '''
# for img in detection_boxes:
#     print(str(img) + " " + str(detection_boxes[img]))



''' calculate accuracy of direction detection
    loop through every item in det_obj_dictionary
    and look for ones that overlap with GT and check if
    ad's direction matches the annotated direction '''
print("\n\nProcessing data...")

correct_dir_cnt = 0
fp_cnt = 0
fn_cnt = 0
wrong_dir_count = 0
dir_not_detected_cnt = 0
# print(detection_boxes)
total = len(detection_boxes)
cur_cnt = 0
for det_img in detection_boxes:
    cur_cnt +=1
    image = cv2.imread(os.path.join(img_folder_path,det_img),cv2.IMREAD_COLOR)
    # print(len(detection_boxes[det_img]))
    for i in range(len(detection_boxes[det_img])):
        # print(detection_boxes[det_img][i])
        det_obj_dir = int(detection_boxes[det_img][i][4])
        det_obj_box = [detection_boxes[det_img][i][0], detection_boxes[det_img][i][1], detection_boxes[det_img][i][2], detection_boxes[det_img][i][3]]
        # print(det_obj_box)
        # print(str(det_img) + " " + str(gt_boxes[det_img]))
        for i in range(len(gt_boxes[det_img])):
            gt_obj_dir = int(gt_boxes[det_img][i][4])
            gt_obj_box = [gt_boxes[det_img][i][0], gt_boxes[det_img][i][1], gt_boxes[det_img][i][2], gt_boxes[det_img][i][3]]
            if IOU(det_obj_box, gt_obj_box) > 0.5:
                if det_obj_dir == direction_map[int(gt_obj_dir)]:
                    correct_dir_cnt += 1

                elif det_obj_dir == -1:
                    dir_not_detected_cnt += 1

                else:
                    wrong_dir_count += 1

                '''visualize gt direction and detected direction together'''
                    # cv2.rectangle(image,(det_obj_box[0],det_obj_box[1]),(det_obj_box[2],det_obj_box[3]),(0,0,255),3) #BGR
                    # cv2.rectangle(image,(gt_obj_box[0],gt_obj_box[1]),(gt_obj_box[2],gt_obj_box[3]),(255,0,0),3) #BGR
                    # cv2.putText(image, (str(direction_map[int(gt_obj_dir)]) + " " + str(det_obj_dir)), (gt_obj_box[0],gt_obj_box[1]-5), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255))
                    # cv2.imshow("test", image)
                    # cv2.waitKey(0)
    print("total: {} count: {}".format(total,cur_cnt), end='\r', flush=True)
    

print("Total Detected Vehicle Count {} \n Correct Dir Det Count : {} \n Wrong Dir Det Count : {} \n Dir Not Detected Count : {}".format(obj_count, correct_dir_cnt, wrong_dir_count, dir_not_detected_cnt))
print("dir accuracy rate : {accuracy:.4f}".format(accuracy=correct_dir_cnt/(correct_dir_cnt+wrong_dir_count))) #out of the confident network dir output, what percentage were right?
print("dir detection rate : {accuracy:.4f}".format(accuracy=(obj_count-dir_not_detected_cnt)/obj_count)) #out of all the objects, how many did the model provide a dir output?  (either right or wrong)
# print("dir accuracy rate : {accuracy:.4f}".format(accuracy=correct_dir_cnt/obj_count))





    #     if prev_name != image_name:
    #         # print("COUNT " + str(count) + "***********")
    #         # print("prev " + prev_name)
    #         # print("curr " + image_name)
    #         count += 1

    #     prev_name = image_name
    #     # print(image_name)
    #     # print("Line{}: {}".format(count, line.strip()))
    # print("image_cnt is " + str(count) ) 

    # if modified: 
    #     cv2.imwrite(os.path.join(img_copy_path,imgName),image)
    #     print("{}/{}  {}".format(index,len(xml_names),os.path.join(img_copy_path,imgName)))
    #     modified=0

