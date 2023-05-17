from scipy.ndimage import label, generate_binary_structure
from MEDIcaTe.utilities import *



def remove_small_vols(nii_label_file,vol_size,out_destination):
    '''
    Purpose: remove all small volumes in a label image smaller than a certain number of voxels.
    
    Inputs:
        nii_label_file: label file in nifti format (nii.gz)
        vol_size: the max number of connected to keep
        out_destination: abspath to file to save resulting segment
    '''
    s = generate_binary_structure(3,3)
    nii_label_numpy = get_nii_image_to_numpy(nii_label_file)
    
    labeled_array, num_features = label(nii_label_numpy, s)
    label_size = [(labeled_array == label).sum() for label in range(num_features + 1)]
    
    # now remove the labels
    for lab,size in enumerate(label_size):
        if size <= vol_size:
            nii_label_numpy[labeled_array == lab] = 0
    
    generate_new_nii(nii_label_file, nii_label_numpy, out_destination)


if __name__ == '__main__':
    nii_label_file_abs_path = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_patient_space_body_masked/HNC01_748.nii.gz'
    out_destination = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted_patient_space_body_masked_no_small_vols'
    remove_small_vols(nii_label_file_abs_path, 15, out_destination)
