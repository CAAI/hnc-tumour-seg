from MEDIcaTe.nii_resampling import *
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *
from MEDIcaTe.roi_generators import *
from MEDIcaTe.visualize_labels_ct_pet import *
from MEDIcaTe.normalize import *
from random import sample
import numpy as np
import pathlib

path_to_data_src = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifti_as_deepmedic/train'
path_to_data_dst = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifti_as_deepmedic/train_r'

for fo in listdir(path_to_data_src):
    cur_src_path = join(path_to_data_src,fo)
    cur_dst_path = join(path_to_data_dst,fo)
    if not isdir(cur_dst_path):
        os.mkdir(cur_dst_path)
    for fi in listdir(cur_src_path):
        cur_src_file_path = join(cur_src_path,fi)
        cur_dst_file_path = join(cur_dst_path,fi)
        if not isfile(cur_dst_file_path):
            if (fi[-11:-7] == '0000') or (fi[-11:-7] == '0001'):
                convert_nii_to_float32(cur_src_file_path,cur_dst_file_path)
                print(f'Converted {fi} to float32')
            else: 
                convert_nii_to_int16(cur_src_file_path,cur_dst_file_path)
                print(f'Converted {fi} to int16')