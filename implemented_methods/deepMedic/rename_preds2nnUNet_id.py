from MEDIcaTe.file_folder_ops import *
from shutil import copyfile

pred_folder = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m4_f0/predictions'
pred_dst_folder = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m4_f0/predictions_nnunet_id'
print('copying...')
for i,file in enumerate(listdir(pred_folder)):
    if 'Segm' in file:
        new_name = f'{file[:9]}.nii.gz'
        new_abspath = join(pred_dst_folder,new_name)
        src_path = join(pred_folder,file)
        copyfile(src_path,new_abspath) 
print('done')