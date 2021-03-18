#! python3
import os, sys
from os import system, name
import json
import numpy as np
import cv2
import glob
import shutil
import argparse
import matplotlib.pyplot as plt
import numpy 


#DETLOG LOCATION Z:\seongjin.lee\udb

'''
PER CLASS : CONF, OCC, TRUNC





PAN CLASS : CONF, OCC, TRUNC
'''



parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=False)

classes = {
    1 : "PED",
    2 : "RIDER",
    3 : "CAR",
    4 : "TRUCK",
    5 : "BUS",
}

#nested dict to save statistics
gt_stats = {
    "PED" : {"0": 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0,},
    "RIDER" : {"0": 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0,},
    "CAR" : {"0": 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0,},
    "TRUCK" : {"0": 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0,},
    "BUS" : {"0": 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0,},
}

gt_conf_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}
gt_occ_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}
gt_trunc_stats = {
    "PED" : [],
    "RIDER" : [],
    "CAR" : [],
    "TRUCK" : [],
    "BUS" : [],
    "ALL" : [],
}



#if argument is given, use that
#if not give, use default
args = parser.parse_args()
main_folder = ""
if type(args.mf) == type(None):
    # main_folder = r"Z:\seongjin.lee\eval\M551_improvement\only_conf\1600000"
    # output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics\\prefix_only_conf_model_output"
    # tag = "conf_only"


    main_folder = r"C:\Users\Yoseop\Desktop\Personal\OD_Work\ZF\Softlabel\prefix_0.3_eval\Eval"
    output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics\\prefix_0.3_model_output"
    tag = "0_3"

    # main_folder = r"Z:\seongjin.lee\eval\M551_improvement\original\final"
    # output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics\original_model_output"
    # tag = "original"

    # main_folder = r"Z:\seongjin.lee\udb\GODTrain200929_refine_result_ver3"
    # output_folder = "C:\\Users\\Yoseop\\Desktop\\Personal\\OD_Work\\ZF\\Softlabel\\statistics"

    # main_folder = r"C:\Users\Yoseop\Desktop\erase\test\detlog"
else:
    main_folder = args.mf
print(main_folder)

count =0
total = 411719
# print(len(glob.glob(main_folder+"\\*")))

# '''
# detection log per class
# '''
for src in glob.glob(main_folder+"\\*.txt"): #conf, trunc, occ scores
    name = src.rsplit("\\")[-1][:-4].upper()
    if "PROPOSAL" in name or "TS" in name or "TL" in name:
        continue
    f = open(src, "r")
    print(src)
    print(name)

    for line in f:
        info = line.split()
        conf = float(info[1])

        gt_conf_stats[name].append(conf)
        gt_conf_stats["ALL"].append(conf)



'''
detection log per image
'''
# for src in glob.glob(main_folder+"\\*"): #conf, trunc, occ scores
#     # print(src)
#     f = open(src, "r")
#     for line in f:
#         info = line.split()
#         det_cls = int(info[0])
#         conf = float(info[1])
#         det_box = [float(info[2]),float(info[3]),float(info[4]),float(info[5])]
#         conf = float(info[1])
#         occ = float(info[6])
#         trunc = float(info[7])
#         name = classes[det_cls]
        
#         gt_conf_stats[name].append(conf)
#         gt_conf_stats["ALL"].append(conf)

#         if occ != -1 and occ != 0:
#             gt_occ_stats[name].append(occ)
#             gt_occ_stats["ALL"].append(occ)

#         if trunc != -1 and trunc != 0:
#             gt_trunc_stats[name].append(trunc)
#             gt_trunc_stats["ALL"].append(trunc)

#     count +=1
#     f.close()
#     print("{} : {}".format(total,count), end ='\r')

for key1, value1 in gt_conf_stats.items():
    print(key1 + " " + str(len(value1)))

for key, value in gt_conf_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=50)
    plt.gca().set(title='Conf Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\CONF_{}_{}.png".format(key.upper(), tag)
    plt.savefig(filename)
    plt.close()

for key, value in gt_occ_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=50)
    plt.gca().set(title='Occ Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\OCC_{}_{}.png".format(key.upper(), tag)
    plt.savefig(filename)
    plt.close()


for key, value in gt_trunc_stats.items():
    # print(key + " " + str(value))
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    arr = numpy.array(value)
    plt.hist(arr, bins=50)
    plt.gca().set(title='Trunc Histogram of {}'.format(key), ylabel='Frequency')
    filename = output_folder + "\\TRUNC_{}_{}.png".format(key.upper(), tag)
    plt.savefig(filename)
    plt.close()


#write stats to file
with open(output_folder + "\\conf.txt", 'w') as f:
    for key, value in gt_conf_stats.items():
        f.write("%s\n" % key)
        for item in value:
            f.write("%s," % item)
        f.write("\n")
    f.close()


with open(output_folder + "\\trunc.txt", 'w') as f:
    for key, value in gt_trunc_stats.items():
        f.write("%s\n" % key)
        for item in value:
            f.write("%s," % item)
        f.write("\n")
    f.close()

with open(output_folder + "\\occ.txt", 'w') as f:
    for key, value in gt_occ_stats.items():
        f.write("%s\n" % key)
        for item in value:
            f.write("%s," % item)
        f.write("\n")
    f.close()






