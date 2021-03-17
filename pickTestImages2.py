#! python2
import os, sys
import shutil
import json
from xml.dom import minidom


main_folder = r'C:\Users\YoseopKim\Desktop\Personal\OD_Work\Roadmark\roadmarktrain191002\Annotations'
img_copy_path = os.path.join( main_folder[:-11], "bump_images_only")
img_folder_path = os.path.join(main_folder[:-11], "JPEGImages")
print(img_copy_path)
print(img_folder_path)

# single_file = r'C:\Users\YoseopKim\Desktop\Personal\OD_Work\Roadmark\roadmarktrain191002\Annotations\201706_hoo.kim_gopr1330.mp4_01190.xml'
if not os.path.exists(img_copy_path):
    os.mkdir(img_copy_path)
xml_names = os.listdir(main_folder)
filePaths = list(range(len(xml_names)))

index=0
for xml in xml_names:
    # if str(record)=="xml":
    #     continue
    filePaths[index] = os.path.join(main_folder , xml)
    index+=1

# print(xml_names)
xml_index =0

for one_xml in filePaths:
    
    xml = minidom.parse(one_xml)
    itemlist = xml.getElementsByTagName('name')
    # print(xml)
    for s in itemlist:
        if s.childNodes[0].data == 'roadmark__bump':
            # print(one_xml)
            print(s.childNodes[0].data)

    ##finding cases of two object appearance
    # crosswalk_found = 0
    # bump_found = 0
    # for s in itemlist:
    #     if s.childNodes[0].data == 'roadmark_crosswalk':
    #         crosswalk_found = 1
    #         if bump_found:
    #             shutil.copy(os.path.join(os.path.join(main_folder[:-11], "JPEGImages") ,xml_names[xml_index][:-4]+".jpg"), img_copy_path+"/"+xml_names[xml_index][:-4]+".jpg")


    #     elif s.childNodes[0].data == 'roadmark__bump':
    #         bump_found = 1
    #         if crosswalk_found:
    #             shutil.copy(os.path.join(os.path.join(main_folder[:-11], "JPEGImages") ,xml_names[xml_index][:-4]+".jpg"), img_copy_path+"/"+xml_names[xml_index][:-4]+".jpg")

    # crosswalk_found =0
    # bump_found =0
    # xml_index+=1



    # ##finding cases of single object appearance
    # for s in itemlist:
    #     if s.childNodes[0].data == 'roadmark__bump':
    #         # print(one_xml)
    #         # print(s.childNodes[0].data)
    #         shutil.copy(os.path.join(os.path.join(main_folder[:-11], "JPEGImages") ,xml_names[xml_index][:-4]+".jpg"), img_copy_path+"/"+xml_names[xml_index][:-4]+".jpg")
    #         # shutil.copy(os.path.join(main_folder ,xml_names[xml_index]), img_copy_path+"/"+xml_names[xml_index])

    #         # print( img_copy_path+"/"+xml_names[xml_index][:-4]+".jpg")
    #         # print()
    # xml_index+=1



