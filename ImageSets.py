#! python3
import os, sys
import shutil
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-mf', required=True)
parser.add_argument('-output', required=False) #where we want to move the desired images to
# parser.add_argument('-jpgs', required=True)
# parser.add_argument('-output', required=True)


args = parser.parse_args()


#folder containing JPEGImages and Annotations
main_folder = args.mf
output_path = args.output

#folder name with JPEGImages
img_folder = os.path.join(main_folder, 'JPEGImages')
anno_folder = os.path.join(main_folder, 'Annotations')

#list of all the JPEGImages and annotations in the folders
imgs = []
imgs = os.listdir(img_folder)
annos = []
annos = os.listdir(anno_folder)

#path for ImageSets
ImageSets = os.path.join(main_folder, 'ImageSets')

# create all.txt file
if not os.path.exists(ImageSets):
    os.mkdir(ImageSets)   

annos.sort()
imgs.sort()

# with open(os.path.join(ImageSets, 'all.txt'), 'a+') as f1:
#     # for img in imgs:
#     #     f1.write(img[:-4])
#     #     f1.write("\n")    
count =0
print("annos = " + str(len(annos)))
print("imgs = " + str(len(imgs)))
img_type = imgs[0][len(imgs[0])-4:]
if(len(annos) == len(imgs)):
    #create all.txt and fill it with Image names

    for i in range(len(annos)) :
        # print(annos[i])
        # print(imgs[i])
        if(annos[i][:-4] == imgs[i][:-4]):
            count+=1
            print(annos[i])
            print(imgs[i])
            if(annos[i][:-4]=="desktop" or imgs[i][:-4]=="desktop"):
                print(imgs[i][:-4])
                print(annos[i][:-4])
                break
    print("count is " + str(count))
    print("anno_len : " + str(len(annos)))
    print("imgs_len : " + str(len(imgs)))
    with open(os.path.join(ImageSets, 'all.txt'), 'a+') as f1:
        for img in imgs:
            # if(annos[i][:-4]=="desktop" or imgs[i][:-4]=="desktop"):
            #     print(imgs[i])
            #     print(annos[i])
            #     os.remove(os.path.join(anno_folder, annos[i]))
            #     os.remove(os.path.join(img_folder, imgs[i]))
            #     break
            # else:
            f1.write(img[:-4])
            f1.write("\n")
    
    

else:
    # for i in range(max(len(imgs),len(annos))) :
    with open(os.path.join(ImageSets, 'all.txt'), 'a+') as f1:
        for i in range(len(annos)) :
            # print(os.path.join(img_folder, annos[i][:-4]+".jpg"))
            # if(annos[i][:-4]=="desktop" or imgs[i][:-4]=="desktop"):
            #         print(imgs[i][:-4])
            #         print(annos[i][:-4])
            if not os.path.isfile(os.path.join(img_folder, annos[i][:-4]+img_type)): #if corresponding jpg does not exist, skip
                # shutil.move( os.path.join(img_folder, imgs[i]), os.path.join(output_path, imgs[i]))                
                continue
            else: #for cases where corresponding jpg does exist add it to all.txt
                # print(annos[i][:-4]+".jpg")
                count+=1
                f1.write(annos[i][:-4]+"\n")
                    # f1.write("\n")

        # elif(annos[i][:-4] != imgs[i][:-4]):
        #     # print("******************************************************")
        #     print(annos[i])
        #     print(imgs[i])
        #     # break
        #     # print()
        #     answer = input("Would you like to remove the image " + imgs[i] + "?")
        #     # print(answer)
        #     if(answer=='y'):
        #         os.remove(os.path.join(img_folder, imgs[i]))
        #     # print()
        #     answer2 = input("Would you like to remove " + annos[i] + "?")
        #     if(answer2=='y'):
        #         os.remove(os.path.join(anno_folder, annos[i]))
        #     # break
            print("current count :" + str(count), end ='\r')
print("count :" + str(count))


# for img in imgs:
#     # f1.write(img)
#     print(img[:-4])
