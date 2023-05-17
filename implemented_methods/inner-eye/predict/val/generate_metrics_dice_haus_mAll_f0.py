from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/output/majority_voted_patient_space'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
out_folder_abs_path = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/inner-eye/predict/'

out_file_abs_path = join(out_folder_abs_path,'dice_haus_mAll_f0.csv')

run_for_folder(folder_pred,folder_gt,out_abs_path=out_file_abs_path)