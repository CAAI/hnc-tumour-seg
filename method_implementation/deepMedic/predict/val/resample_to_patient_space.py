'''
Purpose: resample predicted data to original patient space.

'''

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.nii_resampling import resample_label_dst_like_src
from multiprocessing import Pool

gt = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
pred = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m4_f0/predictions_nnunet_id'
dest = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m4_f0/predictions_nnunet_id_patient_space'

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
    pool = Pool(processes=22)                         
    pool.map(resample_to_patient_space_swin_unetr, data_inputs)