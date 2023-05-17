from MEDIcaTe.file_folder_ops import load_pickle
import pandas as pd
import numpy as np

detection_rate = pd.read_csv('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/md_delineation_study/MD_answers/tabel_label_overview.csv',sep=';')

metrics = pd.read_csv('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_final_results/metrics_test64_clinical_study_final_manually_fixed3.csv')

ids_random_nn_unet = pd.read_csv('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/md_delineation_study/Xmd_study_all_info.csv')
map_random2key = dict(ids_random_nn_unet[['rand_key_ref', 'key']].values)
map_key2nn_unet = load_pickle('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/convert_to_nn_unet_scripts/7c_nn_unet_names_pet_negatives.pkl')

dice_nnunet = metrics[(metrics['metric'] == 'dice') & (metrics['method'] == 'nnUNet')]

dice_nnunet['detected'] = np.where(dice_nnunet['value'] > 0, 1, 0)

map_dl_detected = dict(dice_nnunet[['case', 'detected']].values)

detection_rate['dl_exist'] = detection_rate['nn_unet_id'].map(map_dl_detected)
detection_rate['key'] = detection_rate['ref_key'].map(map_random2key)
detection_rate['nn_unet_id_negative'] = detection_rate['key'].map(map_key2nn_unet)

# manually add cases that were checked based on plot
detection_rate.loc[detection_rate['nn_unet_id']=='HNC03_054', 'dl_exist'] = 1
detection_rate.loc[detection_rate['nn_unet_id']=='HNC03_056', 'dl_exist'] = 1

detection_rate.to_csv('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_final_results/tabel_label_overview.csv')
