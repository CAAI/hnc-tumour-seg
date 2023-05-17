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
    
    gt_label_path = join(gt_labels,case)
    pred_label_path = join(predicted_labels, case)
    #md_label_path = join(md_labels, case)

    gt_label_path = None if not isfile(gt_label_path) else gt_label_path

    visualization(final_path=final_path_case,ct_path=ct_path,pet_path=pt_path,
                  l1_path=gt_label_path, l1_name='ground truth',
                  l2_path=pred_label_path, l2_name='predicted',
                  l3_path=None, l3_name=None,
                  slices=None, cropping=False, all_slices=False,
                  incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':
    gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/labels'
    images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/images'
    predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/predictions_nnunet/labels_nn_unet_ensemble_final'
    #md_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/data_nifti/labels'
    final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_hgh_all/figures'

    #data_inputs = ['HNC05_001.nii.gz'] # HNC03_040.nii.gz','HNC03_010.nii.gz','HNC03_007.nii.gz','HNC03_028.nii.gz'] # listdir(predicted_labels)
    # data_inputs = data_inputs[0:10]
    #pool = Pool()
    #pool.map(plot_preds, data_inputs)
    plot_preds('HNC05_001.nii.gz')