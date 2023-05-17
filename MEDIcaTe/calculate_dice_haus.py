'''
Purpose: calculate dice score and hausdorff distance, thus enable comparison between medical doctor(md) and reference doctor(ref) tumor labels.    

To enable use of the following script, the reader must overwrite the paths defined in the scripts, this includes:

md_path: path to folder containing md tumor labels
ref_path_ path to folder containing ref tumor labels

'''

import os
import numpy as np
import pandas as pd
import SimpleITK as sitk
import argparse
from scipy.spatial import cKDTree
from os.path import join, isdir, isfile
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.utilities import *
from MEDIcaTe.nii_resampling import *
from multiprocessing import Pool
from functools import partial
import torchio as tio

def dice_v2(image0, image1):
    ''' 
    Code copied from 
    https://github.com/voreille/hecktor/blob/master/src/evaluation/scores.py
    '''
    return 2 * np.sum(np.logical_and(
        image0, image1)) / (np.sum(image0) + np.sum(image1))


def dice_from_nifti(image0, image1):
    ''' 
    Purpose: Calculate DICE between two niftis when input is nifti (nii.gz)

    Code copied from 
    https://github.com/voreille/hecktor/blob/master/src/evaluation/scores.py
    '''

    l1_image=sitk.ReadImage(image0)
    l2_image=sitk.ReadImage(image1)
            
    #convert the image into array of numbers
    l1_array = sitk.GetArrayFromImage(l1_image)
    l2_array = sitk.GetArrayFromImage(l2_image)

    return 2 * np.sum(np.logical_and(
        l1_array, l2_array)) / (np.sum(l1_array) + np.sum(l2_array))

def hausdorff_distance_v2(image0, image1):
    '''
    Code copied from 
    https://github.com/voreille/hecktor/blob/master/src/evaluation/scores.py
    '''
    a_points = np.transpose(np.nonzero(image0))
    b_points = np.transpose(np.nonzero(image1))

    # Handle empty sets properly:
    # - if both sets are empty, return zero
    # - if only one set is empty, return infinity
    if len(a_points) == 0:
        return 0 if len(b_points) == 0 else np.inf
    elif len(b_points) == 0:
        return np.inf

    return max(max(cKDTree(a_points).query(b_points, k=1)[0]),
               max(cKDTree(b_points).query(a_points, k=1)[0]))


def hausdorff_distance_with_resampling(lab1_nii, lab2_nii):
    '''
    Code copied from 
    https://github.com/voreille/hecktor/blob/master/src/evaluation/scores.py

    DGK 13-dep-2022: I added a resampling step of resampling to 1x1x1mm.
    This ensures that the return value is a physical distance in mm.

    Input should be binary nifti files. 

    TODO: in case lab1 and lab2 include a different number of slices after resampling to 1x1x1mm, need to resample lab1 like lab2 first.
    '''

    transform = tio.Resample(1)
    lab1 = tio.LabelMap(lab1_nii)
    # handle special case of HNC0176 where there is an error in the affine matrix in the image label. 
    if 'HNC02_176.nii.gz' in lab1_nii:
        lab1 = tio.LabelMap('/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/labels/labels_clinical_errors_removed/HNC02_176_corrected.nii.gz')
    lab2 = tio.LabelMap(lab2_nii)
    lab1_transformed = transform(lab1)
    lab2_transformed = transform(lab2)
    lab1_t_np = np.squeeze(lab1_transformed.numpy())
    lab2_t_np = np.squeeze(lab2_transformed.numpy())
    
    if lab1_t_np.shape == lab2_t_np.shape:
        a_points = np.transpose(np.nonzero(lab1_t_np))
        b_points = np.transpose(np.nonzero(lab2_t_np))

        # Handle empty sets properly:
        # - if both sets are empty, return zero
        # - if only one set is empty, return infinity
        if len(a_points) == 0:
            return 0 if len(b_points) == 0 else np.inf
        elif len(b_points) == 0:
            return np.inf

        return max(max(cKDTree(a_points).query(b_points, k=1)[0]),
                max(cKDTree(b_points).query(a_points, k=1)[0]))
    else:
        return 'Check manually. Shapes not equal.'

def hausdorff_distance_from_nifti(image0, image1):
    '''
    Purpose: Calculate HD between two niftis when input is nifti (nii.gz)
    Code copied from 
    https://github.com/voreille/hecktor/blob/master/src/evaluation/scores.py
    '''
    
    l1_image=sitk.ReadImage(image0)
    l2_image=sitk.ReadImage(image1)
            
    #convert the image into array of numbers
    l1_array = sitk.GetArrayFromImage(l1_image)
    l2_array = sitk.GetArrayFromImage(l2_image)
    
    a_points = np.transpose(np.nonzero(l1_array))
    b_points = np.transpose(np.nonzero(l2_array))

    # Handle empty sets properly:
    # - if both sets are empty, return zero
    # - if only one set is empty, return infinity
    if len(a_points) == 0:
        return 0 if len(b_points) == 0 else np.inf
    elif len(b_points) == 0:
        return np.inf

    return max(max(cKDTree(a_points).query(b_points, k=1)[0]),
               max(cKDTree(b_points).query(a_points, k=1)[0]))

def check_match(two_column_list):
    '''
    This function takes a two column list as input. 
    The function returns True if id of the two files in each row matches. 
    Otherwise function returns False
    '''
    for e in two_column_list: 
        name_md= os.path.basename(e[0])
        name_ref=os.path.basename(e[1])
        
        name_md=name_md.replace('_md', '')
        name_ref=name_ref.replace('_ref', '')

        if name_md==name_ref:
            return True
        else:
            return False

