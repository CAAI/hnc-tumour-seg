'''
Purpose: Moving hecktor TRAINING data into nnUNET structure
'''

from MEDIcaTe.file_folder_ops import join, listdir
from MEDIcaTe.nii_resampling import resample_back_to_patient_space
from shutil import copyfile
from multiprocessing import Pool


def rescructure_and_resample_hecktor_to_nnunet(case):
    case_path = join(src_path, case)
    for file in listdir(case_path):
        f_path = join(case_path, file)
        print(f'______________________RUNNING CASE {case}______________________')
        print(f'f_path = {f_path}')
        if f_path.endswith('ct_gtvt.nii.gz'):
            dst_file = join(dest_path_labels, f'{case}.nii.gz')
            print(f'dst_file = {dst_file}')
            copyfile(f_path, dst_file)
            # label destination here
        elif f_path.endswith('ct.nii.gz'):
            dst_file = join(dest_path_images, f'{case}_0000.nii.gz')
            print(f'dst_file = {dst_file}')
            copyfile(f_path, dst_file)
        elif f_path.endswith('pt.nii.gz'):
            dst_file = join(dest_path_images, f'{case}_0001.nii.gz')
            ct_file = join(dest_path_images, f'{case}_0000.nii.gz')
            resample_back_to_patient_space(f_path, ct_file, outname = dst_file, verbose = True)
            print(f'dst_file = {dst_file}')
            # copyfile(f_path, dst_file)
        else:
            print('unkown ending - check case')
            print(f'f_path = {f_path}')


if __name__ == '__main__':
    src_path = '/homes/kovacs/project_data/hnc-auto-contouring/HECKTOR/hecktor_train/hecktor_nii'
    dest_path_images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_hecktor/train/images'
    dest_path_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_hecktor/train/labels'

    case_list = listdir(src_path)
    pool = Pool()
    pool.map(rescructure_and_resample_hecktor_to_nnunet, case_list)