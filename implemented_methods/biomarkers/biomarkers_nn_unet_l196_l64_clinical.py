'''
Purpose: Collect biomarkers from t_64 and t_196 using original clinical
radiotherapy delineations as reference and nnUNet predictions as predicted. 
'''


from MEDIcaTe.biomarkers import get_all_biomarkers
from MEDIcaTe.file_folder_ops import listdir, join, isfile, basename, dirname
from multiprocessing import Pool
import pandas as pd


def get_biomarkers(case_label_abs_path):
    case_file = basename(case_label_abs_path)
    l64_or_r196 = basename(dirname(dirname(dirname(case_label_abs_path))))
    if l64_or_r196 == 't_l64':
        path_to_pet_case = join(path_to_pet_64, f'{case_file[:-7]}_0001.nii.gz')
    elif l64_or_r196 == 't_r196':
        path_to_pet_case = join(path_to_pet_196, f'{case_file[:-7]}_0001.nii.gz')
    else:
        print('WARNING: Did not find PET file')
        print(f'l64_or_r196 = {l64_or_r196}')
    
    print(f'Processing {case_label_abs_path}')

    biomarker = []
    value = []

    if (isfile(case_label_abs_path) & isfile(path_to_pet_case)):
        biomarkers = get_all_biomarkers(case_label_abs_path, path_to_pet_case)
        value.append(biomarkers.n_objects)
        value.append(biomarkers.mtv)
        value.append(biomarkers.suv_peak)
        value.append(biomarkers.suv_mean)
        value.append(biomarkers.suv_max)
        value.append(biomarkers.tlg)
    else:
        value.append('check_case_manually')
        value.append('check_case_manually')
        value.append('check_case_manually')
        value.append('check_case_manually')
        value.append('check_case_manually')
        value.append('check_case_manually')

    biomarker.append('n_objects')
    biomarker.append('mtv')
    biomarker.append('suv_peak')
    biomarker.append('suv_mean')
    biomarker.append('suv_max')
    biomarker.append('tlg')

    case_list = [case_file[:-7]] * 6

    return biomarker, value, case_list


if __name__ == '__main__':
    path_to_pet_64 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/images'
    path_to_pet_196 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
    
    label_niis_ref_64 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_clinical_errors_removed'
    label_niis_ref_196 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed'

    label_niis_pred_64 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/predictions_nnunet/labels_nn_unet_ensemble_final'
    label_niis_pred_196 = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_ensemble_final'

    
    case_list_ref_64 = listdir(label_niis_ref_64)
    case_list_ref_64 = [label_niis_ref_64 + '/' + case for case in case_list_ref_64]
    
    case_list_ref_196 = listdir(label_niis_ref_196)
    case_list_ref_196 = [label_niis_ref_196 + '/' + case for case in case_list_ref_196]

    case_list_ref = case_list_ref_64+case_list_ref_196
    
    case_list_pred_64 = listdir(label_niis_pred_64)
    case_list_pred_64 = [case for case in case_list_pred_64 if case.endswith(('.nii.gz'))]
    case_list_pred_64 = [label_niis_pred_64 + '/' + case for case in case_list_pred_64]

    case_list_pred_196 = listdir(label_niis_pred_196)
    case_list_pred_196 = [case for case in case_list_pred_196 if case.endswith(('.nii.gz'))]
    case_list_pred_196 = [label_niis_pred_196 + '/' + case for case in case_list_pred_196]

    case_list_pred = case_list_pred_64+case_list_pred_196

    pool = Pool(processes=20)

    biomarkers_ref = pool.map(get_biomarkers, case_list_ref) # , biomarkers_pred 

    biomarkers_pred = pool.map(get_biomarkers, case_list_pred) # , biomarkers_pred 

    biomarker = []
    value = []
    method = []
    case_list = []

    for element in biomarkers_ref:
        biomarker += element[0]
        value += element[1]
        method += ['ph'] * 6
        case_list += element[2]

    for element in biomarkers_pred:
        biomarker += element[0]
        value += element[1]
        method += ['dl'] * 6
        case_list += element[2]
    
    result_dest = ('/homes/kovacs/project_data/hnc-auto-contouring/'
                   'hnc_rigs_all/data_final_results')

    d_biomarkers = pd.DataFrame({'case': case_list, 'value': value,
                              'biomarker': biomarker, 'method': method})
                    
    d_biomarkers.to_csv(join(result_dest, 'biomarkers_l64_r196_clinRTref.csv'),
                     index=False)