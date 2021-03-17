#! python2
import os, sys
import shutil
import json
from xml.dom import minidom
from lxml import etree as ET

'''set up paths'''
main_folder = r'C:\Users\Yoseop\Desktop\Personal\OD_Work\NewFeat_Ger\test_8638\lp\images_annotations\Day'
xml_orig_path = os.path.join(main_folder, "fix_needed")
xml_fix_path = os.path.join(main_folder, "Annotations")
# img_folder_path = os.path.join(main_folder[:-11], "JPEGImages")

'''create folder if it doesnt exist'''
if not os.path.exists(xml_fix_path):
    os.mkdir(xml_fix_path)
xml_names = os.listdir(xml_orig_path)
filePaths = list(range(len(xml_names)))

'''create paths to each xml file'''
index=0
for xml in xml_names:
    # if str(record)=="xml":
    #     continue
    filePaths[index] = os.path.join(xml_orig_path , xml)
    index+=1

'''parse each xml file'''



xmin=3000
xmax=0
ymin=3000
ymax=0
index=0
parser = ET.XMLParser(remove_blank_text=True)

for xml in filePaths:
    mytree = ET.parse(xml, parser)
    myroot = mytree.getroot()
    for obj in myroot.findall('object'):
        for plate in obj.findall('LicensePlate'):
            for point in plate.findall('Point'):
                # print(point.attrib)
                xmin = min(xmin, float(point.attrib['x']))
                ymin = min(ymin, float(point.attrib['y']))
                xmax = max(xmax, float(point.attrib['x'])) 
                ymax = max(ymax, float(point.attrib['y']))
            new_plate_obj = ET.Element("object")
            name = ET.SubElement(new_plate_obj, "name")
            name.text = "license_plate"
            bndbox = ET.SubElement(new_plate_obj, "bndbox")
            x_min = ET.SubElement(bndbox, "xmin")
            x_min.text = str(xmin) 
            y_min = ET.SubElement(bndbox, "ymin")
            y_min.text = str(ymin) 
            x_max = ET.SubElement(bndbox, "xmax")
            x_max.text = str(xmax) 
            y_max = ET.SubElement(bndbox, "ymax")
            y_max.text = str(ymax) 
            xmin=3000
            xmax=0
            ymin=3000
            ymax=0
            myroot.insert(1, new_plate_obj)
                    
            obj.remove(plate)
    mytree.write(os.path.join(xml_fix_path,xml_names[index]), encoding='utf-8', pretty_print=True)

    index+=1


# folder = r'C:\Users\YoseopKim\Desktop\Personal\OD_Work\License\LP_train_191011\Annotations'
# file_name = 'trig_20190326_174352_v7.01.00_r7_evk_dai_unrect_rgb_full_74474.xml'

'''test with single file first'''
# mytree = ET.parse(os.path.join(folder,file_name))
# myroot = mytree.getroot()

# xmin=3000
# xmax=0
# ymin=3000
# ymax=0
# for obj in myroot.findall('object'):
#     for plate in obj.findall('LicensePlate'):
#         for point in plate.findall('Point'):
#             print(point.attrib)
#             xmin = min(xmin, int(point.attrib['x']))
#             ymin = min(ymin, int(point.attrib['y']))
#             xmax = max(xmax, int(point.attrib['x'])) 
#             ymax = max(ymax, int(point.attrib['y']))
#         new_plate_obj = ET.Element("object")
#         name = ET.SubElement(new_plate_obj, "name")
#         name.text = "LicensePlate"
#         bndbox = ET.SubElement(new_plate_obj, "bnxbox")
#         x_min = ET.SubElement(bndbox, "xmin")
#         x_min.text = str(xmin) 
#         y_min = ET.SubElement(bndbox, "ymin")
#         y_min.text = str(ymin) 
#         x_max = ET.SubElement(bndbox, "xmax")
#         x_max.text = str(xmax) 
#         y_max = ET.SubElement(bndbox, "ymax")
#         y_max.text = str(ymax) 
#         xmin=3000
#         xmax=0
#         ymin=3000
#         ymax=0
#         myroot.insert(1, new_plate_obj)
                
#         obj.remove(plate)



# mytree.write(open(os.path.join(xml_fix_path,file_name), 'wb'))


# if not os.path.exists(img_copy_path):
#     os.mkdir(img_copy_path)
# xml_names = os.listdir(main_folder)
# filePaths = list(range(len(xml_names)))

# index=0
# for xml in xml_names:
#     # if str(record)=="xml":
#     #     continue
#     filePaths[index] = os.path.join(main_folder , xml)
#     index+=1

# # print(xml_names)
# xml_index =0

# for one_xml in filePaths:
    
#     xml = minidom.parse(one_xml)
#     itemlist = xml.getElementsByTagName('name')
#     # print(xml)
#     for s in itemlist:
#         if s.childNodes[0].data == 'roadmark__bump':
#             # print(one_xml)
#             print(s.childNodes[0].data)

#     ##finding cases of two object appearance
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



