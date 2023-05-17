from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_patient_space_body_masked'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
out_abs_path = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/swin-unetr/predict/dice_haus_mAll_f0.csv'

run_for_folder(folder_pred,folder_gt,out_abs_path=out_abs_path)