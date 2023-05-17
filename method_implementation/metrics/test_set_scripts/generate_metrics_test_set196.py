'''
Purpose: Generate metrics for evaluation of implemented mehods on test-data set of 196 cases.

metrics available at https://github.com/CAAI/rh-scripts/blob/master/rhscripts/metrics.py
'''

from rhscripts.metrics import dice_similarity, getLesionLevelDetectionMetricsV2
from MEDIcaTe.calculate_dice_haus import hausdorff_distance_with_resampling
from MEDIcaTe.utilities import get_nii_image_to_numpy
from MEDIcaTe.file_folder_ops import *
import pandas as pd
from multiprocessing import Pool
import collections

def generate_metrics_for_method(case):
    print(case)
    path_to_case_gt = join(path_folder_ground_truth, basename(case))
    path_to_case_pred = case
    
    gt_np = get_nii_image_to_numpy(path_to_case_gt)
    pred_np = get_nii_image_to_numpy(path_to_case_pred)

    dice = dice_similarity(gt_np, pred_np)
    hd = hausdorff_distance_with_resampling(path_to_case_gt, path_to_case_pred)
    lesion_metrics = getLesionLevelDetectionMetricsV2(gt_np, pred_np)

    metric = []
    value = []
    case_list = []

    value.append(dice)
    value.append(hd)
    value.append(lesion_metrics.precision)
    value.append(lesion_metrics.recall)
    value.append(lesion_metrics.f1)
    value.append(lesion_metrics.TP)
    value.append(lesion_metrics.FP)
    value.append(lesion_metrics.FN)

    metric.append('dice')
    metric.append('hd')
    metric.append('precision')
    metric.append('recall')
    metric.append('f1')
    metric.append('TP')
    metric.append('FP')
    metric.append('FN')

    case_list = [basename(case)[:-7]] * 8

    return metric, value, case_list


if __name__ == '__main__':
    predicted_deep_medic = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/deep_medic/deep_medic_standard_5fold_result'
    predicted_inner_eye = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/inner_eye'
    predicted_nn_unet = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_ensemble_final'
    predicted_swin_unetr = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/swin_unetr_w_crop_foreground' 
    predicted_tureckova = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/tureckova/vnet1_lowres_timed'

    path_folder_ground_truth = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed'

    metric = []
    value = []
    method = []
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
    case_data_all_dm = pool.map(generate_metrics_for_method, list_of_cases_dm)
    case_data_all_inner_eye = pool.map(generate_metrics_for_method, list_of_cases_inner_eye)
    case_data_all_nn_unet = pool.map(generate_metrics_for_method, list_of_cases_nn_unet)
    case_data_all_tureckova = pool.map(generate_metrics_for_method, list_of_cases_tureckova)
    case_data_all_swin_unetr = pool.map(generate_metrics_for_method, list_of_cases_swin_unetr)

    for case in case_data_all_dm:
        metric+=case[0]
        value+=case[1]
        method += ['deep_medic'] * 8
        case_list+=case[2]

    for case in case_data_all_inner_eye:
        metric+=case[0]
        value+=case[1]
        method += ['inner_eye'] * 8
        case_list+=case[2]

    for case in case_data_all_nn_unet:
        metric+=case[0]
        value+=case[1]
        method += ['nnUNet'] * 8
        case_list+=case[2]

    for case in case_data_all_tureckova:
        metric+=case[0]
        value+=case[1]
        method += ['tureckova'] * 8
        case_list+=case[2]

    for case in case_data_all_swin_unetr:
        metric+=case[0]
        value+=case[1]
        method += ['swin_unetr'] * 8
        case_list+=case[2]

    result_dest = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_final_results'
    d_metrics = pd.DataFrame({'case':case_list,'value':value,'metric':metric,'method':method})
    d_metrics.to_csv(join(result_dest,'metrics_test196_errors_removed_swin_masked_v4.csv'),index=False)

