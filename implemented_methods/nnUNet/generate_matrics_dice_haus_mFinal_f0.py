from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_trained_models/nnUNet/ensembles/Task500_HNC01/ensemble_3d_lowres__nnUNetTrainerV2__nnUNetPlansv2.1--3d_cascade_fullres__nnUNetTrainerV2CascadeFullRes__nnUNetPlansv2.1/ensembled_postprocessed_val_cases_alone_dgk'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'

out_abs_path_folder = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/nnUNet'
out_abs_path_file = join(out_abs_path_folder,'dice_haus_mFinal_f0.csv')

run_for_folder(folder_pred,folder_gt,out_abs_path=out_abs_path_file)