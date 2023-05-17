'''
Purpose: Get metrics for all 5 methods on validation set of fold 0.
Mainly to test if the pipeline is OK before proceeding to the test set.

TODO: Have not yet done this for innereye, nnUNEt and tureckova. Make sure to include thoses.
'''

import pandas as pd

result_file_deep_medic = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/deepMedic/predict/val/dice_haus_mAll_f0_no_small_vols.csv'
result_file_inner_eye = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/inner-eye/predict/dice_haus_mAll_f0.csv'
result_file_nn_unet = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/nnUNet/dice_haus_mFinal_f0.csv'
result_file_swin_unetr = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/swin-unetr/predict/dice_haus_mAll_f0_no_small_vols.csv'
result_file_tureckova = '/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/tureckova/dice_haus_vnetLowres_f0.csv'

r_deep_medic = pd.read_csv(result_file_deep_medic, index_col=0)
r_inner_eye = pd.read_csv(result_file_inner_eye, index_col=0)
r_nn_unet = pd.read_csv(result_file_nn_unet, index_col=0)
r_swin_unetr = pd.read_csv(result_file_swin_unetr, index_col=0)
r_tureckova = pd.read_csv(result_file_tureckova, index_col=0)

r_deep_medic['method'] = 'deep_medic'
r_inner_eye['method'] = 'inner_eye'
r_nn_unet['method'] = 'nn_unet'
r_swin_unetr['method'] = 'swin_unetr'
r_tureckova['method'] = 'tureckova'

r = pd.concat([r_deep_medic,r_inner_eye,r_nn_unet,r_swin_unetr,r_tureckova])
r_dice = r.drop(columns=['Hausdorff distance'])
r_dice['metric'] = 'dice'
r_dice = r_dice.rename(columns={'Dice Score': 'value'})

r_haus = r.drop(columns=['Dice Score'])
r_haus['metric'] = 'haus'
r_haus = r_haus.rename(columns={'Hausdorff distance': 'value'})

r_out = pd.concat([r_dice,r_haus])

r_out.to_csv('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_final_results/metrics_val_set_f0_no_small_vols.csv')
