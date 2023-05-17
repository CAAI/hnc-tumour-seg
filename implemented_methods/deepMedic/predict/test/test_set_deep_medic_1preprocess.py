'''
Purpose: predict HNC02 with 196 patients using deep medic models.

The file was run from docker container:

docker run --gpus '"device=0"' --cpus 12.0 -d -it \
-v ~/../../media/bizon/data2tb/deep_medic/:/deep_medic/ \
tensorflow/tensorflow:latest-gpu bash

docker ps

docker exec -it vigorous_swirles bash

cd /deep_medic/homes/kovacs/project_scripts/hnc_segmentation/deep_medic/deepmedic
pip install .

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
    
    file_to_resample = join(path_to_test_set_all_cases, case)
    output_folder = path_to_resampled_for_deep_medic
    output_file = join(output_folder,case)
    
    if not isfile(output_file): # only process files if not created aready
        resample_nii_to_voxel_size(file_to_resample, output_folder, voxel_size, verbose = True)


def normalize_deep_medic(case):
    ct_mean_gl = -86.70951920247971
    ct_std_gl = 449.6891469125435
    pet_mean_gl = 1.454322559282762
    pet_std_gl = 1.9064418631810773
    
    file_to_normalize = join(path_to_resampled_for_deep_medic, case)
    output_folder = path_to_normalized_for_deep_medic
    output_file = join(output_folder,case)
    
    if not isfile(output_file):
        if case[-11:-7] == '0000':
            norm_0mean_1variance(file_to_normalize, output_folder, ct_mean_gl, ct_std_gl)
        elif case[-11:-7] == '0001':
            norm_0mean_1variance(file_to_normalize, output_folder, pet_mean_gl, pet_std_gl)
    # norm_0mean_1variance

'''def resample_label_data(case):
    voxel_size = (-0.9765625, 0.9765625,  2.0) # hard coded since it is based on the training data. 
    file_to_resample = ''
    output_file = ''
    if not isfile(output_file): # only process files if not created aready
        resample(file_to_resample, output_file, voxel_size, verbose = True)
'''
def generate_rois_deep_medic(case):
    cur_nifti_file = join(path_to_resampled_for_deep_medic, case)
    if case[-11:-7] == '0001': # only run for PET files
        generate_rois_dm_pt(cur_nifti_file, path_to_rois_for_deep_medic, clobber = True)

def generate_predict_config_files_deep_medic():
    pass

if __name__=='__main__':
    # path to test set.
    # 
    # alternate input paths:
    
    path_to_test_set_1_case = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_1_case_for_test_of_test'
    path_to_test_set_30_cases = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_30_cases_for_timing_test196'
    path_to_test_set_all_cases = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'

    # preprocess
    path_to_resampled_for_deep_medic = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_preprocessed/images_All_cases_for_test'
    path_to_normalized_for_deep_medic = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_preprocessed/images_All_cases_for_test_norm'
    path_to_rois_for_deep_medic = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_preprocessed/images_All_cases_for_test_rois'
    # do preprocessing here

    image_files = listdir(path_to_test_set_1_case)

    pool = Pool()
    pool.map(resample_image_data, image_files)

    image_files_resampled = listdir(path_to_resampled_for_deep_medic)
    pool.map(normalize_deep_medic, image_files_resampled)

    pool.map(generate_rois_deep_medic, image_files_resampled)

    end = time.time()
    total_time = end-start
    print(f'Processed {len(image_files)} cases.')
    print(f'Total time to preprocess = {np.round(total_time,2)} sec.')


# generate config files

# run prediction
# cd /deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/config_files/model
# deepMedicRun -model ./modelConfig_HNC_f0.cfg -test ../test/testConfig_HNC_r196_m0.cfg -load ../../output/output_HNC_f0/saved_models/trainSessionHNC0/deepMedicHNC_f0.trainSessionHNC0.final.2022-05-04.18.29.22.643919.model.ckpt -dev cuda
# deepMedicRun -model ./modelConfig_HNC_f1.cfg -test ../test/testConfig_HNC_r196_m1.cfg -load ../../output/output_HNC_f1/saved_models/trainSessionHNC1/deepMedicHNC_f1.trainSessionHNC1.final.2022-05-06.23.30.55.220415.model.ckpt -dev cuda
# deepMedicRun -model ./modelConfig_HNC_f2.cfg -test ../test/testConfig_HNC_r196_m2.cfg -load ../../output/output_HNC_f2/saved_models/trainSessionHNC2/deepMedicHNC_f2.trainSessionHNC2.final.2022-05-09.03.19.22.271867.model.ckpt -dev cuda
# deepMedicRun -model ./modelConfig_HNC_f3.cfg -test ../test/testConfig_HNC_r196_m3.cfg -load ../../output/output_HNC_f3/saved_models/trainSessionHNC3/deepMedicHNC_f3.trainSessionHNC3.final.2022-05-04.18.26.01.841199.model.ckpt -dev cuda
# deepMedicRun -model ./modelConfig_HNC_f4.cfg -test ../test/testConfig_HNC_r196_m4.cfg -load ../../output/output_HNC_f4/saved_models/trainSessionHNC4/deepMedicHNC_f4.trainSessionHNC4.final.2022-05-06.23.44.07.115762.model.ckpt -dev cuda



# output should be in patient space. Resampling: 

# get the final time
