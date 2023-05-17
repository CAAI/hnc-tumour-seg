'''
Functions for various intensity normalization scheems
DGK 06-04-2022
'''

from .utilities import *
from .file_folder_ops import *
import numpy as np
import numpy.ma as ma

def norm_0mean_1variance(input_nii, output_path, mean, std):
    '''
    Purpose: Perform zero mean and unit variance normalization
    of Nifty image. 

    Parameters:
        - input_nifty: the file to be normalized
        - mean: mean to be used for normalization
        - std: std to be used for normalization
        - output_path: folder in which to save the normalized file

    Return values:
        - numpy ndarray containing the image data
    '''
    # get_nii
    data = get_nii_image_to_numpy(input_nii)
    # normalize
    data_norm = (data - mean) / std
    # save
    output_fname = join(output_path, basename(input_nii))
    generate_new_nii(input_nii, data_norm, output_fname)


def get_nii_mean_std(input_nii):
    data = get_nii_image_to_numpy(input_nii)
    input_mean = np.mean(data)
    input_std = np.std(data)
    return input_mean, input_std


def get_nii_mean_std_in_roi(input_nii, input_roi):
    data = get_nii_image_to_numpy(input_nii)
    roi = get_nii_image_to_numpy(input_roi)
    data_out = ma.masked_where(roi==0, data)
    input_mean = np.mean(data_out)
    input_std = np.std(data_out)
    return input_mean, input_std


