#! python3
import os, sys
import shutil
import json

'''
convert annotations
'''

for i in range(0,1): # #number of folders containing data to convert. could be one or multiple
    #single folder name
    main_path = 'C:\Users\YoseopKim\Desktop\Personal\Anyverse\Anyverse_test\UDB'
    folder_path = os.path.join(main_path, 'Annotations_to_convert')
    convert_path = os.path.join(main_path,'Annotations')
    if not os.path.exists(convert_path):
        os.mkdir(convert_path)

    imageNames = os.listdir(os.path.join(main_path, 'JPEGImages'))
    #list of all the files in single folder
    records = []
    filePaths =[]
    records = os.listdir(folder_path)
    fileNames = os.listdir(folder_path)
    filePaths = range(len(records))
    # records = filePaths

    #recreate list of files with proper pathing
    index=0
    for record in records:
        # if str(record)=="xml":
        #     continue
        filePaths[index] = os.path.join(folder_path , record)
        index+=1    
        # print(len(record[:-5]))
    # print(filePaths)
    #parse JSON annotaion data
    #convert to UDB XML format
    index=0
    for single_file in filePaths:

        if len(str(single_file))<5:
            continue
        # else:
        #     print "     ************   "+ single_file + "     ************   \n"



        new_path = convert_path+"/"+imageNames[index][:-4]+".xml"

        print(new_path)
        index+=1

        with open(new_path, 'a+') as f1:
            with open(single_file, 'r') as f2:
                #read JSON file
                json_str = json.load(f2)
                #camera width and height
                width = str(json_str['camera']['resolution'][0])
                height = str(json_str['camera']['resolution'][1])
                f1.write("<annotation>\n\t<size>\n\t\t<width>"+width+"</width>\n\t\t<height>"+height+"</height>\n\t</size>\n")


                single_file_all_objects = json_str['objects']

                for single_obj in single_file_all_objects:
                    name = str(single_obj['label']).lower()
                    # if name == "car" or name == "van":
                    #     name = "sedan"
                    if name == "motorcycle": 
                        name = "bike"
                    # elif name == "bycicle":
                    #     name = "bicycle"
                    elif name == "cyclist":
                        name = "rider_bicycle"
                    elif name == "biker":
                        name = "rider_bike"                   
                    # elif  or name == "rider":
                    #     name = "rider"


                    # print(name+"'s ")
                    coord = single_obj['2d-bounding-rectangle']
                    xmin = str(coord[0])
                    ymin = str(coord[1])
                    xmax = str(coord[0]+coord[2])
                    ymax = str(coord[1]+coord[3])
                    # print(str(single_obj['label']).lower()+ " " +str(coord))
                    # print(str(xmin))

                    f1.write("\t<object>\n\t\t<name>"+name+"</name>\n\t\t<bndbox>\n\t\t\t<xmin>"+xmin+"</xmin>\n\t\t\t<ymin>"+ymin+"</ymin>\n\t\t\t<xmax>"+xmax+"</xmax>\n\t\t\t<ymax>"+ymax+"</ymax>\n\t\t</bndbox>\n")

                    # if name == "pedestrian":
                    #     f1.write("\t<sit_stand>0</sit_stand>\n")
                    # if name =="sedan":
                        # print(str(single_obj['occluded']))
                    if str(single_obj['occluded']) == "False":
                        f1.write("\t<occluded>0</occluded>\n")
                    else:
                        f1.write("\t<occluded>1</occluded>\n")
    
                    f1.write("\t</object>\n")
                
                f1.write("</annotation>")

