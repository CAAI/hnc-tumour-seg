# This file is in the workings. just started it. Jan 24. 2025.

# How to use deep learning model available at https://rigshospitalet-tumour-segmentation.regionh.dk/

This files explains how I use my trained model. You can use this for inspiration on how to run on your own data.

# Preprocesseing
There is a minimal but necessary preprocessing necessary.

The model is designed to work on the first 35 of the body measured from the apex of the head, which is enough to include the full head and neck region.

# Install nnUNet
Install nnUNet V1 in your environment. Follow the instructions here: https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1

# Running the model 
Download the model from https://rigshospitalet-tumour-segmentation.regionh.dk/. Instruction are on the website.
Unzip the model file to your destination of choice. 
In terminal: `unzip Task500_HNC01_dgk_model.zip`.
Your folder should now be inflated with 5 folders with a bunch of trained models and weights: 2d, 3d_cascade_fullres, 3d_fullres, 3d_lowres and ensembles.

My final model is an ensemble model. I make a .sh-file with the following commands 

`time ( nnUNet_predict -i $FOLDER_WITH_TEST_CASES -o $OUTPUT_FOLDER_MODEL1 -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_lowres -p nnUNetPlansv2.1 -t Task500_HNC01 -z ) &> model1_output_time.txt` 

`time ( nnUNet_predict -i $FOLDER_WITH_TEST_CASES -o $OUTPUT_FOLDER_MODEL2 -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_cascade_fullres -p nnUNetPlansv2.1 -t Task500_HNC01 -z ) &> model2_output_time.txt`

`time ( nnUNet_ensemble -f $OUTPUT_FOLDER_MODEL1 $OUTPUT_FOLDER_MODEL2 -o $OUTPUT_FOLDER -pp $POSTPROCESS_FILE --npz) &> ensemble_output_time_npz.txt`

You don't have to time it with `time`, but I prefer to do that. 
See how my .sh file looks here. (TODO: Add file and hyperlink)



