'''
Purpose: resample predicted test data labels to original patient space.
For Swin-Unetr.
'''

import time 
start = time.time()

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.nii_resampling import resample_label_dst_like_src
from multiprocessing import Pool
import numpy as np

gt = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels'
pred = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/output/test196_m0'
dest = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr'

def resample_to_patient_space_swin_unetr(case):
    predicted = join(pred, case)
    original = join(gt,f'{case[:9]}.nii.gz')
    out = join(dest,case)
    print(f'predicted = {predicted}')
    print(f'original = {original}')
    print(f'out = {out}')
    #if not isfile(out):
    resample_label_dst_like_src(predicted, original, outname=out)
    #else:
    #    print(f'{case} already resampled (file existed on destination)')

if __name__ == '__main__':
    data_inputs = listdir(pred)
    pool = Pool(processes=22)                         
    pool.map(resample_to_patient_space_swin_unetr, data_inputs)
    end = time.time()
    total_time = end-start
    print(f'Total time to resample to patient space = {np.round(total_time,2)} sec.')