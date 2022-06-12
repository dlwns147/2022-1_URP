import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from PIL import Image
import torch
# import IS
import pathlib
from IPython import embed
import torchvision.transforms as TF

from pytorch_gan_metrics import (get_inception_score,
                                 get_fid,
                                 get_inception_score_and_fid)
from pytorch_gan_metrics import ImageDataset
from torch.utils.data import DataLoader
IS_dict_fake = {}
IS_dict_real = {}

path = "/media/data1/sangjun/urp22/results/leftImg8bit_rain_crop768/test_latest_iter795000/images"
path2 = "/media/data1/sangjun/VFP290K"
train = ["GOPR0809", "GOPR0812", "GOPR0813", "GOPR0815", "GOPR0816", "GOPR0827", "GOPR0829", "GOPR0832", "GOPR0865", "GOPR0866", "GOPR0951", "GOPR0952", "GOPR1726", "GOPR1732", "GOPR1733", "GOPR1738", "GOPR1739", "GOPR1743", "GOPR1746", "GOPR1750", "GOPR1752", "GOPR1781", "GOPR1787", "GOPR1790", "GOPR1793", "GOPR1797", 
"GOPR1800", "GOPR1801", "GOPR1802", "GOPR1805", "GOPR1810", "GOPR1813", "GOPR1855", "GOPR1859", "GOPR1865"]
paths = [os.path.join(path, t) for t in train]
path2s = [os.path.join(path2, t) for t in train]
# folders = sorted(os.listdir(path))
folders = sorted(paths)
path2s = sorted(path2s)
print(folders)
# print(folders)
# print(len(folders))
for folder in folders:
    
    # temp_path = os.path.join(path, folder)
#     # temp_path = os.path.join(temp_path, "images")
#     temp_path2 = os.path.join(path2, folder)
#     temp_path2 = os.path.join(temp_path2, "images")
    dataset = ImageDataset(paths, exts=['png', 'jpg'])
#     loader = DataLoader(dataset, batch_size=50, num_workers=4)
#     dataset2 = ImageDataset(temp_path2, exts=['png', 'jpg'])
#     loader2 = DataLoader(dataset2, batch_size=50, num_workers=4)
    
#     IS_fake, IS_std_fake = get_inception_score(loader)
#     IS_real, IS_std_real = get_inception_score(loader2)
    
#     IS_dict_fake[temp_path]=[IS_fake, IS_std_fake]
#     IS_dict_real[temp_path2]=[IS_real, IS_std_real]
#     print(f"FAKE: {temp_path} -> {IS_fake}")
#     print(f"REAL: {temp_path2} -> {IS_real}")
#     print("===================================")
