'''
Purpose: Generate ROI's needed by for normalization and training DeepMedic.

DeepMedic prefers to have a ROI of the body to avoid too much air in the input.
DeepMedic uses this ROI during training to ensure sampling from meaningful areas.
During normalization we also use mean and std from the ROI.
'''
from .file_folder_ops import * 
import nibabel as nib
import numpy as np
from scipy.ndimage import gaussian_filter

def generate_rois_dm_ct(ct_image_nifty, destination_path):
    '''
    Parameters:
        ct_image_nifty: The nifty input CT image used to generate the ROI
        destination_path: The output folder where the output ROI-image will be saved
    '''
    ct_img = nib.load(ct_image_nifty) 
    data = ct_img.get_data()    # load nifty image to numpy
    new_data = data.copy()      # copy the data (avoid overwrithing anything)

    # generate the ROI which has 0 for air and 1 for everything else
    threshold = -700
    new_data[new_data >= threshold] = 1
    new_data[new_data < threshold] = 0
    

    # save the resulting nifty image
    f_name =  f'{os.path.basename(ct_image_nifty)[:-7]}_roi.nii.gz' # output nifty filename
    roi_img = nib.Nifti1Image(new_data, ct_img.affine, ct_img.header)
    nib.save(roi_img, os.path.join(destination_path,f_name))


def generate_rois_dm_pt(pt_image_nifty, destination_path, clobber = False):
    '''
    Parameters:
        pt_image_nifty: The nifty input PET image used to generate the ROI
        destination_path: The output folder where the output ROI-image will be saved
        clobber: Set to True if you want to overwrite existing ROIs
    '''
    # check if the file we want to create already exists first
    output_fname =  f'{os.path.basename(pt_image_nifty)[:-7]}_roi.nii.gz' # output nifty filename
    output_fname_w_path = os.path.join(destination_path, output_fname)
    if not isfile(output_fname_w_path) or clobber:
        ct_img = nib.load(pt_image_nifty) 
        data = ct_img.get_data()    # load nifty image to numpy
        new_data = data.copy()      # copy the data (avoid overwrithing anything)

        # generate the ROI 
        # smooth the image first to get a nicer ROI
        new_data = gaussian_filter(new_data, sigma=5)

        #do the thresholding with 0 for air and 1 for everything else
        threshold = 0.2
        new_data[new_data >= threshold] = 1
        new_data[new_data < threshold] = 0
        
        # save the resulting nifty image
        roi_img = nib.Nifti1Image(new_data, ct_img.affine, ct_img.header)
        nib.save(roi_img, output_fname_w_path)