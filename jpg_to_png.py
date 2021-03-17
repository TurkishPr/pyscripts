import os, sys
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageOps

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
args = parser.parse_args()
main_folder = args.mf
imgCount = len(os.listdir(main_folder))
count =0
for src in glob.glob(main_folder+"\\*"):
    imageName = src.rsplit("\\")[-1]
    path = src.rsplit('JPEGImages')[0]
    pngPath = os.path.join(path,"png_converted")
    if not os.path.exists(pngPath):
        os.mkdir(pngPath)

    image = Image.open(src)
    image.save(os.path.join(path,os.path.join("png_converted", imageName[:-4]+".png")))
    count+=1
    print("{}/{}  {} \r".format(count,imgCount,imageName[:-4]+".png"), end='\r', flush=True)