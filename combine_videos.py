import os, sys
import glob
import shutil
import argparse
import subprocess

'''Arguments'''
parser = argparse.ArgumentParser()
parser.add_argument('-input1', required=True)
parser.add_argument('-input2', required=True)
parser.add_argument('-output', required=True)
# parser.add_argument('-combined_log_path', required=True)
args = parser.parse_args()

input_path1 = args.input1
input_path2 = args.input2
output_folder_name = args.output

main_path = input_path1.rsplit('\\',1)[0]
output_path = os.path.join(main_path,output_folder_name)
if not os.path.exists(output_path):
    os.mkdir(output_path)
    

input1_list = os.listdir(input_path1)
input2_list = os.listdir(input_path2)
for input in input1_list: #if file is not a vid file, get rid of it from the list
    # print(input.rsplit('.',1)[0])
    if input.rsplit('.',1)[1]!="avi":
        input1_list.remove(input)
for input in input2_list:
    if input.rsplit('.',1)[1]!="avi":
        input2_list.remove(input)


for input in input1_list:
    subprocess.call("ffmpeg -i {} -i {} -filter_complex hstack -c:v ffv1 {}".format(os.path.join(input_path1, input), os.path.join(input_path2, input), os.path.join(output_path,input.rsplit('.',1)[0]+"_combined.avi")) )



# print(input1_list)
# print(input2_list)

# if not os.path.exists(output_path):
#     os.mkdir(output_path)


# inference_arg = input_path + " \" \" " + output_path + " -"

#run inference tools
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
# subprocess.call(r"C:\Users\Yoseop\Desktop\SV\svnet3\tools\algo_tools\dist/pyalgo_test.exe " + inference_arg)
# subprocess.call("license_plate.exe " + inference_arg)
# subprocess.call("roadmark.exe " + inference_arg)