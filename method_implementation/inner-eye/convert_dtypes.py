from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *

path_to_image_folder_src = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train_raw_data_base/images'
path_to_label_folder_src = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train_raw_data_base/labels'

path_to_image_folder_dst = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train/images'
path_to_label_folder_dst = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train/labels'

#convert images to float32
for i,fi in enumerate(listdir(path_to_image_folder_src)):
    path_to_nii_src = join(path_to_image_folder_src,fi)
    path_to_nii_dst = join(path_to_image_folder_dst,fi)
    print(f'converting image file {fi} to float32')
    convert_nii_to_float32(path_to_nii_src,path_to_nii_dst)
    

#convert labels to int8
for i,fi in enumerate(listdir(path_to_label_folder_src)):
    path_to_nii_src = join(path_to_label_folder_src,fi)
    path_to_nii_dst = join(path_to_label_folder_dst,fi)
    print(f'converting label file {fi} to int8')
    convert_nii_to_int8(path_to_nii_src,path_to_nii_dst)

