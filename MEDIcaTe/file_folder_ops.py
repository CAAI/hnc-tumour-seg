'''
This is copied from https://github.com/MIC-DKFZ/batchgenerators/blob/master/batchgenerators/utilities/file_and_folder_operations.py
The script has been very useful several times, so I am adding a copy of it here to be used in this package.
David Kovacs Petersen 28-03-2022

In script after installing MEDIcaTe simply run
from file_folder_ops import  * 
And the functions here should be available to you. 

28-03-2022 David Gergely Kovacs Petersen. 
'''
# Copyright 2021 Division of Medical Image Computing, German Cancer Research Center (DKFZ)
# and Applied Computer Vision Lab, Helmholtz Imaging Platform
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pickle
import json
from typing import List
import os
from os.path import basename, join
import pandas as pd


def subdirs(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) -> List[str]:
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


def subfiles(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True) -> List[str]:
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


def nifti_files(folder: str, join: bool = True, sort: bool = True) -> List[str]:
    return subfiles(folder, join=join, sort=sort, suffix='.nii.gz')


def maybe_mkdir_p(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)


def load_pickle(file: str, mode: str = 'rb'):
    with open(file, mode) as f:
        a = pickle.load(f)
    return a


def write_pickle(obj, file: str, mode: str = 'wb') -> None:
    with open(file, mode) as f:
        pickle.dump(obj, f)


def load_json(file: str):
    with open(file, 'r') as f:
        a = json.load(f)
    return a


def save_json(obj, file: str, indent: int = 4, sort_keys: bool = True) -> None:
    with open(file, 'w') as f:
        json.dump(obj, f, sort_keys=sort_keys, indent=indent)


def pardir(path: str):
    return os.path.join(path, os.pardir)


def split_path(path: str) -> List[str]:
    """
    splits at each separator. This is different from os.path.split which only splits at last separator
    """
    return path.split(os.sep)


def nnunet_summary_json_to_pd(json_path, output_path=None):
    '''
    PURPOSE: generate dataframe with metrics stored in .json file. If output_path is not None then a csv file is created. 
    
    FUNCTION:
    nnunet_summary_json_to_pd(json_path, output_path):

    INPUT:
        json_path:      str             - full path to json file.
        output_path:    str, optional   - output directory. Note exclude csv name, just directory
    OUTPUT:
        df:             panda dataframe - dataframe with metrics and patient name.
    '''
    f = open(json_path) #get json file
    summary=json.load(f)
    
    metrics=list(['idx','Patient'])
    for n,i in enumerate(summary['results']['all']):
        
        # get metrics
        for j in i['1']:
            if n==0:
                metrics.append(j)
                df=pd.DataFrame(columns=metrics) #make dataframe


        patient=os.path.basename(i['reference']).replace('.nii.gz','')
        df = pd.concat([df,pd.DataFrame(({
            'idx':                          [n],
            'Patient':                      patient,
            'Accuracy':                     i['1']['Accuracy'],
            'Dice':                         i['1']['Dice'],
            'False Discovery Rate':         i['1']['False Discovery Rate'],
            'False Negative Rate':          i['1']['False Negative Rate'],
            'False Omission Rate':          i['1']['False Omission Rate'],
            'False Positive Rate':          i['1']['False Positive Rate'],
            'Jaccard':                      i['1']['Jaccard'],
            'Negative Predictive Value':    i['1']['Negative Predictive Value'],
            'Precision':                    i['1']['Precision'],
            'Recall':                       i['1']['Recall'],
            'Total Positives Reference':    i['1']['Total Positives Reference'],
            'Total Positives Test':         i['1']['Total Positives Test'],
            'True Negative Rate':           i['1']['True Negative Rate']}))])
    if output_path is not None:
        df.to_csv(os.path.join(output_path,'nnunet_summary.csv'),index=False)            
        
    return df


# I'm tired of typing these out
join = os.path.join
isdir = os.path.isdir
isfile = os.path.isfile
listdir = os.listdir
makedirs = maybe_mkdir_p
os_split_path = os.path.split
basename = os.path.basename
dirname = os.path.dirname

# I am tired of confusing those
subfolders = subdirs
save_pickle = write_pickle
write_json = save_json