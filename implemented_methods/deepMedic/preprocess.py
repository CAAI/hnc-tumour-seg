from file_folder_ops import *
from nii_resampling import generate_rois_dm
from fig_images_labels import vizualization

#a = load_pickle('/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_preprocessed/Task500_HNC01/dataset_properties.pkl')
input_folder_images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
input_folder_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
output_folder_images = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train'

ct_image_nifty = join(input_folder_images, 'HNC01_000_0000.nii.gz')
destination_path = output_folder_images
#generate_rois_dm(ct_image_nifty, destination_path)

vizualization(final_path = destination_path,
              ct_path = ct_image_nifty,
              label1_path = '/homes/kovacs/project_data/hnc-auto-contouring/deepMedic/data_nifty/d_train/HNC01_000_0000_roi.nii.gz')
