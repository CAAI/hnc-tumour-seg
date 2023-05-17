'''
Purpose: Generate config files necessary to run deep medic. 
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *


def generate_config_files_for_test(destination_path):
    files_ct = []
    files_pt = []
    files_roi = []
    files_out = []

    absolute_subtring = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/'
    relative_substring = '../../'

    cases = listdir(dm_test_dat_path)
    
    for case in cases:
        if case[10:] == '0000.nii.gz':
            fname_ct = join(dm_test_dat_path,f'{case[0:9]}_0000.nii.gz')
            fname_pet= join(dm_test_dat_path,f'{case[0:9]}_0001.nii.gz')
            fname_roi= join(dm_test_roi_path,f'{case[0:9]}_0001_roi.nii.gz')
            #ct
            if isfile(fname_ct):
                files_ct.append(fname_ct.replace(absolute_subtring,relative_substring))
            else: 
                print('ERROR: CT file did not exist')
            #pet
            if isfile(fname_pet):
                files_pt.append(fname_pet.replace(absolute_subtring,relative_substring))
            else: 
                print('ERROR: PET file did not exist')
            #roi
            if isfile(fname_roi):
                files_roi.append(fname_roi.replace(absolute_subtring,relative_substring))
            else: 
                print('ERROR: ROI file did not exist')
            files_out.append(f'{case[0:9]}.nii.gz')
        
    files_ct.sort()
    files_pt.sort()
    files_roi.sort()
    files_out.sort()
    all_im_roi_labs = [files_ct, files_pt, files_roi, files_out]
    out_files = ['ct', 'pet', 'roi', 'names_of_predictions']
        
        
    for i, modality in enumerate(out_files):
        outF = open(join(destination_path,f'test_data_t196_{modality}.cfg'), 'w')
        for line in all_im_roi_labs[i]:
        # write line to output file
            outF.write(line)
            outF.write("\n")
        outF.close()

def generate_test_config_file():
    pass

def generate_run_file():
    pass

if __name__=='__main__':

    # Path to the test data images in preprocessed form:
    dm_test_dat_path = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_preprocessed/images_All_cases_for_test_norm'

    # Path to the test dasta rois ceated during preprocessing:
    dm_test_roi_path = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_preprocessed/images_All_cases_for_test_rois'

    # Path to the config files: 
    config_path_test = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/config_files/test'

    generate_config_files_for_test(destination_path = config_path_test)

    end = time.time()
    total_time = end-start
    print(f'Processed {len(listdir(dm_test_roi_path))} cases.')
    print(f'Total time to preprocess = {np.round(total_time,2)} sec.')