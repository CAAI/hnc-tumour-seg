'''
Purpose:  Generate dataset.csv file for inner-eye deep learning

This all depends on how you strucuted your files. This script works for my structure, which is:
-- data
    -- d_test
        HNC01_000_0000.nii.gz
        HNC01_000_0001.nii.gz
        HNC01_001_0000.nii.gz
        HNC01_001_0001.nii.gz
        ...
where the ending _0000.nii.gz are CT's and _0001.nii.gz are PET.
'''

import time 
start = time.time()

from MEDIcaTe.utilities import *

if __name__=='__main__':

    path_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels' # files not used.
    path_images = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_test/converted_data_types'

    path_to_dataset_csv = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye'

    # paths relative to lcation of dataset.csv:
    rel_path_images = 'd_test/converted_data_types'
    rel_path_labels = 'd_test/converted_data_types/labels'

    subject = []
    filePath = []
    channel = []

    for i,f in enumerate(listdir(path_labels)):
        case_id = f[:-7]
        # add ct line
        filePath.append(join(rel_path_images,f'{case_id}_0000.nii.gz'))
        channel.append('ct')
        subject.append(i+1+835)

        # add pet line
        filePath.append(join(rel_path_images,f'{case_id}_0001.nii.gz'))
        channel.append('pet')
        subject.append(i+1+835)


        # add label line. This is not supposed to be done for test sets, but I can't get it to run, if I don't add it. 
        filePath.append(join(rel_path_labels,f'{case_id}.nii.gz'))
        channel.append('tumor')
        subject.append(i+1+835)
        

    out_dat = pd.DataFrame(list(zip(subject, filePath, channel)), columns =['subject', 'filePath', 'channel'])
    out_dat.to_csv(join(path_to_dataset_csv,'dataset_test196.csv'),index=False)
    print(out_dat.head(15))

    end = time.time()
    total_time = end-start
    print(f'Total time to generate dataset.csv = {np.round(total_time,2)} sec.')