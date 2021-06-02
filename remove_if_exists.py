import glob
import os
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-local', required=True) #folder with files we want to erase
parser.add_argument('-remote', required=True) #where we want check if files-to-erase exist
parser.add_argument('-target', required=False) #the files we want
args = parser.parse_args()

local = args.local
remote = args.remote
target_path = args.target

files_to_erase = glob.glob(local+'/*')
# target_images = glob.glob(target_path+"/*.xml")

count=0
for i in files_to_erase:
    # print(os.path.basename(i))
    # print(i)
    local_file_name = os.path.basename(i)
    # print(local_file_name)
    if os.path.isfile(os.path.join(remote, local_file_name)):
        print("File " + local_file_name + " exists in remote")
        os.remove(i)
        print("Removed " + i + " from local storage")
        count+=1
    # print(os.path.join(input_path, target_image_base+'.jpg'))
    # shutil.copyfile( os.path.join(input_path, target_image_base+'.xml'), os.path.join(output_path, target_image_base+'.xml') )
    # if os.path.isfile(os.path.join(input_path, target_image_base+'.jpg')):
    #     count+=1
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