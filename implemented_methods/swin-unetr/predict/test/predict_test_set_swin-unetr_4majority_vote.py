'''
Purpose: Get output of 5 swin-unetr models, majority between them vote to get prediction final result. 

This script is created to majority vote on test-set HNC02 (path to data hard-coded)
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.majority_vote import majority_vote
from MEDIcaTe.nii_resampling import *
from multiprocessing import Pool

def majority_vote_swin_unetr(case):
    pred0_abspath = join(pred0,case)
    pred1_abspath = join(pred1,case)
    pred2_abspath = join(pred2,case)
    pred3_abspath = join(pred3,case)
    pred4_abspath = join(pred4,case)
    #print(case)
    if (isfile(pred0_abspath) & isfile(pred1_abspath) & isfile(pred2_abspath) & isfile(pred3_abspath) & isfile(pred4_abspath)): #
        out_abs_fname = join(mv_dest,case)
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
    pred0 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m0'
    pred1 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m1'
    pred2 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m2'
    pred3 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m3'
    pred4 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m4'


    # destination of majority voted result
    mv_dest = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/majority_voted'

    data_inputs = listdir(pred0)
    pool = Pool(processes=22)
    pool.map(majority_vote_swin_unetr, data_inputs)

    end = time.time()
    total_time = end-start
    print(f'Total time to do majority voting = {np.round(total_time,2)} sec.')