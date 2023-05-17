'''
Purpose: Get output of 5 inner-eye models and majority vote to get final result. 
'''

from MEDIcaTe.file_folder_ops import *
from MEDIcaTe.majority_vote import majority_vote
from MEDIcaTe.nii_resampling import *
#import torchio as tio
from multiprocessing import Pool

# path to predicted data
pred0 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m0/predictions_nnunet_id_patient_space'
pred1 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m1_f0/predictions_nnunet_id_patient_space'
pred2 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m2_f0/predictions_nnunet_id_patient_space'
pred3 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m3_f0/predictions_nnunet_id_patient_space'
pred4 = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/testSessionDm_valSet_m4_f0/predictions_nnunet_id_patient_space'

# destination of majority voted result
mv_dest = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0'

def majority_vote_inner_eye(case):
    if isdir(pred0):
        pred0_abspath = join(pred0,case)
        pred1_abspath = join(pred1,case)
        pred2_abspath = join(pred2,case)
        pred3_abspath = join(pred3,case)
        pred4_abspath = join(pred4,case)
        out_abs_fname = join(mv_dest,case)
        print(case)
        #print(pred0_abspath)
        #print(out_abs_fname)
        if (isfile(pred0_abspath) & isfile(pred1_abspath) & isfile(pred2_abspath) & isfile(pred3_abspath) & isfile(pred4_abspath)):
            if not isfile(out_abs_fname):
                #print('WILL DO MAJORITY VOTIG HERE')
                majority_vote(out_abs_fname,pred0_abspath,pred1_abspath,pred2_abspath,pred3_abspath,pred4_abspath)
        else:
            print(f'appears there was a missing prediction on {case}')

if __name__ == '__main__':
    data_inputs = listdir(pred0)
    pool = Pool(processes=22)                         
    pool.map(majority_vote_inner_eye, data_inputs)
    