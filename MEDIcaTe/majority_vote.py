'''
Do majority voting among a number of input niftis
'''

from .utilities import *
import numpy as np

def majority_vote(out_f_name, *nifti_images):
    '''
    Performs majority voting between arbitrary number of inputs
    Inputs:
        - out_f_name: absolute path to output file containing the resulting segmentation of the vote.
        - *nifty_images: an arbitrary number of input files between which majority vote is performed. 
                         preferable these are int8 and contain only zeros and ones with ones being the segment to vote for. 
    
    '''
    template_image = get_nii_image_to_numpy_float32(nifti_images[0])
    added_image = np.zeros(template_image.shape, np.float32)
    out_image = np.zeros(template_image.shape, np.float32)
    for im in nifti_images:
        added_image = np.add(added_image, get_nii_image_to_numpy_float32(im))
    n_input_segments = len(nifti_images)
    out_image[added_image>n_input_segments/2] = 1
    generate_new_nii(nifti_images[0], out_image, out_f_name)