#! python3
import os, sys
import shutil
import json
from PIL import Image

'''
convert annotations
'''
#single folder name
main_path = r'C:\Users\Yoseop\Desktop\Personal\OD_Work\CrowdHuman\CrowdHuman_val'
odgt = os.path.join(main_path, 'annotation_val.odgt') #file to convert
convert_path = os.path.join(main_path,'Annotations')
if not os.path.exists(convert_path):
    os.mkdir(convert_path)
jpeg_path = os.path.join(main_path, 'JPEGImages')
imageNames = os.listdir(jpeg_path)

#read odgt file, convert to JSON
# index=0
# data = []
# with open(odgt) as f:
#     for line in f:
#         data.append(json.loads(line))
#         index+=1

#read odgt file, convert to JSON
index=0
ignored_ped=0
mask=0
ped=0
with open(odgt) as f:
    for line in f:
        data = json.loads(line)
        name = data['ID']
        print(name)
        with open(os.path.join(convert_path,str(name)+".xml"), 'w+') as xml:
            im = Image.open(os.path.join(jpeg_path,str(name)+".jpg"))
            width, height = im.size
            xml.write("<annotation>\n\t<size>\n\t\t<width>"+str(width)+"</width>\n\t\t<height>"+str(height)+"</height>\n\t</size>\n")
            im.close()
            gtboxes = data['gtboxes']
            for single_obj in gtboxes:
                tag = str(single_obj['tag'])
                if tag == "person":
                    tag = "pedestrian"
                    if 'ignore' not in single_obj['extra'] or single_obj['extra']['ignore']!=1: #if ped is not 'ignored'
                        ped+=1
                        fxmin = str(single_obj['hbox'][0]) #full bndbox coordinates
                        fymin = str(single_obj['hbox'][1])
                        fxmax = str(int(fxmin)+single_obj['hbox'][2])
                        fymax = str(int(fymin)+single_obj['hbox'][3])
                        
                        # vxmin = str(single_obj['vbox'][0]) #visible bndbox coordinates
                        # vymin = str(single_obj['vbox'][1])
                        # vxmax = str(int(vxmin)+single_obj['vbox'][2])
                        # vymax = str(int(vymin)+single_obj['vbox'][3])

                        xml.write("\t<object>\n\t\t<name>"+tag+"</name>\n\t\t<bndbox>\n\t\t\t<xmin>"+fxmin+"</xmin>\n\t\t\t<ymin>"+fymin+"</ymin>\n\t\t\t<xmax>"+fxmax+"</xmax>\n\t\t\t<ymax>"+fymax+"</ymax>\n")
                        # xml.write("\t\t\t<vxmin>"+vxmin+"</vxmin>\n\t\t\t<vymin>"+vymin+"</vymin>\n\t\t\t<vxmax>"+vxmax+"</vxmax>\n\t\t\t<vymax>"+vymax+"</vymax>\n")
                    
                        #head bndbox cooridnates
                        # print(single_obj['head_attr'])
                        # if 'ignore' not in single_obj['head_attr'] or single_obj['head_attr']['ignore'] != 1 : #only if head is not 'ignored'
                        #     hxmin = str(single_obj['hbox'][0])
                        #     hymin = str(single_obj['hbox'][1])
                        #     hxmax = str(int(hxmin)+single_obj['hbox'][2])
                        #     hymax = str(int(hymin)+single_obj['hbox'][3])
                            # xml.write("\t\t\t<hxmin>"+hxmin+"</hxmin>\n\t\t\t<hymin>"+hymin+"</hymin>\n\t\t\t<hxmax>"+hxmax+"</hxmax>\n\t\t\t<hymax>"+hymax+"</hymax>\n")


                        xml.write('\t\t</bndbox>\n') #close coordiante info
                        # print(single_obj['extra'])
                        if tag =="pedestrian" and 'occ' in single_obj['extra'] and single_obj['extra']['occ']==1 :
                            xml.write("\t<occluded>1</occluded>\n")
                        
                        xml.write("\t</object>\n")
                    elif single_obj['extra']['ignore']==1:
                        ignored_ped+=1
                        tag = "ignored"
                        fxmin = str(single_obj['fbox'][0]) #full bndbox coordinates
                        fymin = str(single_obj['fbox'][1]) #masks's full, visible, and head coordinates are all the same
                        fxmax = str(int(fxmin)+single_obj['fbox'][2])
                        fymax = str(int(fymin)+single_obj['fbox'][3])
                        
                        xml.write("\t<object>\n\t\t<name>"+tag+"</name>\n\t\t<bndbox>\n\t\t\t<xmin>"+fxmin+"</xmin>\n\t\t\t<ymin>"+fymin+"</ymin>\n\t\t\t<xmax>"+fxmax+"</xmax>\n\t\t\t<ymax>"+fymax+"</ymax>\n")
                        xml.write('\t\t</bndbox>\n') #close coordiante info
                        xml.write("\t</object>\n")
                elif tag == "mask":
                    tag = "ignored"
                    fxmin = str(single_obj['fbox'][0]) #full bndbox coordinates
                    fymin = str(single_obj['fbox'][1]) #masks's full, visible, and head coordinates are all the same
                    fxmax = str(int(fxmin)+single_obj['fbox'][2])
                    fymax = str(int(fymin)+single_obj['fbox'][3])
                    
                    xml.write("\t<object>\n\t\t<name>"+tag+"</name>\n\t\t<bndbox>\n\t\t\t<xmin>"+fxmin+"</xmin>\n\t\t\t<ymin>"+fymin+"</ymin>\n\t\t\t<xmax>"+fxmax+"</xmax>\n\t\t\t<ymax>"+fymax+"</ymax>\n")
                    xml.write('\t\t</bndbox>\n') #close coordiante info
                    xml.write("\t</object>\n")
                    mask+=1
            xml.write("</annotation>")

        index+=1
        print(str(index)+ "\n")
print("ignored ped = " + str(ignored_ped))
print("ignore = " + str(mask))
print("ped = " + str(ped))