import cv2
import numpy as np
import glob

img_array = []
for filename in sorted(glob.glob('/media/data1/sangjun/urp22/results/leftImg8bit_rain_crop768/test_latest_iter865000/images/GOPR2157/*')) :
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('GOPR2157_24frames.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 24.0, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()