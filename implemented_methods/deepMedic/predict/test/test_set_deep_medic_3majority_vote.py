'''
Purpose: Get output of 5 DEEP MEDIC models majority vote to get final result. 
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.majority_vote import majority_vote
from MEDIcaTe.nii_resampling import *
from multiprocessing import Pool

# path to predicted data
pred0 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/predictions/testSessionDm_r196_m0/predictions'
pred1 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/predictions/testSessionDm_r196_m1/predictions'
pred2 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/predictions/testSessionDm_r196_m2/predictions'
pred3 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/predictions/testSessionDm_r196_m3/predictions'
pred4 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/predictions/testSessionDm_r196_m4/predictions'

# destination of majority voted result
mv_dest = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/majority_voted'

def majority_vote_inner_eye(case):
    if isdir(pred0):
        if case[10:14]=='Segm':
            pred0_abspath = join(pred0,case)
            pred1_abspath = join(pred1,case)
            pred2_abspath = join(pred2,case)
            pred3_abspath = join(pred3,case)
            pred4_abspath = join(pred4,case)
            out_abs_fname = join(mv_dest,f'{case[:9]}.nii.gz')
            print(case)
            #print(pred0_abspath)
            #print(out_abs_fname)
            if (isfile(pred0_abspath) & isfile(pred1_abspath) & isfile(pred2_abspath) & isfile(pred3_abspath) & isfile(pred4_abspath)):
                if not isfile(out_abs_fname):
                    #print('WILL DO MAJORITY VOTIG HERE')
                    majority_vote(out_abs_fname,pred0_abspath,pred1_abspath,pred2_abspath,pred3_abspath,pred4_abspath)
            else:
                print(f'appears there was a missing prediction on {case}')

if __name__ == '__main__':
    data_inputs = listdir(pred0)
    pool = Pool(processes=22)                         
    pool.map(majority_vote_inner_eye, data_inputs)

    end = time.time()
    total_time = end-start
    print(f'Processed {len(data_inputs)} cases.')
    print(f'Total time to majotiry vote for deep medic = {np.round(total_time,2)} sec.')
    