'''
Collection of functions useful for image processing
'''
from .file_folder_ops import *
import nibabel as nib
import numpy as np
import shutil

def control_nii_orientation(nii_1_fpath, nii_2_fpath = None, verbose = False):
    '''
    Check the orientation on nifti files
    Will simply print the orientation of the files passed
    Parameters:
        nii_1_fpath: path to a nifti file
        nii_2_fpath: path to a second nifti file
    '''
    if nii_2_fpath == None:
        nii_1 = nib.load(nii_1_fpath)
        nii_1_orient = nib.orientations.aff2axcodes(nii_1.affine)
        if verbose:
            print(f'{basename(nii_1_fpath)}: {nii_1_orient}')
        return nii_1_orient
    else:
        nii_1 = nib.load(nii_1_fpath)
        nii_2 = nib.load(nii_2_fpath)
        nii_1_orient = nib.orientations.aff2axcodes(nii_1.affine)
        nii_2_orient = nib.orientations.aff2axcodes(nii_2.affine)
        if verbose:
            print(f'{basename(nii_1_fpath)}: {nii_1_orient}, basename(nii_2_fpath): {nii_2_orient}')
        return nii_1_orient, nii_2_orient

def get_header(nii_1_fpath):
    '''
    Returns the header of a nifti file.
    '''
    n1_img = nib.load(nii_1_fpath)
    n1_header = n1_img.header
    return n1_header

def get_affine(nii_1_fpath):
    '''
    Returns the affine matrix of a nifti file.
    '''
    n1_img = nib.load(nii_1_fpath)
    n1_affine = n1_img.affine
    return n1_affine

def get_nii_image_to_numpy(path_to_nii):
    '''
    Load image data in nifti file to a numpy array
    '''
    img = nib.load(path_to_nii)
    data = img.get_fdata()
    new_data = data.copy() # don't overwrite anything in original file
    return new_data

def get_nii_image_to_numpy_float32(path_to_nii):
    '''
    Load image data in nifti file to a float_32 numpy array 
    '''
    img = nib.load(path_to_nii)
    data = img.get_fdata(dtype = np.float32)
    new_data = data.copy() # don't overwrite anything in original file
    return new_data

def get_nii_label_to_numpy_int16(path_to_nii):
    '''
    Load image data in nifti file to a int16 numpy array 
    '''
    img = nib.load(path_to_nii)
    data = img.get_fdata(dtype = np.int16)
    new_data = data.copy() # don't overwrite anything in original file
    return new_data

def get_nii_label_to_numpy_int8(path_to_nii):
    '''
    Load image data in nifti file to a int8 numpy array 
    '''
    img = nib.load(path_to_nii)
    data = img.get_fdata(dtype = np.int8)
    new_data = data.copy() # don't overwrite anything in original file
    return new_data

def generate_new_nii(container, new_dat, output_fname):
    '''
    Generate a new nifti-file as container but with modified new_dat
    
    Parameters
        - container: Nifti input-file. The affine and header of this
        file will be matched in the output file. 
        - new_dat: Numpy ND-array with image data for the new nifti.
        - output_fname: The output filename (include full path)
    '''
    affine = get_affine(container)
    header = get_header(container)
    new_nii = nib.Nifti1Image(new_dat, affine, header)
    nib.save(new_nii, output_fname)

def convert_nii_to_int16(nii_image_src,nii_image_dst):
    '''
    Purpose: Create a copy of nifty file in int16 format.
    Parameters
        - nii_image_src: Nifti source file.
        - nii_image_dst: Nifti destination file
    '''
    # the code is adapted from https://stackoverflow.com/questions/44397617/change-data-type-in-numpy-and-nibabel
    image = nib.load(nii_image_src)
    
    # to be extra sure of not overwriting data:
    new_data = np.copy(image.get_data())
    hd = image.header

    # in case you want to remove nan: (DGK: I want scripts to fail if these give NAN so I don't remove)
    # new_data = np.nan_to_num(new_data) 
    array_sum = np.sum(new_data)
    array_has_nan_before = np.isnan(array_sum)

    # update data type:
    new_dtype = np.int16  # for example to cast to int8.
    new_data = new_data.astype(new_dtype)
    image.set_data_dtype(new_dtype)
    
    array_sum = np.sum(new_data)
    array_has_nan_after = np.isnan(array_sum)

    if array_has_nan_before:
        print(f'{array_has_nan_before} had NANs before conversion')
    if array_has_nan_after:
        print(f'{array_has_nan_after} had NANs after conversion')

    # if nifty1
    if hd['sizeof_hdr'] == 348:
        new_image = nib.Nifti1Image(new_data, image.affine, header=hd)
    # if nifty2
    elif hd['sizeof_hdr'] == 540:
        new_image = nib.Nifti2Image(new_data, image.affine, header=hd)
    else:
        raise IOError('Input image header problem')

    nib.save(new_image, nii_image_dst)

