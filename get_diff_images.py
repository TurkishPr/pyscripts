#get different images

import glob
import os
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-i1', required=True) #input list 1 dir
parser.add_argument('-12', required=True) #input lsit 2 dir
parser.add_argument('-o', required=True) #dir we copy to
args = parser.parse_args()

input_one = args.i1
input_two = args.i2
output = args.o

inputlist_one = glob.glob(input_one+"/*.jpg")
inputlist_two = glob.glob(input_two+"/*.jpg")
# target_images = glob.glob(target_path+"/*.xml")

count=0
if len(inputlist_one > inputlist_two):
    for i in inputlist_one:
        # print(os.path.basename(i)) 
        image_base = os.path.basename(i)[:-4]
        ext = os.path.basename[i][len(image_base):]
        print(ext)
        # print(target_image_base)
        # print(os.path.join(input_path, target_image_base+'.jpg'))
        # shutil.copyfile( os.path.join(input_path, image_base+'.xml'), os.path.join(output_path, image_base+'.xml') )
        if not os.path.isfile(os.path.join(input_two, image_base+'.jpg')) and not os.path.isfile(os.path.join(input_two, image_base+'.png')):
            count+=1
            #os.remove( os.path.join(input_path, target_image_base) )
            #cmd = "copy {0} {1}".format(os.path.join(input_path, target_image_base), os.path.join(output_path, target_image_base))
            #os.system(cmd)
            shutil.copyfile( os.path.join(input_one, image_base+'.png'), os.path.join(output, image_base+'.png') )
            # shutil.move( os.path.join(input_path, target_image_base+'.jpg'), os.path.join(output_path, target_image_base+'.jpg') )
            # os.remove( os.path.join(input_path, target_image_base+'.jpg'))

        print(count, end='\r')
else:
    for i in inputlist_two:
        # print(os.path.basename(i)) 
        image_base = os.path.basename(i)[:-4]
        ext = os.path.basename[i][:4]
        # print(target_image_base)
        # print(os.path.join(input_path, target_image_base+'.jpg'))
        # shutil.copyfile( os.path.join(input_path, image_base+'.xml'), os.path.join(output_path, image_base+'.xml') )
        if not os.path.isfile(os.path.join(input_two, image_base+'.jpg')) and not os.path.isfile(os.path.join(input_two, image_base+'.png')):
            count+=1
            #os.remove( os.path.join(input_path, target_image_base) )
            #cmd = "copy {0} {1}".format(os.path.join(input_path, target_image_base), os.path.join(output_path, target_image_base))
            #os.system(cmd)
            shutil.copyfile( os.path.join(input_one, image_base+'.png'), os.path.join(output, image_base+'.png') )
            # shutil.move( os.path.join(input_path, target_image_base+'.jpg'), os.path.join(output_path, target_image_base+'.jpg') )
            # os.remove( os.path.join(input_path, target_image_base+'.jpg'))

    print(count, end='\r')

print(count)