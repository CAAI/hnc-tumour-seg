'''
Purpose: Get output of 5 inner-eye models and majority between them vote to get final result. 

This script is created to majority vote on test-set HNC02 (path to data hard-coded)
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.majority_vote import majority_vote
from MEDIcaTe.nii_resampling import *
from multiprocessing import Pool

def majority_vote_inner_eye(case):
    pred0_folder = join(pred0,case)
    if isdir(pred0_folder) & (case != 'thumbnails'):
        pred0_abspath = join(pred0,case,'tumor.nii.gz')
        pred1_abspath = join(pred1,case,'tumor.nii.gz')
        pred2_abspath = join(pred2,case,'tumor.nii.gz')
        pred3_abspath = join(pred3,case,'tumor.nii.gz')
        pred4_abspath = join(pred4,case,'tumor.nii.gz')
        #print(case)
        if (isfile(pred0_abspath) & isfile(pred1_abspath) & isfile(pred2_abspath) & isfile(pred3_abspath) & isfile(pred4_abspath)): #
            out_abs_fname = join(mv_dest,dict_innerEye2nnUNet.get(int(case)))
            #if not isfile(out_abs_fname): #only run for those not already done.
            print(f'now doing majority voting on {case}')
            majority_vote(out_abs_fname,pred0_abspath,pred1_abspath,pred2_abspath,pred3_abspath,pred4_abspath)#
        else:
            print(f'appears there was a missing prediction on {case}')
        if isfile(pred0_abspath) is False:
            print(f'missing file was on {pred0_abspath}')
        elif isfile(pred1_abspath) is False:
            print(f'missing file was on {pred1_abspath}')
        elif isfile(pred2_abspath) is False:
            print(f'missing file was on {pred2_abspath}')
        elif isfile(pred3_abspath) is False:
            print(f'missing file was on {pred3_abspath}')
        elif isfile(pred4_abspath) is False:
            print(f'missing file was on {pred4_abspath}')

if __name__ == '__main__':
    # path to predicted data
    pred0 = '/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-08-09T113226Z_HNC_tumor_dgk_HeadAndNeckBase/best_validation_epoch/Test'
    pred1 = '/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-08-09T092409Z_HNC_tumor_dgk_HeadAndNeckBase_f1/best_validation_epoch/Test'
    pred2 = '/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-08-09T133636Z_HNC_tumor_dgk_HeadAndNeckBase_f2/best_validation_epoch/Test'
    pred3 = '/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-08-09T154411Z_HNC_tumor_dgk_HeadAndNeckBase_f3/best_validation_epoch/Test'
    pred4 = '/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-08-09T174718Z_HNC_tumor_dgk_HeadAndNeckBase_f4/best_validation_epoch/Test'

    # load a mapping from inner-eye subject number to out ID's system: HNCXX_YYY.nii.gz
    dict_innerEye2nnUNet = load_pickle('/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/dict_innerEye2nnUNet.pkl')

    # destination of majority voted result
    mv_dest = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/output/test_set/majority_voted'

    data_inputs = listdir(pred0)
    pool = Pool(processes=22)
    pool.map(majority_vote_inner_eye, data_inputs)

    end = time.time()
    total_time = end-start
    print(f'Total time to do majority voting = {np.round(total_time,2)} sec.')