#! python3
import os, sys
# from posix import XATTR_SIZE_MAX
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
# parser.add_argument('-img_folder', required=True)
# parser.add_argument('-json_folder', required=True)

args = parser.parse_args()
main_folder = args.mf
# img_folder = args.img_folder
# json_folder = args.json_folder

file_list = glob.glob(main_folder+"\*")

for file in file_list:
    # print(file)
    fileName = os.path.basename(file)
    # print(fileName)
    subFolder = fileName.split('post_')[-1]
    subFolder = subFolder.rsplit('_iter')[0]
    print(subFolder)
    # if len(subFolder) > 3 :
    # print(str(subFolder[3]))

    if not os.path.exists(os.path.join(main_folder, str(subFolder))):
        os.mkdir(os.path.join(main_folder, str(subFolder)))
    
    shutil.move(file, os.path.join(main_folder, str(subFolder)))
