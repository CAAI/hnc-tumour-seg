
'''
Purpose: resampling nifty image files to output defined in mm.
'''

from .file_folder_ops import *
from .utilities import *
from nibabel.processing import resample_to_output
import nibabel as nib
import numpy as np
from os import system
import torchio as tio


def find_pix_dim(nifty_file):
    """
    Gets dimensions x, y and z of a voxel. unit is  millimeters
    """
    nifty = nib.load(nifty_file)
    pix_dim = nifty.header["pixdim"] #pixel dimension
    dim = nifty.header["dim"] 

    # get x- and y- dimensions
    max_indx = np.argmax(dim)
    pixdimX = pix_dim[max_indx]
    dim = np.delete(dim, max_indx)
    pix_dim = np.delete(pix_dim, max_indx)
    max_indy = np.argmax(dim)
    pixdimY = pix_dim[max_indy]

    # get z- dimension
    pixdimz = pix_dim[2]
    
    return [pixdimX, pixdimY, pixdimz]

def find_pix_dim_with_orientation(nifti_file):
    """
    Gets dimensions x, y and z of a voxel. unit is  millimeters
        Note: if image orientation is (L,A,F), affine[0,0] should 
        be a negative number. 
    """
    affine = get_affine(nifti_file)
    
    pixdimX = affine[0,0]
    pixdimY = affine[1,1]
    pixdimz = affine[2,2]
    
    return (pixdimX, pixdimY, pixdimz)

def resample_nii_to_voxel_size(input_path, voxel_size, output_path=None, order = 3, verbose = False):
    '''
    Resample image to a new size and save output

    Parameters:
        - input_path: path to nifty input image file ../../<filename.nii.gz>
        - output_path: path to which output FOLDER nifty image is saved
        - voxel_size: the output voxelsize in milimiters given as tuple (x,y,z)
        - order: order of spline used for interpolation. NOTE: Use order=0 for
        nearest-neighbour interpolation!
        - verbose: output prints

    If voxel_sizes matches input_path nifty image voxel size it will 
    save a copy of input nifty on destination.
    '''
    #defining full path and filename for the resampled/output nifty images 
    filename = basename(input_path)
    
    
    input_img = nib.load(input_path) #load .nii image
    
    # only resample if voxel_size is different from existing pix_dims
    pix_dims = find_pix_dim_with_orientation(input_path)
    if pix_dims != voxel_size:
    
    # generating the resampled/output nifty image
        if verbose:
            print(f'Resampling case {filename}')
        
        # note that this uses third order spline interpolation by default. Not OK for binary segments.
        output_img = resample_to_output(input_img, tuple(np.abs(voxel_size)), order = order)
        
        # flip the result to (L,A,S) if result orientation is changed to (R,A,S)
        if verbose:
            print(voxel_size[0])
        if np.negative(voxel_size[0]) > 0: 
            old_orientation = nib.orientations.aff2axcodes(output_img.affine)
            output_img = output_img.slicer[::-1]
            new_orientation = nib.orientations.aff2axcodes(output_img.affine)
            if verbose: 
                print(f'Orientation was changed from {old_orientation} to {new_orientation}')
    else:
        if verbose:
            print("Image voxelsize already as requested. Creating a copy to destination.")
        output_img = input_img
    
    if output_path !=None:
        output = join(output_path,filename) #full information for the output  
        nib.save(output_img, output) #saving the resampled image
    return output_img



   
def resample_binary(input_path_ref, input_path_flo, output_path, verbose = False):
    '''
    NOTE: This function is currently unused, as order = 0 in resample function seems to just as good for this!
    TODO: Determine if to be deleted or??
    Using nearest-neighbour interpolation for resampling binary in- and outputs.
    Using nifty_reg package reg_resample since unsure how this is done using Nibabel.

    Prerequisistes:
        Make sure you have installed the Niftyreg package. It containes the reg_resample function. 
    
    Note: before using this function make sure the the reference image already has the right dimensions!

    Parameters:
        - input_path_ref: path to image to be matched in voxel-size by the binary input image
        ../../<filename.nii.gz> (ref = reference image, the one to be matched)
        - input_path_flo: path to binary nifty input image 
        ../../<filename.nii.gz> (flo = floating image, the one to be resampled)
        - output_path: path to folder where output nifty image is saved
        - voxel_size: the output voxelsize in milimiters given as tuple (x,y,z)
        - verbose: output prints; makes the function verbose.
    '''
    # output filename is based on input
    output_fname = join(output_path, basename(input_path_flo))

    # define the command string
    cmd_str = f'reg_resample -ref {input_path_ref} -flo {input_path_flo} -res {output_fname} -NN'
    if verbose:
        print(cmd_str)
    system(cmd_str)

def check_affine_all_but_voxel_size_designators(affine1, affine2):
    '''
    Purpuse: Check if there are differences between two affines in any other position than:
        - affine [0,0]
        - affine [1,1]
        - affine [2,2]
    '''
    affine_equality_test = (affine1 == affine2)
    only_trues_exists = ((affine_equality_test[0,1])&
        (affine_equality_test[0,2])&
        (affine_equality_test[0,3])&
        (affine_equality_test[1,0])&
        (affine_equality_test[1,2])&
        (affine_equality_test[1,3])&
        (affine_equality_test[2,0])&
        (affine_equality_test[2,1])&
        (affine_equality_test[2,3])&
        (affine_equality_test[3,0])&
        (affine_equality_test[3,1])&
        (affine_equality_test[3,2])&
        (affine_equality_test[3,3]))
    if only_trues_exists:
        return True
    else:
        return False


