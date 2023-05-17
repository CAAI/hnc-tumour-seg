'''
Plot output of nnUNEt
'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool


gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed'
images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_ensemble_final'
final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/figs/nnUNet'

def plot_nnunet(case):
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
    data_inputs = ['HNC02_176.nii.gz']
    pool = Pool(processes=20)
    pool.map(plot_nnunet, data_inputs)