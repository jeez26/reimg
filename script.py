import cv2
import numpy as np
import math
import sys, time
import base64
import os

def nn_interpolate(file_name, scale_factor):
    image = cv2.imread('upload/'+file_name)

    (rows, cols, channels) = image.shape
    scaled_height = rows * scale_factor
    scaled_weight = cols * scale_factor

    row_scale_factor = rows / scaled_height
    col_scale_factor = cols / scaled_weight

    row_position = np.floor(np.arange(scaled_height) * row_scale_factor).astype(int)
    column_position = np.floor(np.arange(scaled_weight) * col_scale_factor).astype(int)

    scaled_image = np.zeros((scaled_height, scaled_weight, 3), np.uint8)

    for i in range(scaled_height):
        for j in range(scaled_weight):
            scaled_image[i, j] = image[row_position[i], column_position[j]]
            
    new_file_name = 'upload/'+file_name.split('.')[0]+'_new.'+file_name.split('.')[1]
    cv2.imwrite(new_file_name, scaled_image)
    with open(new_file_name, "rb") as f:
        im_b64 = base64.b64encode(f.read()).decode("utf-8")
    os.remove(new_file_name)
    return im_b64


def u(s,a):
    if (abs(s) >=0) & (abs(s) <=1):
        return (a+2)*(abs(s)**3)-(a+3)*(abs(s)**2)+1
    elif (abs(s) > 1) & (abs(s) <= 2):
        return a*(abs(s)**3)-(5*a)*(abs(s)**2)+(8*a)*abs(s)-4*a
    return 0



def padding(image,H,W,C):
    zimage = np.zeros((H+4,W+4,C))
    zimage[2:H+2,2:W+2,:C] = image
    #Pad the first/last two col and row
    zimage[2:H+2,0:2,:C]=image[:,0:1,:C]
    zimage[H+2:H+4,2:W+2,:]=image[H-1:H,:,:]
    zimage[2:H+2,W+2:W+4,:]=image[:,W-1:W,:]
    zimage[0:2,2:W+2,:C]=image[0:1,:,:C]
    #Pad the missing eight points
    zimage[0:2,0:2,:C]=image[0,0,:C]
    zimage[H+2:H+4,0:2,:C]=image[H-1,0,:C]
    zimage[H+2:H+4,W+2:W+4,:C]=image[H-1,W-1,:C]
    zimage[0:2,W+2:W+4,:C]=image[0,W-1,:C]
    return zimage


def bicubic(file_name, scale_factor, a=-1/2):
    image = cv2.imread('upload/'+file_name)
    #Get image size
    H,W,C = image.shape

    image = padding(image,H,W,C)
    #Create new image
    dH = math.floor(H*scale_factor)
    dW = math.floor(W*scale_factor)
    scaled_image = np.zeros((dH, dW, 3))

    h = 1/scale_factor

    for c in range(C):
        for j in range(dH):
            for i in range(dW):
                x, y = i * h + 2 , j * h + 2

                x1 = 1 + x - math.floor(x)
                x2 = x - math.floor(x)
                x3 = math.floor(x) + 1 - x
                x4 = math.floor(x) + 2 - x

                y1 = 1 + y - math.floor(y)
                y2 = y - math.floor(y)
                y3 = math.floor(y) + 1 - y
                y4 = math.floor(y) + 2 - y

                mat_l = np.matrix([[u(x1,a),u(x2,a),u(x3,a),u(x4,a)]])
                mat_m = np.matrix([[image[int(y-y1),int(x-x1),c],image[int(y-y2),int(x-x1),c],image[int(y+y3),int(x-x1),c],image[int(y+y4),int(x-x1),c]],
                                   [image[int(y-y1),int(x-x2),c],image[int(y-y2),int(x-x2),c],image[int(y+y3),int(x-x2),c],image[int(y+y4),int(x-x2),c]],
                                   [image[int(y-y1),int(x+x3),c],image[int(y-y2),int(x+x3),c],image[int(y+y3),int(x+x3),c],image[int(y+y4),int(x+x3),c]],
                                   [image[int(y-y1),int(x+x4),c],image[int(y-y2),int(x+x4),c],image[int(y+y3),int(x+x4),c],image[int(y+y4),int(x+x4),c]]])
                mat_r = np.matrix([[u(y1,a)],[u(y2,a)],[u(y3,a)],[u(y4,a)]])
                scaled_image[j, i, c] = np.dot(np.dot(mat_l, mat_m),mat_r)

    new_file_name = 'upload/'+file_name.split('.')[0]+'_new.'+file_name.split('.')[1]
    cv2.imwrite(new_file_name, scaled_image)
    with open(new_file_name, "rb") as f:
        im_b64 = base64.b64encode(f.read()).decode("utf-8")
    os.remove(new_file_name)
    return im_b64




def bilinear(file_name, scale_factor):
    image = cv2.imread('upload/'+file_name)
    (h, w, channels) = image.shape
    h2 = h  * scale_factor
    w2 = w  * scale_factor
    scaled_image = np.zeros((h2, w2, 3), np.uint8)
    x_ratio = float((w - 1)) / w2;
    y_ratio = float((h - 1)) / h2;
    for i in range(1, h2 - 1): 
        for j in range(1 ,w2 - 1):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            x_diff = (x_ratio * j) - x
            y_diff = (y_ratio * i) - y
            a = image[x, y] & 0xFF
            b = image[x + 1, y] & 0xFF
            c = image[x, y + 1] & 0xFF
            d = image[x + 1, y + 1] & 0xFF
            blue = a[0] * (1 - x_diff) * (1 - y_diff) + b[0] * (x_diff) * (1-y_diff) + c[0] * y_diff * (1 - x_diff)   + d[0] * (x_diff * y_diff)
            green = a[1] * (1 - x_diff) * (1 - y_diff) + b[1] * (x_diff) * (1-y_diff) + c[1] * y_diff * (1 - x_diff)   + d[1] * (x_diff * y_diff)
            red = a[2] * (1 - x_diff) * (1 - y_diff) + b[2] * (x_diff) * (1-y_diff) + c[2] * y_diff * (1 - x_diff)   + d[2] * (x_diff * y_diff)
            scaled_image[j, i] = (blue, green, red)

    new_file_name = 'upload/'+file_name.split('.')[0]+'_new.'+file_name.split('.')[1]
    cv2.imwrite(new_file_name, scaled_image)
    with open(new_file_name, "rb") as f:
        im_b64 = base64.b64encode(f.read()).decode("utf-8")
    os.remove(new_file_name)
    return im_b64
