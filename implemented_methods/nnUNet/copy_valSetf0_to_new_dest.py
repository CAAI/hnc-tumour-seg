'''
Purpose:
Copy nnUnet validation fold 0 cases to a new folder
'''

from shutil import copyfile
from MEDIcaTe.file_folder_ops import *

nnUNet_all = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_trained_models/nnUNet/ensembles/Task500_HNC01/ensemble_3d_lowres__nnUNetTrainerV2__nnUNetPlansv2.1--3d_cascade_fullres__nnUNetTrainerV2CascadeFullRes__nnUNetPlansv2.1/ensembled_postprocessed'
folder_w_cases2copy = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0'
destination_folder = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_trained_models/nnUNet/ensembles/Task500_HNC01/ensemble_3d_lowres__nnUNetTrainerV2__nnUNetPlansv2.1--3d_cascade_fullres__nnUNetTrainerV2CascadeFullRes__nnUNetPlansv2.1/ensembled_postprocessed_val_cases_alone_dgk'

print('copying...')
for i,case in enumerate(listdir(folder_w_cases2copy)):
    src_file = join(nnUNet_all,case)
    dst_file = join(destination_folder,case)
    copyfile(src_file,dst_file)
print('done')