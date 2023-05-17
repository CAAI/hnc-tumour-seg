from file_folder_ops import *
from roi_generators import generate_rois_dm_pt
from fig_images_labels import vizualization

if __name__ == '__main__':
    #a = load_pickle('/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_preprocessed/Task500_HNC01/dataset_properties.pkl')
    input_folder_images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
    input_folder_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
    output_folder_images = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train'

    # load case
    # resample Need to resample first because the ROI should be in the resampled space
    # get mean and std of each case
    # get mean og means and mean og std's
    # normalize images

    #ct_image_nifty = join(input_folder_images, 'HNC01_000_0000.nii.gz')
    #pt_image_nifty = join(input_folder_images, 'HNC01_000_0001.nii.gz')
    #destination_path = output_folder_images
    #generate_rois_dm_pt(pt_image_nifty, destination_path)



    '''
    vizualization(final_path = destination_path,
                ct_path = ct_image_nifty,
                pet_path = pt_image_nifty,
                label1_path = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train/HNC01_000_0001_roi.nii.gz',
                label2_path = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train/HNC01_000_0001_roi.nii.gz',
                slice_range = list(range(70, 80)))
    '''
