'''
Purpose: resample predicted test data labels to original patient space.
For Inner-Eye.
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.nii_resampling import resample_back_to_patient_space
from multiprocessing import Pool
import numpy as np

gt = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels'
pred = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/output/test_set/majority_voted'
dest = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/inner_eye'

def resample_to_patient_space_swin_unetr(case):
    predicted = join(pred, case)
    original = join(gt,f'{case[:9]}.nii.gz')
    out = join(dest,case)
    print(f'predicted = {predicted}')
    print(f'original = {original}')
    print(f'out = {out}')
    if not isfile(out):
        resample_back_to_patient_space(predicted, original, outname=out)
    else:
        print(f'{case} already resampled (file existed on destination)')

if __name__ == '__main__':
    data_inputs = listdir(pred)
    pool = Pool(processes=22)                         
    pool.map(resample_to_patient_space_swin_unetr, data_inputs)

    end = time.time()
    total_time = end-start
    print(f'Total time to do majority voting = {np.round(total_time,2)} sec.')