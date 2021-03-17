import glob
import os
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-input', required=True) #pool we copy from
parser.add_argument('-output', required=True) #where we want to move the desired files to
parser.add_argument('-target', required=True) #the files we want
args = parser.parse_args()

input_path = args.input
output_path = args.output
target_path = args.target

target_images = glob.glob(target_path+"/*.jpg")
# target_images = glob.glob(target_path+"/*.xml")

count=0
for i in target_images:
    # print(os.path.basename(i)) 
    target_image_base = os.path.basename(i)[:-4]
    # print(target_image_base)
    # print(os.path.join(input_path, target_image_base+'.jpg'))
    shutil.copyfile( os.path.join(input_path, target_image_base+'.xml'), os.path.join(output_path, target_image_base+'.xml') )
    if os.path.isfile(os.path.join(input_path, target_image_base+'.jpg')):
        count+=1
        #os.remove( os.path.join(input_path, target_image_base) )
        #cmd = "copy {0} {1}".format(os.path.join(input_path, target_image_base), os.path.join(output_path, target_image_base))
        #os.system(cmd)
        # shutil.copyfile( os.path.join(input_path, target_image_base+'.png'), os.path.join(output_path, target_image_base+'.png') )
        # shutil.move( os.path.join(input_path, target_image_base+'.jpg'), os.path.join(output_path, target_image_base+'.jpg') )
        # os.remove( os.path.join(input_path, target_image_base+'.jpg'))

    '''    
    if not os.path.isfile(os.path.join(input_path, target_image_base)):
        count+=1
        shutil.copyfile( os.path.join(target_path, target_image_base), os.path.join(output_path, target_image_base) )
    '''    
    print(count, end='\r')
print(count)