# Load packages
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *
from multiprocessing import Pool

# At the source the images are resampled to median size of the dataset and normalized. '
# Images are saved as float32 and labels as INT8
image_src_path = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train_norm/images'
label_src_path = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train_norm/labels'
image_dst_path = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/imagesTr'

def conv_folder_to_4d(label_file):
    case = label_file[:-7]
    print(f'processing case {case}')
    ct_abs_path = join(image_src_path,f'{case}_0000.nii.gz')
    pet_abs_path = join(image_src_path,f'{case}_0001.nii.gz')
    pet_ct_dst_path = join(image_dst_path,label_file)
    convert_pet_ct_to_4d_nifti_channel_first(ct_abs_path, pet_abs_path, pet_ct_dst_path)

label_files = listdir(label_src_path)
pool = Pool()
pool.map(conv_folder_to_4d, label_files)

'''
Note: This was done on a 24 cpu-core computer and took about 20 minutes for 835 cases.
Consider if you'd rather just use a for-loop or fewer cores.
''' 