'''
Purpose: Create a mapping from InnerEye-ID's to nnUNet-ID's.

This is used to name the files with nnUNet ID's in the majority voting scripts.

Later this is useful when resampling to original patient space and computing method metrics.
'''

import time 
start = time.time()

import pandas as pd
import numpy as np
from MEDIcaTe.file_folder_ops import *

path_to_data_csv = '/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/dataset.csv'
dat = pd.read_csv(path_to_data_csv)
dat_labels = dat.loc[dat['channel']=='tumor']
dat_labels['filePath'] = dat_labels['filePath'].apply(lambda x: basename(x))

inner_eye_id = dat_labels['subject'].to_list()
nnUNet_id = dat_labels['filePath'].to_list()

dict_innerEye2nnUNet = dict(zip(inner_eye_id,nnUNet_id))

write_pickle(dict_innerEye2nnUNet,join(dirname(path_to_data_csv),'dict_innerEye2nnUNet.pkl'))

end = time.time()
total_time = end-start
print(f'Total time to generate mapping = {np.round(total_time,2)} sec.')