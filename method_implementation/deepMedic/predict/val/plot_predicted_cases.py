'''
Plot output of DeepMedic

23-06-2022 this was run with the following paths to plot results
'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool


gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
predicted_labels = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0'
final_path = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0_plots'

def plot_swin_unetr(case):
    case_ct = f'{case[:-7]}_0000.nii.gz'
    case_pet = f'{case[:-7]}_0001.nii.gz'
    final_path_case = join(final_path, case[:-7])
    ct_path = join(images,case_ct)
    pt_path = join(images, case_pet)
    gt_label_path = join(gt_labels, case)
    pred_label_path = join(predicted_labels,case)
    visualization(final_path=final_path_case,ct_path=ct_path,pet_path=pt_path,l1_path=gt_label_path,l2_path=pred_label_path,l3_path=None,slices=None,cropping=False ,all_slices=False,incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':
    data_inputs = listdir(predicted_labels)
    #data_inputs = data_inputs[0:10]
    pool = Pool(processes=22)
    pool.map(plot_swin_unetr, data_inputs)