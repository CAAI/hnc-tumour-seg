'''
Purpose: Get output of 5 swin-unetr models and majority vote to get final result. 
'''

# import packages
from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.majority_vote import majority_vote
from MEDIcaTe.nii_resampling import *
#import torchio as tio
from multiprocessing import Pool

# path to predicted data
pred0 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/m0/test_fold0_val'
pred1 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/m1/test_fold0_val'
pred2 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/m2/test_fold0_val'
pred3 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/m3/test_fold0_val'
pred4 = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/m4/test_fold0_val'

# destination of majority voted result
mv_dest = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/output/majority_voted'

def majority_vote_swin_unetr(case):
    pred0_abspath = join(pred0,case)
    pred1_abspath = join(pred1,case)
    pred2_abspath = join(pred2,case)
    pred3_abspath = join(pred3,case)
    pred4_abspath = join(pred4,case)
    out_abs_fname = join(mv_dest,case)
    print(case)
    #print(pred0_abspath)
    #print(out_abs_fname)
    if not isfile(out_abs_fname):
        majority_vote(out_abs_fname,pred0_abspath,pred1_abspath,pred2_abspath,pred3_abspath,pred4_abspath)
    #print('not doing majority voting')
    

if __name__ == '__main__':
    data_inputs = listdir(pred0)
    pool = Pool()                         
    pool.map(majority_vote_swin_unetr, data_inputs)
    

