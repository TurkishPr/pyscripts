### execute "python" in python folder of svcaffe
#################################################

import caffe
import numpy as np
import os, sys
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import struct


def visualize_weights(net, layer_name, padding=4, filename=''):
    # The parameters are a list of [weights, bisases]
    data = np.copy(net.params[layer_name][0].data)
    # N is the totla number of convoltions
    N = data.shape[0] * data.shape[1]
    #print("N : " + str(N))
    # Ensure that the resulting image is square
    filters_per_row = int(np.ceil(np.sqrt(N)))
    #print("filters per row : " + str(filters_per_row))
    # Assume the filters are square
    filter_size = data.shape[2]
    #print("filter_size : " + str(filter_size))
    # Size of the result image including padding
    result_size = filters_per_row*(filter_size + padding) - padding
    #print("result_size : " + str(result_size))
    # Initialize result image to all zeros
    result = np.zeros((result_size, result_size))

    # Tile the filters into the reuslt image
    filter_x = 0
    filter_y = 0
    #print(data.shape[0])
    #print(data.shape[1])
    for n in range(data.shape[0]):
        for c in range(data.shape[1]):
            if filter_x == filters_per_row:
                filter_y += 1
                filter_x = 0
            for i in range(filter_size):
                for j in range(filter_size):
                    result[filter_y*(filter_size + padding) + i, filter_x*(filter_size + padding) + j] = data[n, c, i, j]
            filter_x += 1
    # Normalize image to 0~1
    min = result.min()
    max = result.max()
    result = (result - min) / (max - min)

    # Plot figure
    plt.figure(figsize=(10,10))
    plt.axis('off')
    plt.imshow(result, cmap='gray', interpolation='nearest')


    # save plot if filename is given
    if filename != '':
        plt.savefig(filename, bbox_inches = 'tight', pad_inches = 0)

    plt.show()



caffe.set_device(0)
caffe.set_mode_gpu()

net = caffe.Net('train_val.prototxt','M523_RE_iter_1500000.caffemodel', caffe.TEST)
#net2 = caffe.Net('transformed.prototxt','original.caffemodel', caffe.TEST)
visualize_weights(net, 'conv1_1', 4, 'conv1.jpg')
visualize_weights(net, 'conv2_1', 4, 'conv2.jpg')
visualize_weights(net, 'conv3_1', 4, 'conv3.jpg')
visualize_weights(net, 'conv4_1', 4, 'conv4.jpg')
visualize_weights(net, 'conv5_1', 4, 'conv5.jpg')

# for transforming
# weight: net6.params[LAYER NAME HERE][0].data[...] = transformed(net.params[LAYER NAME HERE][0].data.copy())
# bias = net2.params[LAYER NAME HERE[1].data[...] = transform9net.params[LAYER NAME HERE][1].data.copy())
#....

#net2.save('transformed.caffemodel') #save new caffemodel
