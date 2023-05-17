'''
Plot output of swin-unetr. 

'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import join, listdir
from multiprocessing import Pool


gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed'
images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/swin_unetr_w_crop_foreground'
final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/figs/swin_unetr/outliers_body_masked'

def plot_swin_unetr(case):
    case_ct = f'{case[:-7]}_0000.nii.gz'
    case_pet = f'{case[:-7]}_0001.nii.gz'
    final_path_case = join(final_path, case[:-7])
    ct_path = join(images, case_ct)
    pt_path = join(images, case_pet)
    gt_label_path = join(gt_labels, case)
    pred_label_path = join(predicted_labels, case)
    visualization(final_path=final_path_case, ct_path=ct_path, pet_path=pt_path,
                  l1_path=gt_label_path, l1_name='ground truth',
                  l2_path=pred_label_path, l2_name='predicted',
                  slices=None, cropping=False, all_slices=False,
                  incl_info=True, outline=True, verbose=True)

if __name__ == '__main__':
    #data_inputs = listdir(predicted_labels)
    #data_inputs = data_inputs[0:10]
    data_inputs = ['HNC02_060.nii.gz']
    pool = Pool()
    pool.map(plot_swin_unetr, data_inputs)
    print(data_inputs)
