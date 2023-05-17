from multiprocessing import Pool
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *


def remove_segm_outside_body(case):
    ext = os.path.splitext(case)[1]
    if ext == '.gz': 
        path_pred_case = join(pred_path,case)
        path_body_rois_case = join(path_body_rois,f'{case[:-7]}_0001_roi.nii.gz')
        pred_path_body_masked_case = join(pred_path_body_masked, case)

        pred_nii = get_nii_image_to_numpy(path_pred_case)
        body_roi_nii = get_nii_image_to_numpy(path_body_rois_case)

        pred_nii[body_roi_nii == 0] = 0

        generate_new_nii(path_pred_case, pred_nii, pred_path_body_masked_case)


if __name__ == '__main__':

    pred_path = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr' # the volumes to be edited
    path_body_rois = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/postprocessing/body_rois' # path to body rois
    pred_path_body_masked = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/swin_unetr_w_crop_foreground' #output path

    data_inputs = listdir(pred_path)
    data_inputs = data_inputs
    pool = Pool()
    pool.map(remove_segm_outside_body, data_inputs)