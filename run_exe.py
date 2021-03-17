import os, sys
import glob
import shutil
import argparse
import subprocess

'''Arguments'''
parser = argparse.ArgumentParser()
parser.add_argument('-input', required=True)
parser.add_argument('-output', required=True)
# parser.add_argument('-combined_log_path', required=True)
args = parser.parse_args()

input_path = args.input
output_path = args.output
# combined_log_path = args.combined_log_path
# video_path = r"C:\Users\Yoseop\Desktop\"
# output_path = r"C:\Users\Yoseop\Desktop/"
# combined_log_path = r"C:\Users\Yoseop\Desktop\combined"
if not os.path.exists(output_path):
    os.mkdir(output_path)
# if not os.path.exists(combined_log_path):
#     os.mkdir(combined_log_path)

inference_arg = input_path + " \" \" " + output_path + " -"

#run inference tools
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
subprocess.call("license_plate.exe " + inference_arg)
subprocess.call("roadmark.exe " + inference_arg)
subprocess.call("sod.exe " + inference_arg)