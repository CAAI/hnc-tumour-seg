# How to predit data with trained InnerEye models

## Use models to predict

1) Preprocess the test data as was done for inner-eye training (´predict_test_set_inner_eye_1preprocess.py´)

2) Generate the dataset.csv file for the testset (dataset_test196.csv) (´predict_test_set_inner_eye_2generate_dataset_csv.py´)

3) Modify and run /homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/InnerEyeLocal/ML/configs/segmentation/HNC_tumor_dgk_HeadAndNeckBase.py [...f1-f4] to run on test data.

4) Run using the following lines: 
python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-13T092536Z_HNC_tumor_dgk_HeadAndNeckBase/checkpoints/last.ckpt --inference_on_test_set=True


## Do majority voting between 5 models

Purpose: Do majority voting betwen 5 inner-eye models.

1) load predictions from folder
2) majority vote
3) plots results
4) do metrics with dice_haus

