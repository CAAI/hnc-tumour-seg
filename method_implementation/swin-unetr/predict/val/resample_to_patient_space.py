'''
Purpose: resample predicted data to original patient space.

23-jun-2022: used to reample model output to patient space with:
gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
pred = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted'
dest = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_patient_space'


23-jun-2022: used to resample body rois to patient space.
'''

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.nii_resampling import resample_label_dst_like_src
from multiprocessing import Pool

gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
pred = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train/rois' # dat to resample
dest = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/body_rois'

def resample_to_patient_space_swin_unetr(case):
    predicted = join(pred, case)
    original = join(gt,f'{case[:9]}.nii.gz')
    out = join(dest,case)
    print(f'predicted = {predicted}')
    print(f'original = {original}')
    print(f'out = {out}')
    if not isfile(out):
        resample_label_dst_like_src(predicted, original, outname=out)
    else:
        print(f'{case} already resampled')

if __name__ == '__main__':
    data_inputs = listdir(pred)
    pool = Pool()                         
    pool.map(resample_to_patient_space_swin_unetr, data_inputs)