'''
Plot test cases to verify everything ok
'''

from MEDIcaTe.optimized_visualization import visualization
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool




def plot_preds(case):
    case_ct = f'{case[:-7]}_0000.nii.gz'
    case_pet = f'{case[:-7]}_0001.nii.gz'
    final_path_case = join(final_path, case[:-7]+'_FIG2_outline_')
    ct_path = join(images, case_ct)
    pt_path = join(images, case_pet)
    
    gt_label_path = join(gt_labels,case)
    pred_label_path = join(predicted_labels, case)
    md_label_path = join(md_labels, case)

    gt_label_path = None if not isfile(gt_label_path) else gt_label_path

    visualization(final_path=final_path_case+'empty',ct_path=ct_path,pet_path=pt_path,
                  l1_path= None, #,gt_label_path,
                  l1_name= None, #'ref. expert'
                  l2_path= None, # pred_label_path, #pred_label_path, # 
                  l2_name= None, #'AI', #'AI', # 
                  l3_path= None, #md_label_path, # md_label_path, # md_label_path, 
                  l3_name= None, #'phys. eva',#'eval. expert', # 'phys. eva',
                  slices=[86], cropping=False, all_slices=True, # for slices to do a specific do: 
                  incl_info=True,outline=False,verbose=True)

    visualization(final_path=final_path_case+'_ref',ct_path=ct_path,pet_path=pt_path,
                  l1_path= gt_label_path, #,gt_label_path,
                  l1_name= 'ref. expert', #'ref. expert'
                  l2_path= None, # pred_label_path, #pred_label_path, # 
                  l2_name= None, #'AI', #'AI', # 
                  l3_path= None, #md_label_path, # md_label_path, # md_label_path, 
                  l3_name= None, #'phys. eva',#'eval. expert', # 'phys. eva',
                  slices=[86], cropping=False, all_slices=False, # for slices to do a specific do: 
                  incl_info=True,outline=True,verbose=True)
    
    visualization(final_path=final_path_case+'_AI',ct_path=ct_path,pet_path=pt_path,
                  l1_path= None, #gt_label_path, #,gt_label_path,
                  l1_name= None, #'ref. expert', #'ref. expert'
                  l2_path= pred_label_path, #pred_label_path, # 
                  l2_name= 'AI', #'AI', # 
                  l3_path= None, #md_label_path, # md_label_path, # md_label_path, 
                  l3_name= None, #'phys. eva',#'eval. expert', # 'phys. eva',
                  slices=[86], cropping=False, all_slices=False, # for slices to do a specific do: 
                  incl_info=True,outline=True,verbose=True)
    
    visualization(final_path=final_path_case+'_eva',ct_path=ct_path,pet_path=pt_path,
                  l1_path= None, #gt_label_path, #,gt_label_path,
                  l1_name= None, #'ref. expert', #'ref. expert'
                  l2_path= None, #pred_label_path, #pred_label_path, # 
                  l2_name= None, #'AI', #'AI', # 
                  l3_path= md_label_path, # md_label_path, # md_label_path, 
                  l3_name= 'phys. eva',#'eval. expert', # 'phys. eva',
                  slices=[86], cropping=False, all_slices=False, # for slices to do a specific do: 
                  incl_info=True,outline=True,verbose=True)

if __name__ == '__main__':
    gt_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/ref_renamed'
    images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/images'
    predicted_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/predictions_nnunet/labels_nn_unet_ensemble_final'
    md_labels = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/labels/labels_doctor_study/md_renamed'
    final_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_l64/figs/manual_assessment'

    data_inputs = ['HNC03_030.nii.gz']  # listdir(predicted_labels) #, 'HNC03_043.nii.gz'
    #data_inputs = listdir(predicted_labels)
    #data_inputs = [item for item in data_inputs if "nii.gz" in item]
    #data_inputs = data_inputs
    pool = Pool()
    pool.map(plot_preds, data_inputs)