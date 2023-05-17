from MEDIcaTe.calculate_dice_haus import run_for_folder

folder_pred = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m0/predictions_nnunet_id_patient_space'
folder_gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
out_abs_path = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/deepMedic/predict/val/dice_haus_m0_f0.csv'

run_for_folder(folder_pred,folder_gt,out_abs_path=out_abs_path)