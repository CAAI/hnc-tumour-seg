# commands can be run from folder ~/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning
# 
# NOTE: File cannot be run from MEDIcaTe/implemented_methods/InnerEye/predict/test/ it needs to be moved to whereever you installed InnerEye Deep Learning!


# screen -S/r inner-eye
# if needed: ssh kovacs@10.49.144.33
# export CUDA_VISIBLE_DEVICES=0
# conda activate InnerEye

# cd ~/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning
# then run:
# export PYTHONPATH=`pwd`

#prediction on valset for model1 was done.
time ( python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-13T092536Z_HNC_tumor_dgk_HeadAndNeckBase/checkpoints/last.ckpt --inference_on_test_set=True ) &> InnerEyeLocal/ML/configs/segmentation/test_timing/model1_output_time_inner_eye.txt
time ( python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase_f1 --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-10T162204Z_HNC_tumor_dgk_HeadAndNeckBase_f1/checkpoints/last.ckpt --inference_on_test_set=True ) &> InnerEyeLocal/ML/configs/segmentation/test_timing/model2_output_time_inner_eye.txt
time ( python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase_f2 --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-10T163327Z_HNC_tumor_dgk_HeadAndNeckBase_f2/checkpoints/last.ckpt --inference_on_test_set=True ) &> InnerEyeLocal/ML/configs/segmentation/test_timing/model3_output_time_inner_eye.txt
time ( python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase_f3 --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-13T092608Z_HNC_tumor_dgk_HeadAndNeckBase_f3/checkpoints/last.ckpt --inference_on_test_set=True ) &> InnerEyeLocal/ML/configs/segmentation/test_timing/model4_output_time_inner_eye.txt
time ( python InnerEyeLocal/ML/runner.py --model=HNC_tumor_dgk_HeadAndNeckBase_f4 --no-train --local_weights_path=/homes/kovacs/project_scripts/hnc_segmentation/inner-eye-ms-oktay/InnerEye-DeepLearning/outputs/2022-06-15T071930Z_HNC_tumor_dgk_HeadAndNeckBase_f4/checkpoints/last.ckpt --inference_on_test_set=True ) &> InnerEyeLocal/ML/configs/segmentation/test_timing/model5_output_time_inner_eye.txt
