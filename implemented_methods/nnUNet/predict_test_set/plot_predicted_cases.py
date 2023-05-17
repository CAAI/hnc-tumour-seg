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
    
    gt_label_path = join(ref_labels, case)
    pred_label_path = join(predicted_labels, case)
    md_label_path = join(md_labels, case)

    gt_label_path = None if not isfile(gt_label_path) else gt_label_path

    visualization(final_path=final_path_case,ct_path=ct_path,pet_path=pt_path,
                  l1_path=gt_label_path, l1_name='ref. phys',
                  l2_path=None, l2_name=None,
                  l3_path=md_label_path, l3_name='eva. phys.',
                  slices=None, cropping=False, all_slices=False,
                  incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':
    ref_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/ref_renamed'
    md_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/md_renamed'
    images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/images'
    predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/predictions_nnunet/labels_nn_unet_ensemble_final'
    final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/figs/manual_assessment'

    data_inputs = ['HNC03_041.nii.gz'] # listdir(predicted_labels)
    # data_inputs = data_inputs[0:10]
    pool = Pool()
    pool.map(plot_preds, data_inputs)