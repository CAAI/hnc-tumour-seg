'''

### Generate dataset.json
We can now generate a json file for the data set. It is generated based on the example shared by the swin-unetr guidelines at https://github.com/Project-MONAI/research-contributions/tree/main/SwinUNETR/BTCV, https://drive.google.com/file/d/1t4fIQQkONv7ArTSZe4Nucwkk1KfdUDvW/view.

We will not add test-cases as this is done separately.

Before you run this, make sure that datafolders are populated (by running predict_test_set_swin-unetr_1preprocess.py)

'''

import time 
start = time.time()

import json
from MEDIcaTe.file_folder_ops import *
import numpy as np

if __name__=='__main__':
    dataset_json_dst_folder = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC02/imagesTs'
    # data_split_pickle = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_preprocessed/Task500_HNC01/splits_final.pkl'

    # Data to be written
    f = open(join(dirname(dirname(dataset_json_dst_folder)),'Task500_HNC01','dataset.json')) #get json file
    dataset=json.load(f)
    
    test_cases = []
    for case in listdir(join(dataset_json_dst_folder,'data_as_4d_channel_first')):
        dict_entry = {'image': f'./data_as_4d_channel_first/{case}',
                      'label': f'../labelsTs/data_as_4d_channel_first/{case}'}
        test_cases.append(dict_entry)

    dataset['test'] = test_cases
    dataset['training'] = []
    dataset['description'] = ['196 test HNC test cases.']
    dataset['licence'] = ['Property of David Gergely Kovacs, Rigshospitalet, 2022-AUG-10']
    dataset['name'] = ["Task500_HNC02"]
    dataset['numTest'] = 196
    dataset['numTraining'] = 0

    # Serializing json 
    json_object = json.dumps(dataset, indent = 4)
    
    # Writing json file
    with open(join(dataset_json_dst_folder,f"dataset_test196.json"), "w") as outfile:
        outfile.write(json_object)
    
    end = time.time()
    total_time = end-start
    print(f'Total time to generate dataset json file = {np.round(total_time,2)} sec.')