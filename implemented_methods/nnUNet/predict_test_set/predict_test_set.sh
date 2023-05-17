# purpose: predict nnUNet final model on test dataset HNC02 with 196 patients.
export FOLDER_WITH_TEST_CASES=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images
export OUTPUT_FOLDER_MODEL1=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_m1
export OUTPUT_FOLDER_MODEL2=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_m2
export OUTPUT_FOLDER=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/nnunet/labels_nn_unet_ensemble_final
export POSTPROCESS_FILE=/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_trained_models/nnUNet/ensembles/Task500_HNC01/ensemble_3d_lowres__nnUNetTrainerV2__nnUNetPlansv2.1--3d_cascade_fullres__nnUNetTrainerV2CascadeFullRes__nnUNetPlansv2.1/postprocessing.json

time ( nnUNet_predict -i $FOLDER_WITH_TEST_CASES -o $OUTPUT_FOLDER_MODEL1 -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_lowres -p nnUNetPlansv2.1 -t Task500_HNC01 -z ) &> model1_output_time.txt
time ( nnUNet_predict -i $FOLDER_WITH_TEST_CASES -o $OUTPUT_FOLDER_MODEL2 -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_cascade_fullres -p nnUNetPlansv2.1 -t Task500_HNC01 -z ) &> model2_output_time.txt
time ( nnUNet_ensemble -f $OUTPUT_FOLDER_MODEL1 $OUTPUT_FOLDER_MODEL2 -o $OUTPUT_FOLDER -pp $POSTPROCESS_FILE ) &> ensemble_output_time.txt
