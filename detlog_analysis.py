#! python3
import os, sys
from os import system, name
import json
import numpy as np
import cv2
import glob
import shutil
import argparse


#DETLOG LOCATION Z:\seongjin.lee\udb

'''
PER CLASS : CONF, OCC, TRUNC

or

PAN CLASS : CONF, OCC, TRUNC
'''



parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=False)


#if argument is given, use that
#if not give, use default
args = parser.parse_args()
main_folder = ""
if type(args.mf) == type(None):
    # main_folder = r"Z:\seongjin.lee\udb\GODTrain200929_refine_result_ver3"
    main_folder = r"C:\Users\Yoseop\Desktop\erase\test\detlog"
else:
    main_folder = args.mf
print(main_folder)
# print(len(glob.glob(main_folder+"\\*")))
for src in glob.glob(main_folder+"\\*"): #conf, trunc, occ scores
    print(src)
    f = open(src, "r")
    for line in f:
        info = line.split()
        det_cls = int(info[0])
        conf = float(info[1])
        det_box = [float(info[2]),float(info[3]),float(info[4]),float(info[5])]
        conf = float(info[1])
        occ = float(info[6])
        trunc = float(info[7])
        print(det_cls, conf, det_box, occ, trunc)
    f.close()


