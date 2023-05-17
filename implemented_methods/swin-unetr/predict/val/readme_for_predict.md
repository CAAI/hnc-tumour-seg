### This is to descripe the order of things to predict data with swin unetr

1) run predict commands on gpu from command line (update this later)
2) use majority_vote.py in this folder to do majority voting
3) use resample_to_patient_space.py in order to get the data in the original size
4) use remove_tumor_outside_body_roi.py to remove things that for sure should not be there
5) use dice_haus on command line to get the metrics of the result

Other than this: 
Adapt plot_predicted_cases.py to have a look at the data. 