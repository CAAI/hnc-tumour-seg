'''
Purpose: Running evaluation of SWIN-UNETR method trained model

python test.py --json_list=<json-path> --data_dir=<data-path> --feature_size=<feature-size>\
--infer_overlap=0.5 --pretrained_model_name=<model-name>

/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/dataset_1.json
feature_size=48
pretrained_model_name=<model-name>

Note: This only creates the string for prediction.
The string must be copied to and run from the Swin-UNETR folder, i.e. from the folder where test.py is located.
In my case: /homes/kovacs/project_scripts/hnc_segmentation/swin-unetr/research-contributions/SwinUNETR/BTCV

'''

if __name__ == '__main__':
    # doing inference on one dataset. Don't know yet exactly which cases this will choose....
    abspath_to_json_list = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01/dataset_1.json'
    abspath_to_datadir = '/homes/kovacs/project_data/hnc-auto-contouring/MONAI/Task500_HNC01'
    feature_size = 48
    pretrained_model_name = 'best_metric_model.pth' # file is located at /homes/kovacs/project_scripts/hnc_segmentation/swin-unetr/research-contributions/SwinUNETR/BTCV/pretrained_models/
    training_str =  f'python test.py --json_list={abspath_to_json_list} --data_dir={abspath_to_datadir} --feature_size={feature_size} --infer_overlap=0.5 --pretrained_model_name={pretrained_model_name}'
    print(training_str)