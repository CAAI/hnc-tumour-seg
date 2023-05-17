'''
Purpose:
Preprocess test data set for Swin-Unetr method from scratch.

Data is prepared according to https://github.com/microsoft/InnerEye-DeepLearning/blob/main/docs/creating_dataset.md.
'''

# import module for timing and start timing
import time 
start = time.time()

#load packages
from MEDIcaTe.nii_resampling import *
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *
from MEDIcaTe.roi_generators import *
from MEDIcaTe.visualize_labels_ct_pet import *
from MEDIcaTe.normalize import *
from multiprocessing import Pool


def resample_image_data(case):
    voxel_size = (-0.9765625, 0.9765625,  2.0) # hard coded since it is based on the training data. 
    
    file_to_resample = join(path_to_test_set_all_cases_images, case)
    output_folder = path_to_resampled_for_swinUnetr
    output_file = join(output_folder,case)
    
    if not isfile(output_file): # only process files if not created aready
        resample_nii_to_voxel_size(file_to_resample, voxel_size, output_folder, verbose = True)

def resample_label_data(case):
    voxel_size = (-0.9765625, 0.9765625,  2.0) # hard coded since it is based on the training data. 
    
    file_to_resample = join(path_to_test_set_all_cases_labels, case)
    output_folder = path_to_resampled_for_swinUnetr_labels
    output_file = join(output_folder,case)
    
    if not isfile(output_file): # only process files if not created aready
        resample_nii_to_voxel_size(file_to_resample, voxel_size, output_folder, order=0, verbose = True)


def normalize_swinUnetr(case):
    ct_mean_gl = -86.70951920247971 # hard coded since it is based on the training data. 
    ct_std_gl = 449.6891469125435   # hard coded since it is based on the training data. 
    pet_mean_gl = 1.454322559282762 # hard coded since it is based on the training data. 
    pet_std_gl = 1.9064418631810773 # hard coded since it is based on the training data. 
    
    file_to_normalize = join(path_to_resampled_for_swinUnetr, case)
    output_folder = path_to_normalized_for_swinUnetr
    output_file = join(output_folder,case)
    
    if not isfile(output_file):
        if case[-11:-7] == '0000':
            norm_0mean_1variance(file_to_normalize, output_folder, ct_mean_gl, ct_std_gl)
        elif case[-11:-7] == '0001':
            norm_0mean_1variance(file_to_normalize, output_folder, pet_mean_gl, pet_std_gl)


def convert_data_types(case):
    input_file = join(path_to_normalized_for_swinUnetr,case)
    output_file = join(path_to_convert_data_types_for_swinUnetr,case)
    if not isfile(output_file):
        convert_nii_to_float32(input_file,output_file)

def convert_data_types_label(case):
    input_file = join(path_to_resampled_for_swinUnetr_labels,case)
    output_file = join(path_to_convert_data_types_for_swinUnetr_labels,case)
    if not isfile(output_file):
        convert_nii_to_int8(input_file,output_file)

def convert_4d_dat_to_channel_first(case):
    ct_abs_path = join(path_to_convert_data_types_for_swinUnetr,f'{case}_0000.nii.gz')
    pet_abs_path = join(path_to_convert_data_types_for_swinUnetr,f'{case}_0001.nii.gz')
    pet_ct_dst_path = join(path_to_4d_channel_first_swinUnetr,f'{case}.nii.gz')
    if not isfile(pet_ct_dst_path):
        convert_pet_ct_to_4d_nifti_channel_first(ct_abs_path, pet_abs_path, pet_ct_dst_path)
    label_abs_path = join(path_to_convert_data_types_for_swinUnetr_labels,f'{case}.nii.gz')
    label_ch_first_dest_abs_path = join(path_to_4d_channel_first_swinUnetr_labels,f'{case}.nii.gz')
    if not isfile(label_ch_first_dest_abs_path):
        convert_label_to_channel_first(label_abs_path, label_ch_first_dest_abs_path)



if __name__=='__main__':
    # path to test set.
    # alternate input paths:
    path_to_test_set_1_case = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_1_case_for_test_of_test'
    path_to_test_set_30_cases = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_30_cases_for_timing_test196'
    path_to_test_set_all_cases_images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
    path_to_test_set_all_cases_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels'


    # preprocess
    path_to_resampled_for_swinUnetr = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/imagesTs/resampled'
    path_to_resampled_for_swinUnetr_labels = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/labelsTs/resampled'

    path_to_normalized_for_swinUnetr = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/imagesTs/normalized'
    
    path_to_convert_data_types_for_swinUnetr = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/imagesTs/converted_data_types'
    path_to_4d_channel_first_swinUnetr = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/imagesTs/data_as_4d_channel_first'

    path_to_convert_data_types_for_swinUnetr_labels = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/labelsTs/converted_data_types'
    path_to_4d_channel_first_swinUnetr_labels = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/labelsTs/data_as_4d_channel_first'
    # do preprocessing here
    
    image_files = listdir(path_to_test_set_all_cases_images) # adding path_to_test_set_1_case | path_to_test_set_30_cases | path_to_test_set_all_cases_images. First two are for testing purposes.
    #resample_image_data(image_files[0])
    pool = Pool()
    pool.map(resample_image_data, image_files)

    image_files_resampled = listdir(path_to_resampled_for_swinUnetr)
    pool.map(normalize_swinUnetr, image_files_resampled)

    image_files_normalized = listdir(path_to_normalized_for_swinUnetr)
    pool.map(convert_data_types, image_files_normalized)

    all_cases = [element[0:9] for element in image_files]
    all_cases = list(dict.fromkeys(all_cases))
    pool.map(convert_4d_dat_to_channel_first, all_cases)

    label_files = listdir(path_to_test_set_all_cases_labels)
    pool.map(resample_label_data,label_files)

    label_files_resampled = listdir(path_to_resampled_for_swinUnetr_labels)
    pool.map(convert_data_types_label,label_files_resampled)

    end = time.time()
    total_time = end-start
    print(f'Processed {len(all_cases)} case(s).')
    print(f'Total time to preprocess = {np.round(total_time,2)} sec.')