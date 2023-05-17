# purpose: predict tureckova's AG-NN-VNET final model on test dataset HNC02 with 196 patients.
# The winning model was the lowres vnet.
# 
# Before running do:
# conda activate tureckova
#
# place file at this path:
# cd ~/project_scripts/hncQ_segmentation/tureckova_vnet/Abdomen-CT-Image-Segmentation/nnunet
# 
# run using:
# ./predict_test_set.sh
#
# see also: https://github.com/tureckova/Abdomen-CT-Image-Segmentation
#
# for time change INPUT_FOLDER and to the following:
# export INPUT_FOLDER=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_30_cases_for_timing_test196

export INPUT_FOLDER=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/images_1_case_for_test_of_test
export OUTPUT_FOLDER=/homes/kovacs/project_data/hnc-auto-contouring/hnc_rigs_all/data_nifty/t_r196/predictions/tureckova/vnet1_lowres_timed
export TIMING_FILE_OUTPUT=/homes/kovacs/project_scripts/hnc_segmentation/MEDIcaTe/implemented_methods/tureckova/predict_test_set/tureckova_output_time.txt

time ( python inference/predict_simple.py -i $INPUT_FOLDER -o $OUTPUT_FOLDER -t Task500_HNC01 -tr nnUNetTrainer -m 3d_lowres ) &> $TIMING_FILE_OUTPUT