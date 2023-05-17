'''
Purpose: resample predicted DEEP MEDIC DATA to original patient space.

'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.nii_resampling import resample_back_to_patient_space
from multiprocessing import Pool
import numpy as np

gt = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels'
pred = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_test_data_196/majority_voted'
dest = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/deep_medic/deep_medic_standard_5fold_result'

def resample_to_patient_space_swin_unetr(case):
    predicted = join(pred, case)
    original = join(gt,f'{case[:9]}.nii.gz')
    out = join(dest,case)
    print(f'predicted = {predicted}')
    print(f'original = {original}')
    print(f'out = {out}')
    #if not isfile(out):
    resample_back_to_patient_space(predicted, original, outname=out)
    #else:
    #print(f'{case} already resampled')

if __name__ == '__main__':
    data_inputs = listdir(pred)
    pool = Pool(processes=22)                         
    pool.map(resample_to_patient_space_swin_unetr, data_inputs)

    end = time.time()
    total_time = end-start
    print(f'Processed {len(data_inputs)} cases.')
    print(f'Total time to resample to patient space vote = {np.round(total_time,2)} sec.')