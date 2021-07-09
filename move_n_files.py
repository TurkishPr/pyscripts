import glob
import os
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True) #main folder  we copy from
parser.add_argument('-out_path', required=True) #where we want to move the desired files to
parser.add_argument('-num', required=True) #number of files we want
args = parser.parse_args()

main_folder = args.mf
output_path = args.out_path
num = int(args.num)

input_xml_path = os.path.join(main_folder, "Annotations")
input_img_path = os.path.join(main_folder, "JPEGImages")

output_xml_path = os.path.join(output_path, "Annotations")
output_img_path = os.path.join(output_path, "JPEGImages")


if not os.path.exists(output_xml_path):
    os.mkdir(output_xml_path)
if not os.path.exists(output_img_path):
    os.mkdir(output_img_path)

target_images = glob.glob(input_img_path+"/*.jpg")
total = len(target_images)
count=0
for i in target_images:
    # print(os.path.basename(i)) 
    target_image_base = os.path.basename(i)[:-4]
    # print(target_image_base)
    # print(os.path.join(input_path, target_image_base+'.jpg'))
    if os.path.isfile(os.path.join(output_img_path, target_image_base+".jpg")): #move only if the file does not already exist at destination
        count+=1
        continue
    else:
        shutil.copyfile( os.path.join(input_xml_path, target_image_base+'.xml'), os.path.join(output_xml_path, target_image_base+'.xml') )
        shutil.copyfile( os.path.join(input_img_path, target_image_base+'.jpg'), os.path.join(output_img_path, target_image_base+'.jpg') )
    count+=1
    print("total: {} count: {}".format(total,count), end='\r', flush=True)


        #os.remove( os.path.join(input_path, target_image_base) )
        #cmd = "copy {0} {1}".format(os.path.join(input_path, target_image_base), os.path.join(output_path, target_image_base))
        #os.system(cmd)
        # shutil.copyfile( os.path.join(input_path, target_image_base+'.png'), os.path.join(output_path, target_image_base+'.png') )
        # shutil.move( os.path.join(input_path, target_image_base+'.jpg'), os.path.join(output_path, target_image_base+'.jpg') )
        # os.remove( os.path.join(input_path, target_image_base+'.jpg'))
    if count == num:
        break