import os
import sys
import shutil


# SRC_PATH = '/media/data1/sangjun/VFP290K'
# TARGET_PATH = '/media/data1/sangjun/urp22/results/leftImg8bit_rain_crop768/test_latest_iter795000/images'

SRC1_PATH = '/media/data1/sangjun/VFP290K'
# SRC2_PATH = '/media/data1/sangjun/urp22/results/leftImg8bit_rain_crop768/test_latest_iter795000/images'
TARGET_PATH = '/media/data1/sangjun/urp22/mixed_dataset'
# FOLDER_LIST = ["GOPR0809", "GOPR0812", "GOPR0813", "GOPR0815", "GOPR0816", "GOPR0827", "GOPR0829", "GOPR0832", "GOPR0865", "GOPR0866", "GOPR0951", "GOPR0952", "GOPR1726", "GOPR1732", "GOPR1733", "GOPR1738", "GOPR1739", "GOPR1743", "GOPR1746", "GOPR1750", "GOPR1752", "GOPR1781", "GOPR1787", "GOPR1790", "GOPR1793", "GOPR1797", 
# "GOPR1800", "GOPR1801", "GOPR1802", "GOPR1805", "GOPR1810", "GOPR1813", "GOPR1855", "GOPR1859", "GOPR1865"]  # train images (relative to 'path') 128 images
FOLDER_LIST = ["GOPR0805", "GOPR0825", "GOPR0860", "GOPR0864", "GOPR1715", "GOPR1742", "GOPR1857", "GOPR2201", "GOPR2668", "GOPR2692", "GOPR2700", "GOPR2749"]

# PATHS = [os.path.join(PATH, folder) for folder in FOLDER_LIST]

# for folder in FOLDER_LIST[0::2] :
#     src_folder = os.path.join(SRC1_PATH, folder, 'images')
#     tar_folder = os.path.join(TARGET_PATH, folder)
#     # os.makedirs(tar_folder, exist_ok = True)
#     shutil.copytree(src_folder, tar_folder)
#     # os.makedirs()
#     # print(path)
#     print(src_folder)
#     print(tar_folder)
    
    
# for folder in FOLDER_LIST[1::2] :
#     src_folder = os.path.join(SRC2_PATH, folder)
#     tar_folder = os.path.join(TARGET_PATH, folder)
#     shutil.copytree(src_folder, tar_folder)
#     print(src_folder)
#     print(tar_folder)

for folder in FOLDER_LIST :
    src_folder = os.path.join(SRC1_PATH, folder, 'images')
    tar_folder = os.path.join(TARGET_PATH, folder)
    shutil.copytree(src_folder, tar_folder)
    print(src_folder)
    print(tar_folder)
