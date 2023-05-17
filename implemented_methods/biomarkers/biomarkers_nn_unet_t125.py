'''
Purpose: Collect biomarkers from t_64 dataset using MD REF delineations as 
reference and nnUNet predictions as predicted. 
'''


from MEDIcaTe.biomarkers import get_all_biomarkers
from MEDIcaTe.file_folder_ops import listdir, join, isfile, basename
from multiprocessing import Pool
import pandas as pd


def get_biomarkers(case_label_abs_path):
    case_file = basename(case_label_abs_path)
    path_to_pet_case = join(path_to_pet, f'{case_file[:-7]}_0001.nii.gz')
    
    print(f'Processing {case_label_abs_path}')

    biomarker = []
    value = []

    if isfile(case_label_abs_path):
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
    path_to_pet = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/images'
    label_niis_ref = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/labels'
    label_niis_pred = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/predictions_nnunet/labels_nn_unet_ensemble_final'
    #label_niis_md = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/md_renamed'

    case_list_ref = listdir(label_niis_ref)
    case_list_ref = [label_niis_ref + '/' + case for case in case_list_ref]
    
    #case_list_md = listdir(label_niis_md)
    #case_list_md = [label_niis_md + '/' + case for case in case_list_md]

    case_list_pred = listdir(label_niis_pred)
    case_list_pred = [case for case in case_list_pred if case.endswith(('.nii.gz'))]
    case_list_pred = [label_niis_pred + '/' + case for case in case_list_pred]

    pool = Pool()

    biomarkers_ref = pool.map(get_biomarkers, case_list_ref) # , biomarkers_pred 

    biomarkers_pred = pool.map(get_biomarkers, case_list_pred) # , biomarkers_pred 
    
    #biomarkers_md = pool.map(get_biomarkers, case_list_md)

    biomarker = []
    value = []
    method = []
    case_list = []

    for element in biomarkers_ref:
        biomarker += element[0]
        value += element[1]
        method += ['ph_ref'] * 6
        case_list += element[2]

    for element in biomarkers_pred:
        biomarker += element[0]
        value += element[1]
        method += ['dl'] * 6
        case_list += element[2]

    '''
    for element in biomarkers_md:
        biomarker += element[0]
        value += element[1]
        method += ['ph_eva'] * 6
        case_list += element[2]
    '''
    
    result_dest = ('/homes/kovacs/project_data/hnc-auto-contouring/'
                   'hnc_rigs_all/data_final_results')

    d_biomarkers = pd.DataFrame({'case': case_list, 'value': value,
                              'biomarker': biomarker, 'method': method})
                    
    d_biomarkers.to_csv(join(result_dest, 'biomarkers_t125_v2.csv'),
                     index=False)