def convert_nii_to_float32(nii_image_src,nii_image_dst):
    '''
    Purpose: Create a copy of nifty file in float32 format.
    Parameters
        - nii_image_src: Nifti source file.
        - nii_image_dst: Nifti destination file
    '''
    # the code is adapted from https://stackoverflow.com/questions/44397617/change-data-type-in-numpy-and-nibabel
    image = nib.load(nii_image_src)
    
    # to be extra sure of not overwriting data:
    new_data = np.copy(image.get_data())
    hd = image.header

    # in case you want to remove nan: (DGK: I want scripts to fail if these give NAN so I don't remove)
    # new_data = np.nan_to_num(new_data) 

    array_sum = np.sum(new_data)
    array_has_nan_before = np.isnan(array_sum)

    # update data type:
    new_dtype = np.float32  # for example to cast to int8.
    new_data = new_data.astype(new_dtype)
    image.set_data_dtype(new_dtype)
    hd.set_data_dtype(new_data.dtype)
    
    array_sum = np.sum(new_data)
    array_has_nan_after = np.isnan(array_sum)

    if array_has_nan_before:
        print(f'{array_has_nan_before} had NANs before conversion')
    if array_has_nan_after:
        print(f'{array_has_nan_after} had NANs after conversion')

    # if nifty1
    if hd['sizeof_hdr'] == 348:
        new_image = nib.Nifti1Image(new_data, image.affine, header=hd)
    # if nifty2
    elif hd['sizeof_hdr'] == 540:
        new_image = nib.Nifti2Image(new_data, image.affine, header=hd)
    else:
        raise IOError('Input image header problem')

    nib.save(new_image, nii_image_dst)

def convert_nii_to_int8(nii_image_src,nii_image_dst):
    '''
    Purpose: Create a copy of nifty label file in int8 format.
    Parameters
        - nii_image_src: Nifti source file.
        - nii_image_dst: Nifti destination file
    '''
    # the code is adapted from https://stackoverflow.com/questions/44397617/change-data-type-in-numpy-and-nibabel
    image = nib.load(nii_image_src)
    
    # to be extra sure of not overwriting data:
    new_data = np.copy(image.get_data())
    hd = image.header

    # in case you want to remove nan: (DGK: I want scripts to fail if these give NAN so I don't remove)
    # new_data = np.nan_to_num(new_data) 

    array_sum = np.sum(new_data)
    array_has_nan_before = np.isnan(array_sum)

    # update data type:
    new_dtype = np.int8  # for example to cast to int8.
    new_data = new_data.astype(new_dtype)
    image.set_data_dtype(new_dtype)
    hd.set_data_dtype(new_data.dtype)
    
    array_sum = np.sum(new_data)
    array_has_nan_after = np.isnan(array_sum)

    if array_has_nan_before:
        print(f'{array_has_nan_before} had NANs before conversion')
    if array_has_nan_after:
        print(f'{array_has_nan_after} had NANs after conversion')

    # if nifty1
    if hd['sizeof_hdr'] == 348:
        new_image = nib.Nifti1Image(new_data, image.affine, header=hd)
    # if nifty2
    elif hd['sizeof_hdr'] == 540:
        new_image = nib.Nifti2Image(new_data, image.affine, header=hd)
    else:
        raise IOError('Input image header problem')

    nib.save(new_image, nii_image_dst)

def convert_pet_ct_to_4d_nifti(ct, pet, dst):
    '''
    Purpose: Collect two 3d nifti volumes in one 4d volume.
    The 4th dimension designates the channel (pet or ct).
    Inputs:
        - ct: absolute path to CT filename
        - pet: absolute path to PET filename
        - dst: absolute path to PET-CT filename
    
    '''
    #to_name = Path(f'data/{split_folder}/images/{ind}.nii.gz')
    #to_name.parent.mkdir(exist_ok=True, parents=True)
    PET = nib.load(pet)
    CT = nib.load(ct)
    PET_CT = np.stack([CT.get_fdata(),PET.get_fdata()],axis=3)
    merged = nib.Nifti1Image(PET_CT, PET.affine, PET.header)
    nib.save(merged, dst)

def convert_pet_ct_to_4d_nifti_channel_first(ct, pet, dst):
    '''
    Purpose: Collect two 3d nifti volumes in one 4d volume.
    The 4th dimension designates the channel (pet or ct).
    Inputs:
        - ct: absolute path to CT filename
        - pet: absolute path to PET filename
        - dst: absolute path to PET-CT filename
    '''
    #to_name = Path(f'data/{split_folder}/images/{ind}.nii.gz')
    #to_name.parent.mkdir(exist_ok=True, parents=True)
    PET = nib.load(pet)
    CT = nib.load(ct)
    PET_CT = np.stack([CT.get_fdata(),PET.get_fdata()],axis=0)
    merged = nib.Nifti1Image(PET_CT, PET.affine, PET.header)
    nib.save(merged, dst)

def convert_label_to_channel_first(label_src_file, dst_file):
    '''
    Some methods, for instance MONAI, uses 4D data with channels first.
    Purpose: Convert 3d data to 4d, where channel is on the first dimension of the nifty file.
    Inputs:
        - label_src_file: absolute path to label source file
        - dst_file: absolute path to the output label in 4d with dim first. 
    '''
    src_dat_nib_obj = nib.load(label_src_file)
    #src_dat = get_nii_image_to_numpy(label_src_file)
    dst_dat = np.expand_dims(src_dat_nib_obj.get_fdata(), axis = 0)
    dst_dat_nii = nib.Nifti1Image(dst_dat, src_dat_nib_obj.affine, src_dat_nib_obj.header)
    nib.save(dst_dat_nii, dst_file)