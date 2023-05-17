from MEDIcaTe.remove_small_volumes import remove_small_vols
from MEDIcaTe.file_folder_ops import *
from multiprocessing import Pool

pred_path = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0'
output_path = '/media/bizon/data2tb/deep_medic/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/output/output_HNC_valSets/predictions/majority_voted_valSet_f0_no_small_vols'

def remove_small_vols_swin(case):
    ext = os.path.splitext(case)[1]
    if ext == '.gz':
        path_pred_case = join(pred_path,case)
        output_path_case = join(output_path,case)
        remove_small_vols(path_pred_case, 15, output_path_case)

if __name__ == '__main__':
    data_inputs = listdir(pred_path)
    pool = Pool()
    pool.map(remove_small_vols_swin, data_inputs)