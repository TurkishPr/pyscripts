#! python3
import os, sys
import shutil

'''
copy stuff
'''
main_path = "C:/Users/YoseopKim/Desktop/Personal/Anyverse/Anyverse_test"

names = os.listdir(main_path)
# print(names)
# print(len(names))
file_cnt = len(names)
# for i in range(1,61):
#     if i<10:
#         img_folder_path = "X:/GOD/PrivateSet/anyverse/Anyverse_result/batch-0" + str(i)
#         depth_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-0" + str(i) +"/hero_camera/depth-images"
#         instance_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-0" + str(i) +"/hero_camera/instance-images"
#         label_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-0" + str(i) +"/hero_camera/label-images"

#     else:
#         img_folder_path = "X:/GOD/PrivateSet/anyverse/Anyverse_result/batch-" + str(i)
#         depth_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-" + str(i) +"/hero_camera/depth-images"
#         instance_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-" + str(i) +"/hero_camera/instance-images"
#         label_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-" + str(i) +"/hero_camera/label-images"

for name in names:
    # print(name)
    # print(os.path.join(main_path,name))
    batch_path = os.path.join(main_path,name)
    img_folder_path = os.path.join(batch_path, 'hero_camera/color-images')
    depth_folder_path = os.path.join(batch_path, 'hero_camera/depth-images')
    instance_folder_path = os.path.join(batch_path, 'hero_camera/instance-images')    
    label_folder_path = os.path.join(batch_path, 'hero_camera/label-images')
    annotations_folder_path = os.path.join(batch_path, 'hero_camera/annotations')

    # print(os.listdir(annotations_folder_path))

    images = os.listdir(img_folder_path)
    depths = os.listdir(depth_folder_path)
    instances = os.listdir(instance_folder_path)
    labels = os.listdir(label_folder_path)
    annotations = os.listdir(annotations_folder_path)

    imageNames = list(images)
    depthNames = list (depths)
    instanceNames = list(instances)
    labelNames = list(labels)
    annotationNames = list(annotations)
    print("*****"+name+"*****")
    print("images      " + str(len(images)))
    print("annotations " + str(len(annotations)))
    print("depths      " + str(len(depths)))
    print("instance    " + str(len(instances)))
    print("labels      " + str(len(labels)))
    index=0
    for image in images:
        images[index] = img_folder_path + '/' + image
        # print(images[index])
        index+=1
    
    index=0
    for label in labels:
        labels[index] = label_folder_path + '/' + label
        # print(labels[index])
        index+=1

    index=0
    for depth in depths:
        depths[index] = depth_folder_path + '/' + depth
        # print(depths[index])
        index+=1

    index=0
    for instance in instances:
        instances[index] = instance_folder_path + '/' + instance
        # print(instances[index])
        index+=1

    index=0
    for annotation in annotations:
        annotations[index] = annotations_folder_path + '/' + annotation
        # print(annotations[index])
        index+=1

    copy_path = os.path.join(main_path, "UDB")
    img_copy_path = os.path.join(copy_path, "JPEGImages")
    depth_copy_path =os.path.join(copy_path, "depth-images")
    instance_copy_path = os.path.join(copy_path, "instance-images")
    label_copy_path = os.path.join(copy_path, "label-images")
    annotation_copy_path = os.path.join(copy_path, "Annotations_to_convert")
    # print(img_copy_path)
    if not os.path.exists(copy_path):
        os.mkdir(copy_path)
    if not os.path.exists(img_copy_path):
        os.mkdir(img_copy_path)
    if not os.path.exists(depth_copy_path):
        os.mkdir(depth_copy_path)
    if not os.path.exists(instance_copy_path):
        os.mkdir(instance_copy_path)
    if not os.path.exists(label_copy_path):
        os.mkdir(label_copy_path)
    if not os.path.exists(annotation_copy_path):
        os.mkdir(annotation_copy_path)

    image_idx = 0
    for image in images:
        fileName ="anyverse_" + name+"_"+imageNames[image_idx]
        image_idx+=1
        # print(fileName)
        try:
            shutil.copy(image, img_copy_path+"/"+fileName)
        except IOError:
            continue
    
    idx = 0
    for depth in depths:

        fileName ="anyverse_" +  name+"_"+depthNames[idx]
        idx+=1
        # print(fileName)
        try:
            shutil.copy(depth, depth_copy_path+"/"+fileName)
        except IOError:
            continue

    idx = 0
    for instance in instances:

        fileName = "anyverse_" + name+"_"+instanceNames[idx]
        idx+=1
        # print(fileName)
        try:
            shutil.copy(instance, instance_copy_path+"/"+fileName)
        except IOError:
            continue

    idx = 0
    for label in labels:

        fileName = "anyverse_" + name+"_"+labelNames[idx]
        idx+=1
        # print(fileName)
        try:
            shutil.copy(label, label_copy_path+"/"+fileName)
        except IOError:
            continue


    idx = 0
    for annotation in annotations:

        fileName = "anyverse_" + name+"_"+annotationNames[idx]
        idx+=1
        # print(fileName)
        try:
            shutil.copy(annotation, annotation_copy_path+"/"+fileName)
        except IOError:
            continue


    
#     '''
#     copy annotations
#     '''
#     if i<10:
#         anno_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-0" + str(i) +"/hero_camera/annotations"
#     else:
#         anno_folder_path = "X:/GOD/PrivateSet/anyverse/anyverse-city-random-scenes/anyverse-city-random-scenes/batch-" + str(i) +"/hero_camera/annotations"
#     # print(folder_path)
#     annotations = []
#     annotations = os.listdir(anno_folder_path)
#     # annotationsNames = list(annotations)
#     # imageNames = os.listdir(img_folder_path)
#     # print(imageNames)
#     index2=0
#     for anno in annotations:
#         annotations[index2] = anno_folder_path + '/' + anno
#         # print(annotations[index2])
#         index2+=1

#     anno_copy_path = "C:/Users/YoseopKim/Desktop/Personal/Anyverse/annotations_to_convert"
#     if not os.path.exists(anno_copy_path):
#         os.mkdir(anno_copy_path)
    
#     anno_idx = 0
#     for anno in annotations:
#         if i<10:
#             fileName = "anyverse_batch-0"+str(i)+"_"+imageNames[anno_idx][:-4]+".json"
#         else:
#             fileName = "anyverse_batch-"+str(i)+"_"+imageNames[anno_idx][:-4]+".json"
#         anno_idx+=1
#         # print(fileName)
#         # print (anno)
#         # print (anno_copy_path+"/"+fileName)
#         try:
#             shutil.copy(anno, anno_copy_path+"/"+fileName)
#         except IOError:
#             continue