def resample_back_to_patient_space(file_to_resample, container, outname=None,verbose=False):
    '''
    This script could be used for me resampling cases.
    Note: Many things can happen in the affine depending on the resampling methods used by 
    various frameworks. Hence it is necessary to manually check if resampling went well manually 
    before calculating result metrics!

    Purpose: resample a destination (e.g. predicted) file to the size of a source file.
    inputs: 
        - file_to_resample: abspath to the nifti file to be resampled
        - container: abspath to the nifti file container. dst will we resampled to the size of this
        - outname: abspath to the resampled nifti file.

    '''

    case = basename(file_to_resample)
    if verbose:
        print(f'Checking if {case} should resampled by comparing dimensions')
    dims_container = find_pix_dim_with_orientation(container)
    dims_file_to_resample = find_pix_dim_with_orientation(file_to_resample)
    lab_file_to_resample = tio.LabelMap(file_to_resample)
    if dims_container != dims_file_to_resample:
        if verbose:
            print(f'Note: doing resampling!!! {case}')
        lab_container = tio.LabelMap(container)
        #
        #  The following is an explicit check of a known bug of nibabel resample_to_output
        #  Will give warning if affine does not match on anything else than position [0,0][1,1][2,2] after running this
        #  If only change is in sign of affine position [0,3] the code will just change signs and proceed.          
        #
        if (lab_file_to_resample.affine[0,3] == -lab_container.affine[0,3]):
            if verbose:
                print('Note: The mismatch in affine was on qoffset_x. Predicted had opposite sign of original. This is a known resampling issue from using nibabel.resample_to_output and can be solved by simply changing sign on qoffset_x in the affine.')
                print('Note: now changing sign on affine[0,3] (qoffset_x).')
            new_affine = lab_file_to_resample.affine
            new_affine[0,3] = new_affine[0,3]*(-1)
            # check if there is still an unexpected mismatch in affines after this change
            lab_file_to_resample = tio.LabelMap(tensor=lab_file_to_resample.data, affine = new_affine)
        affine_check = check_affine_all_but_voxel_size_designators(lab_container.affine, lab_file_to_resample.affine)
        if not affine_check:
            if verbose:
                print(f'Warning: There is still an unexpected mismatch in affine on this case. DO DEBUGGING ON THIS CASE. {case}')
    
        resample_transform = tio.Resample(lab_container) #pre_affine_name='to_clin', image_interpolation='nearest'
        output = resample_transform(lab_file_to_resample)
    else:
        print('Not resampling since predicted dims equal patient space dims. Just making a copy for completeness at destination path.')
        output = lab_file_to_resample

    if not outname==None:
        output.save(outname)
        if verbose:
            print(f'saved resampled file {outname}')
    
    output_numpy = output.numpy()

    return np.squeeze(output)


def resample_label_dst_like_src(dst, src, outname=None):
    '''
    Legacy function. If this is used, it is necessary to manually check that that 
    the final resampling was ok!

    WORKS for SWIN-UNETR so added, but otherwise don't use this one.


    resample a destination (e.g. predicted) file to the size of a source file.
    inputs: 
        - dst: abspath to the nifti file to be resampled
        - src: abspath to the nifti file container. dst will we resampled to the size of this
        - outname: abspath to the resampled nifti file.
    '''

    case = basename(dst)
    print(f'doing resampling of case {case}')
    
    lab_clin = tio.LabelMap(src)
    #affine_matrix = lab_clin.affine
    lab_pred = tio.LabelMap(dst) #, to_clin=affine_matrix 
    expected_affine_equality_test = np.array([  [ True,  True,  True,  True],
                                                [ True,  True,  True,  True],
                                                [ True,  True, False,  True],
                                                [ True,  True,  True,  True]])
    affine_equality_test = (lab_clin.affine == lab_pred.affine)
    if False in (expected_affine_equality_test == affine_equality_test):
        print(f'Note: unexpected mismatch in affines!!! {case}')
        new_affine = lab_pred.affine
        if (lab_pred.affine[0,3] == -lab_clin.affine[0,3]):
            print('Note: The mismatch in affine was on qoffset_x. Predicted had opposite sign of original. This is a known resampling issue from using nibabel.resample_to_output and can be solved by simply changing sign on qoffset_x in the affine.')
            print('Note: now changing sign on affine[0,3] (qoffset_x).')
            new_affine[0,3] = new_affine[0,3]*(-1)
            #lab_pred.affine[0,3] = -lab_pred.affine[0,3]
            # check if there is still an unexpected mismatch in affines after this change
            lab_pred = tio.LabelMap(tensor=lab_pred.data, affine = new_affine)
        affine_equality_test = (lab_clin.affine == new_affine)
        if False in (expected_affine_equality_test == affine_equality_test):
            print(f'Warning: There is still an unexpected mismatch in affine on this case. DO DEBUGGING ON THIS CASE. {case}')
    
    resample_transform = tio.Resample(lab_clin)#pre_affine_name='to_clin', image_interpolation='nearest'
    resampled = resample_transform(lab_pred)

    if not outname==None:
        resampled.save(outname)
        print(f'saved resampled file {outname}')
    
    resampled_numpy = resampled.numpy()

    return np.squeeze(resampled_numpy)
