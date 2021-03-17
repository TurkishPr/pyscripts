import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageOps

od_class = {
    'ped': 1,
    'rider':2,
    'car':3, 
    'truck':4,
    'bus':5,
    'TSC':6,
    'TST':7,
    'TSR':8,
    'TL':9,
    '0':0,
    'TS_etc':12,
    'TL_etc':13,
    'TS_fa':14,
    'TL_fa':15,
}

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
args = parser.parse_args()

main_folder = args.mf

cls_folders = os.listdir(main_folder)

fn_stats = {}
single_stat = {}

for cls in cls_folders:
    fnCnt=0
    imgName=''
    single_cls_folder = os.path.join(main_folder, cls)
    fn_info_file = os.path.join(single_cls_folder,os.path.join('ImageSets','all.txt.checked.txt'))
    print(fn_info_file)
    img_copy_path = os.path.join(single_cls_folder, "fn_cls_n_conf")
    if not os.path.exists(img_copy_path):
        os.mkdir(img_copy_path)
    with open(fn_info_file, "r") as file:
        for line in file:
            if line[len(line)-4:-1]=='jpg': #if line is JPEG file name
                imgName = line[:-1]
                fnCnt=0 #since it is a new JPG, we reset fnCnt
                # print(imgName)
            elif len(line)>5: #if line is gt and fn data
                gt_cls=int(line.rsplit(' ')[0])
                if gt_cls != 21:
                    fnCnt+=1
                    xmin=int(float(line.rsplit(' ')[1]))
                    ymin=int(float(line.rsplit(' ')[2]))
                    xmax=int(float(line.rsplit(' ')[3]))
                    ymax=int(float(line.rsplit(' ')[4]))
                    fn_cls=int(line.rsplit(' ')[5])
                    fn_scr=float(line.rsplit(' ')[6][1:-2])
                    fn_cls_name = list(od_class.keys())[list(od_class.values()).index(fn_cls)]
                    gt_cls_name = list(od_class.keys())[list(od_class.values()).index(gt_cls)]

                    # print(gt_cls)
                    # print(xmin)
                    # print(ymin)
                    # print(xmax)
                    # print(ymax)
                    # print(fn_cls)
                    # print(fn_scr)
                    # blank = Image.new('RGB', (200,230), (0,0,0)) ##create a blank black image
                                        
                    if gt_cls_name.lower() == fn_cls_name.lower(): #conf 나눠먹기된 경우
                        if gt_cls_name in single_stat:
                            single_stat[gt_cls_name] +=1
                        else:
                            single_stat[gt_cls_name] = 1
                            
                    else: # 다른 cls로 잘 못 검출한 경우
                        if fn_cls_name in single_stat:
                            single_stat[fn_cls_name] +=1
                        else:
                            single_stat[fn_cls_name] = 1
                    
                    '''how much we should crop each side'''
                    xc1 = (ymax-ymin)/3
                    xc2 = (ymax-ymin)/3
                    yc1 = (xmax-xmin)/3
                    yc2 = (xmax-xmin)/3

                    # blank.show()
                    image = cv2.imread(os.path.join(single_cls_folder,'JPEGImages\\')+imgName) #open image
                    # cv2.rectangle(image,(xmin,ymin),(xmax,ymax-10),(0,0,255),1) #draw bbox of gt in question
                    # cv2.putText(image, "[{} -> {} {:.2f}]".format(gt_cls_name,fn_cls_name,fn_scr),  (int(xmin), int(ymin+((ymax-ymin)/2))-5), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )
                    # cv2.putText(image, "[{}]".format(gt_cls_name),  (int(xmin), int(ymax)) , cv2.FONT_HERSHEY_PLAIN, 1, (161,146,137), 2 )
                    h, w, c = image.shape #image dimensions
                    height = ymax-ymin #width of FN
                    width = xmax-xmin #height of FN
                    '''resize images'''
                    # if .8<(height/width)<1.2 or .8<(width/height)<1.2:#fn dimension is rougly square 
                    #y1 y2 x1 x2 are bbox for cropping
                    y1 = int(ymin-yc1) 
                    y2 = int(ymax+yc2)
                    x1 = int(xmin-xc1)
                    x2 = int(xmax+xc2)
                    x1_diff_from_origin = int(xmin-xc1)   
                    x2_diff_from_origin = int(xmin-xc2)
                    y1_diff_from_origin = int(ymin-yc1)
                    y2_diff_from_origin = int(ymin-yc2)
                    if y1 < 0:
                        y1_diff_from_origin = 0
                        y2_diff_from_origin = 0
                        y1 = 0
                    if y2 > h:
                        y2 = h
                    if x1 < 0:
                        x1_diff_from_origin = 0
                        x2_diff_from_origin = 0
                        x1 = 0
                    if x2 > w:
                        x2 = w
                    '''altered bbox after cropping and resizing'''
                    # print(xmin)
                    # print(xmax)
                    # print(ymin)
                    # print(ymax)
                    xratio = (x2-x1)/200
                    yratio = (y2-y1)/200
                    x1_a = int(xmin-x1_diff_from_origin)
                    x2_a = int(xmax-x2_diff_from_origin)
                    y1_a = int(ymin-y1_diff_from_origin)
                    y2_a = int(ymax-y2_diff_from_origin)

                    roi = image[y1:y2, x1:x2]#crop the fn 
                    # cv2.imshow("cropped",roi)
                    res = cv2.resize(roi, dsize=(200, 200), interpolation=cv2.INTER_CUBIC)
                    cv2.rectangle(res,(int(x1_a/xratio),int(y1_a/yratio)),(int(x2_a/xratio),int(y2_a/yratio)),(0,0,255),2) #draw bbox of gt in question
                    # print("{}->{}".format(xmin ,x1_a))
                    # print("{}->{}".format(xmax ,x2_a))
                    # print("{}->{}".format(ymin ,y1_a))
                    # print("{}->{}".format(ymax ,y2_a))
                    # print(type(res))
                    img = np.ones([230,200,3], dtype=np.uint8)*0
                    # cv2.imshow("black", img)
                    # cv2.imshow("Image",res)
                    # cv2.imshow("Image",res)
                    img[0:199,0:199] = res[0:199,0:199]
                    # cv2.imshow("copied",img)
                    # cv2.waitKey(0)

                    res = Image.fromarray(res)
                    # print(type(res))
                    # inverted_image = ImageOps.invert(res)
                    # inverted_image.show()
                    # cv2.imshow("Image",res)
                    # blank.paste(res)
                    # d = ImageDraw.Draw(blank)
                    # d. text((5,210), "[{} -> {} {:.2f}]".format(gt_cls_name,fn_cls_name,fn_scr), fill=(255, 48, 48))
                    cv2.putText(img, "{} -> {} {:.2f}".format(gt_cls_name,fn_cls_name,fn_scr),  (5, 220), cv2.FONT_HERSHEY_PLAIN, 1, (48, 48, 255), 2 )

                    # blank.show()
                    # cv2.imshow("resized",blank)
                    # cv2.waitKey(0)



                    # elif width > height:
                    #     #y1 y2 x1 x2 are bbox for cropping
                    #     y1 = int(ymin-yc1) 
                    #     y2 = int(ymax+yc2)
                    #     x1 = int(xmin-xc1)
                    #     x2 = int(xmax+xc2)
                    #     x1_diff_from_origin = int(xmin-xc1)   
                    #     x2_diff_from_origin = int(xmin-xc2)
                    #     y1_diff_from_origin = int(ymin-yc1)
                    #     y2_diff_from_origin = int(ymin-yc2)
                    #     if y1 < 0:
                    #         y1_diff_from_origin = 0
                    #         y2_diff_from_origin = 0
                    #         y1 = 0
                    #     if y2 > h:
                    #         y2 = h
                    #     if x1 < 0:
                    #         x1_diff_from_origin = 0
                    #         x2_diff_from_origin = 0
                    #         x1 = 0
                    #     if x2 > w:
                    #         x2 = w
                    #     '''altered bbox after cropping and resizing'''
                    #     print(xmin)
                    #     print(xmax)
                    #     print(ymin)
                    #     print(ymax)
                    #     xratio = (x2-x1)/200
                    #     yratio = (y2-y1)/200
                    #     x1_a = int(xmin-x1_diff_from_origin)
                    #     x2_a = int(xmax-x2_diff_from_origin)
                    #     y1_a = int(ymin-y1_diff_from_origin)
                    #     y2_a = int(ymax-y2_diff_from_origin)

                    #     roi = image[y1:y2, x1:x2]#crop the fn 
                    #     cv2.imshow("cropped",roi)
                    #     res = cv2.resize(roi, dsize=(200, 200), interpolation=cv2.INTER_CUBIC)
                    #     cv2.rectangle(res,(int(x1_a/xratio),int(y1_a/yratio)),(int(x2_a/xratio),int(y2_a/yratio)),(0,0,255),2) #draw bbox of gt in question
                    #     print("{}->{}".format(xmin ,x1_a))
                    #     print("{}->{}".format(xmax ,x2_a))
                    #     print("{}->{}".format(ymin ,y1_a))
                    #     print("{}->{}".format(ymax ,y2_a))
                    #     cv2.imshow("resized",res)
                    #     cv2.waitKey(0)
                    # else: #height > width
                    #     x1 = int(xmin-(ymax-ymin)/3)
                    #     x2 = int(xmax+(ymax-ymin)/3)
                    #     if x1 < 0:
                    #         x1 = 0
                    #     if x2 > w:
                    #         x2 = w
                    #     roi = image[ymin:ymax, x1:x2]#crop a square around bbox
                    #     cv2.imshow("cropped",roi)
                    #     ratio = (ymax-ymin)/200
                    #     res = cv2.resize(roi, dsize=(int((x2-x1)/ratio),200), interpolation=cv2.INTER_CUBIC)
                    #     cv2.imshow("resized",res)
                    #     cv2.waitKey(0)
                    if fnCnt==1:
                        cv2.imwrite(os.path.join(img_copy_path,imgName),img) #save image to file
                        # blank.save(os.path.join(img_copy_path,imgName))
                    else:
                        # print(img_copy_path,imgName[:-4])
                        cv2.imwrite(os.path.join(img_copy_path,imgName[:-4]+"_"+str(fnCnt)+".jpg"),img) #save image to file
                        # blank.save(os.path.join(img_copy_path,imgName[:-4]+"_"+str(fnCnt)+".jpg"))
                        # print("more than one fn")
                
                    # cropped

    fn_stats[cls] = single_stat
    single_stat = {}
# print("TL ***********************")
# for key, value in fn_stats['TL'].items():
#     print("{} {}".format(key,value))

    # print(fn_stats)
for cls in cls_folders:
    print(cls + " ***********************")
    for key, value in fn_stats[cls].items():
        print("{} {}".format(key,value))



        # print(line)
    # imgName = file.readline()
    # cnt = int(file.readline())
    # print(imgName)
    # print(cnt)
    # for i in range(cnt):
    #     print(file.readline())
    # restOfFile = file.read()
    # print(count)
    # print(restOfFile)
