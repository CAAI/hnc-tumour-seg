'''
Plot HECKTOR cases after resampling to check if it went OK


23-06-2022 this was run with the following paths to plot results

gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_patient_space'
final_path = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_plots_val_f0'


23-06-2022 then run as the following to plot rois:

gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/body_rois'
final_path = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/body_roi_figures'

'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool


gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_hecktor/train/labels'
images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_hecktor/train/images'
#predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr'
final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_hecktor/train/figs/resampling_check_ok'

def plot_swin_unetr(case):
    case_ct = f'{case[:-7]}_0000.nii.gz'
    case_pet = f'{case[:-7]}_0001.nii.gz'
    final_path_case = join(final_path, case[:-7])
    ct_path = join(images,case_ct)
    pt_path = join(images, case_pet)
    gt_label_path = join(gt_labels, case)
    #pred_label_path = join(predicted_labels,case)
    visualization(final_path=final_path_case,ct_path=ct_path,pet_path=pt_path,
                  l1_path=gt_label_path, l1_name='ground truth',
                  l2_path=None, l2_name=None,
                  slices=None, cropping=False, all_slices=False,
                  incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':
    data_inputs = listdir(gt_labels)
    data_inputs = data_inputs[0:10]
    pool = Pool()
    pool.map(plot_swin_unetr, data_inputs)
    print(data_inputs)