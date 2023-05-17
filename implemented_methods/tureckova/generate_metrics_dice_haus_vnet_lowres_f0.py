from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/homes/kovacs/project_data/hnc-auto-contouring/tureckova/predicted/lowres_vnet1/val_f0_cases'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'

out_abs_path_folder = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/tureckova'
out_abs_path_file = join(out_abs_path_folder,'dice_haus_vnetLowres_f0.csv')

run_for_folder(folder_pred,folder_gt,out_abs_path=out_abs_path_file)