from MEDIcaTe.file_folder_ops import listdir, basename
import pandas as pd
import numpy as np
from multiprocessing import Pool
from MEDIcaTe.file_folder_ops import join
from MEDIcaTe.utilities import get_nii_image_to_numpy


def generate_detection_metrics_for_method(case):

    path_to_case_pred = case
    pred_np = get_nii_image_to_numpy(path_to_case_pred).astype(int)

    value = np.any((pred_np == 1)).astype(int)
    case = [basename(case)[:-7]]

    return value, case


if __name__ == '__main__':
    predicted_deep_medic = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/deep_medic/deep_medic_standard_5fold_result'
    predicted_inner_eye = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/inner_eye'
    predicted_nn_unet = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_ensemble_final'
    predicted_swin_unetr = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/swin_unetr_w_crop_foreground' 
    predicted_tureckova = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/tureckova/vnet1_lowres_timed'

    #path_folder_ground_truth = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed'

    value = []
    method = []
    metric = []
    case_list = []

    list_of_cases_dm = listdir(predicted_deep_medic)
    list_of_cases_dm = [predicted_deep_medic + '/' + x for x in list_of_cases_dm]

    list_of_cases_inner_eye = listdir(predicted_inner_eye)
    list_of_cases_inner_eye = [predicted_inner_eye + '/' + x for x in list_of_cases_inner_eye]

    list_of_cases_nn_unet = listdir(predicted_nn_unet)
    list_of_cases_nn_unet = [case for case in list_of_cases_nn_unet if case.endswith(('.nii.gz'))]
    list_of_cases_nn_unet = [predicted_nn_unet + '/' + x for x in list_of_cases_nn_unet]

    list_of_cases_tureckova = listdir(predicted_tureckova)
    list_of_cases_tureckova = [case for case in list_of_cases_tureckova if case.endswith(('.nii.gz'))]
    list_of_cases_tureckova = [predicted_tureckova + '/' + x for x in list_of_cases_tureckova]
    
    list_of_cases_swin_unetr = listdir(predicted_swin_unetr)
    list_of_cases_swin_unetr = [predicted_swin_unetr + '/' + x for x in list_of_cases_swin_unetr]

    pool = Pool()
    case_data_all_dm = pool.map(generate_detection_metrics_for_method, list_of_cases_dm)
    case_data_all_inner_eye = pool.map(generate_detection_metrics_for_method, list_of_cases_inner_eye)
    case_data_all_nn_unet = pool.map(generate_detection_metrics_for_method, list_of_cases_nn_unet)
    case_data_all_tureckova = pool.map(generate_detection_metrics_for_method, list_of_cases_tureckova)
    case_data_all_swin_unetr = pool.map(generate_detection_metrics_for_method, list_of_cases_swin_unetr)
    
    for case in case_data_all_dm:
        metric+=['detection']
        value+=[case[0]]
        case_list+=case[1]
        method += ['deep_medic']

    for case in case_data_all_inner_eye:
        metric+=['detection']
        value+=[case[0]]
        case_list+=case[1]
        method += ['inner_eye']

    for case in case_data_all_nn_unet:
        metric+=['detection']
        value+=[case[0]]
        case_list+=case[1]
        method += ['nnUNet']

    for case in case_data_all_tureckova:
        metric+=['detection']
        value+=[case[0]]
        case_list+=case[1]
        method += ['tureckova']

    for case in case_data_all_swin_unetr:
        metric+=['detection']
        value+=[case[0]]
        case_list+=case[1]
        method += ['swin_unetr']

    
    result_dest = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_final_results'
    d_metrics = pd.DataFrame({'case':case_list,'value':value,'metric':metric,'method':method})
    d_metrics.to_csv(join(result_dest, 'metrics_detection_test196_errors_removed.csv'), index=False)