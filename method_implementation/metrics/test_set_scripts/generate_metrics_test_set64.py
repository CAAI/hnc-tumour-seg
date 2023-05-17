'''
Purpose: Generate metrics for evaluation of implemented mehods
on test-data set of 196 cases.

metrics available at
https://github.com/CAAI/rh-scripts/blob/master/rhscripts/metrics.py
'''

from rhscripts.metrics import (dice_similarity,
                               getLesionLevelDetectionMetricsV2,
                               hausdorff_distance)
from MEDIcaTe.utilities import get_nii_image_to_numpy
from MEDIcaTe.file_folder_ops import basename, join, listdir
import pandas as pd
from multiprocessing import Pool


def generate_metrics_for_method(case):
    print(case)
    path_to_case_gt = join(path_folder_ground_truth, basename(case))
    path_to_case_pred = case

    gt_np = get_nii_image_to_numpy(path_to_case_gt)
    pred_np = get_nii_image_to_numpy(path_to_case_pred)

    dice = dice_similarity(gt_np, pred_np)
    hd = hausdorff_distance(gt_np, pred_np)
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
    predicted_nn_unet = ('/homes/kovacs/project_data/hnc-auto-contouring/'
                         'hnc_rigs_all/data_nifty/t_l64/predictions_nnunet'
                         '/labels_nn_unet_ensemble_final')

    path_folder_ground_truth = ('/homes/kovacs/project_data/'
                                'hnc-auto-contouring/hnc_rigs_all/'
                                'data_nifty/t_l64/labels/'
                                'labels_clinical_errors_removed')

    metric = []
    value = []
    method = []
    case_list = []

    list_of_cases_nn_unet = listdir(predicted_nn_unet)
    list_of_cases_nn_unet = [case for case in list_of_cases_nn_unet if
                             case.endswith(('.nii.gz'))]
    list_of_cases_nn_unet = [predicted_nn_unet + '/' + x for x in
                             list_of_cases_nn_unet]

    pool = Pool()
    case_data_all_nn_unet = pool.map(generate_metrics_for_method,
                                     list_of_cases_nn_unet)

    for case in case_data_all_nn_unet:
        metric += case[0]
        value += case[1]
        method += ['nnUNet'] * 8
        case_list += case[2]

    result_dest = ('/homes/kovacs/project_data/hnc-auto-contouring/'
                   'hnc_rigs_all/data_final_results')
    d_metrics = pd.DataFrame({'case': case_list, 'value': value,
                              'metric': metric, 'method': method})
    d_metrics.to_csv(join(result_dest, 'metrics_test64.csv'), index=False)
