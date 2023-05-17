

from MEDIcaTe.roi_generators import *
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool

def generate_rois(case):
    cur_nifti_file = join(path_to_images, case)
    if case[-11:-7] == '0001': # only run for PET files
        generate_rois_dm_pt(cur_nifti_file, path_to_rois, clobber = True)


if __name__=='__main__':
    path_to_images = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images'
    path_to_rois = '/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/swin_unetr/postprocessing/body_rois'
    data_list = listdir(path_to_images)
    pool = Pool()
    pool.map(generate_rois, data_list)