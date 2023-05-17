'''
Plot test cases to verify everything ok
'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool




def plot_preds(case):
    case_ct = f'{case[:-7]}_0000.nii.gz'
    case_pet = f'{case[:-7]}_0001.nii.gz'
    final_path_case = join(final_path, case[:-7])
    ct_path = join(images, case_ct)
    pt_path = join(images, case_pet)
    
    pred_label_path = join(predicted_labels, case)

    pred_label_path = None if not isfile(pred_label_path) else pred_label_path

    visualization(final_path=final_path_case,ct_path=ct_path,pet_path=pt_path,
                  l1_path=pred_label_path, l1_name='predicted',
                  l2_path=None, l2_name=None,
                  l3_path=None, l3_name=None,
                  slices=None, cropping=False, all_slices=False,
                  incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':

    #gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/ref_renamed'
    images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_n13/images'
    predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_n13/predictions_nnunet/labels_nn_unet_ensemble_final'
    #md_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/md_renamed'
    final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_n13/figs/w_preds'

    data_inputs = listdir(predicted_labels)
    
    pool = Pool(processes=10)
    pool.map(plot_preds, data_inputs)