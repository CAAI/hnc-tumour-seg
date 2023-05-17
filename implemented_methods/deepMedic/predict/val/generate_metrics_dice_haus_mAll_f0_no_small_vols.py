from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0_no_small_vols'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
out_abs_path = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/deepMedic/predict/val/dice_haus_mAll_f0_no_small_vols.csv'

run_for_folder(folder_pred,folder_gt,out_abs_path=out_abs_path)

