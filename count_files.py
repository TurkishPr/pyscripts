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
# parser.add_argument('-out', required=True)

args = parser.parse_args()
main_folder = args.mf

directories = glob.glob(main_folder+"\*")

# print(directories)
count = 0
for dir in directories :
    count += len(glob.glob(dir+"\*"))
print(count)