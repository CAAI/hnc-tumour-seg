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
from random import sample
import numpy as np

# path to test set.
# 
# alternate input paths:
#
# path_to_test_set_30_cases = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_30_cases_for_timing_test196'
# path_to_test_set_all_cases = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
#
path_to_test_set_1_case = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_1_case_for_test_of_test'

# preprocess
path_to_preprocessed_for_deep_medic = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifti_as_deepmedic/test_normalized/t_r196'
# do preprocessing here

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
end = time.time()
total_time = end-start
print("\n"+ str(total_time))