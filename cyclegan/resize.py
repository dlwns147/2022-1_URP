import os
import cv2

dir_path = "/media/data1/sangjun/raindataset/real_world"

for (root, directories, files) in os.walk(dir_path) :
    for d in directories :
        print(os.path.join(root, d))
        
    # for f in files :
    #     print(os.path.join(root, f))