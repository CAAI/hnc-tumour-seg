'''
Purpose:
Copy Tureckova validation fold 0 cases to a new folder
'''


from shutil import copyfile
from MEDIcaTe.file_folder_ops import *

tureckova_all = '/homes/kovacs/project_data/hnc-auto-contouring/tureckova/predicted/lowres_vnet1/training_cases'
folder_w_cases2copy = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0'
destination_folder = '/homes/kovacs/project_data/hnc-auto-contouring/tureckova/predicted/lowres_vnet1/val_f0_cases'

print('copying...')
for i,case in enumerate(listdir(folder_w_cases2copy)):
    src_file = join(tureckova_all,case)
    dst_file = join(destination_folder,case)
    copyfile(src_file,dst_file)
print('done')