def resample_if_not_same_pixdim(lab1, lab2):
    '''
    Resample lab 1 to size of lab 2 if not same size.
    Here the resampled lab1 will overwrite the original.
    If pixdims are good, this just loads lab1 to numpy and returns it.
    '''
    if not find_pix_dim(lab1) == find_pix_dim(lab2):
        return resample_label_dst_like_src(lab1, lab2)
    else:
        return get_nii_image_to_numpy(lab1)

def folder_calc(duplicates,path_l1, path_l2,verbose):
    if verbose: 
        print(f'-------------- Calculating case {duplicates} --------------')
    #generate the images of the two contours  
    label1_abspath=join(path_l1,duplicates)
    label2_abspath=join(path_l2,duplicates)

    # resample 1 to 2 if not same size
    label1 = resample_if_not_same_pixdim(label1_abspath, label2_abspath)
    label2 = get_nii_image_to_numpy(label2_abspath)
    
    # calculate dice and hausdorf between label 1 and 2
    dice_coeff=round(dice(label1,label2), 4)
    haus_coeff=round(hausdorff_distance(label1, label2), 4)

    #generate return variable.
    result=[duplicates,dice_coeff,haus_coeff]

    return result


def run_for_folder(in_path1,in_path2, out_path,processes,verbose):
    
    #make list with full path to all nifty files with tumor labels made by md
    l1_path_list = listdir(in_path1)
    l2_path_list = listdir(in_path2)
    l1_and_l2 = l1_path_list+l2_path_list
    duplicates = [x for n, x in enumerate(l1_and_l2) if x in l1_and_l2[:n]]
    if verbose:
        print(f'Calculating Dice and Hausdorff for {len(duplicates)} cases...')
    if processes is not None:
        if type(processes) is int:
            pool = Pool(processes)
        else:
            raise Exception("argument processes must be of type int.")
    else:
        pool = Pool()
    result_list=pool.map(partial(folder_calc, path_l1=in_path1,path_l2=in_path2,verbose=verbose), duplicates)
    result_list.sort()
    result_list=[['Label','Dice Score','Hausdorff distance']]+result_list
    


    results_df = pd.DataFrame(result_list[1:],columns=result_list[0]).set_index('Label')
    
    # savinf dataframe to csv-file
    if out_path is not None: 
        #save CSV
        full_out_path= os.path.join(out_path, 'summary_MEDIcaTe.csv')
        results_df.to_csv(full_out_path)
    # elif out_abs_path is not None:
    #     full_out_path= os.path.join(out_abs_path)
    #     results_df.to_csv(full_out_path)
    

def run_for_file(in_path1, in_path2):
    '''
    Only works if inputs are files.
    '''
    dice = round(dice_from_nifti(in_path1, in_path2), 4)
    haus=round(hausdorff_distance_from_nifti(in_path1, in_path2), 4)

    return dice, haus

def run_for_folder_or_file(in_path1, in_path2,out_path,processes,verbose):
        # check whether to run for folder or for files 
    if os.path.isfile(in_path1) & os.path.isfile(in_path2):
        dice, haus = run_for_file(in_path1, in_path2)
        print(f'{basename(in_path1)} dice = {dice}')
        print(f'{basename(in_path1)} haus = {haus}')
    elif os.path.isdir(in_path1) & os.path.isdir(in_path2):
        run_for_folder(in_path1, in_path2, out_path=out_path,processes=processes,verbose=verbose)

    else:
        raise Exception("Either both inputs need to be folder or both need to be file. Seems this is not the case.")
        # run on entire folder.


def calculate_dice_haus(in_path1,in_path2,out_path=None,processes=None,verbose=False):
    '''
    PURPOSE: Calculate dice and hausdorff metrics for input.
    FUNCTION: calculate_dice_haus(in_path1,in_path2,out_path,processes=None)
    INPUTS:
        - in_path1, in_path2:  str                -  input nifti files or folders containing nifti. 
                                                     if folders, it will get files with 'nii.gz' ending and compare file names that match between folders
        - out_path:            str, (optional)    -  default is None. If provided it will save the results to the provided folder. 
        - processes:           int, (optional)    -  if nifti folder is given as input, all files in folder is processed using multiprocess, 
                                                     in this context number processes to be used can be specified.
    OUTPUT: CSV. file stored in out_path
    '''
    run_for_folder_or_file(in_path1,in_path2,out_path,processes,verbose)


# Define parser to enable command line function calls
def main():
    '''
    Entrypoint: dice_haus command
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument( 'in_path1',    type=str, help='Please input path for label 1')
    parser.add_argument( 'in_path2',    type=str, help='Please input path for label 2')
    parser.add_argument( '-out_path',   type=str,default=None, help='Please define output path')
    parser.add_argument( '-processes',  type=int,default=None, help='Please define number of processes to be used if in_path1 and in_path2 is given as folders and not files.')
    args = parser.parse_args()

    calculate_dice_haus(args.in_path1, args.in_path2, args.out_path, args.processes)


if __name__ == '__main__':

    in_path1 = '/home/fmik/data/t_l64_doctors/t_l64/labels/md_test/' #path to folder containing medical doctor(md) tumor label
    in_path2 = '/home/fmik/data/t_l64_doctors/t_l64/labels/ref_test/' #path to folder containing reference(ref) doctor tumor label
    out_path='/home/fmik/data/scores/'
    p=None#3

    calculate_dice_haus(in_path1,in_path2,out_path=out_path,processes=p,verbose=False)

    
    