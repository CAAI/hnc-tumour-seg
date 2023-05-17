# Prediction on independent test sets for Deep Medic model

Purpose: Describe how to use trained deepMedic models to predict on an independent test set. 
Requirements: Data must be nifti in nii.gz format.

1. Preprocess
2. Predict
3. Majority vote
4. Resample to patient space

## 1. Preprocessing can be done from whereever the MEDIcaTe package is installed. 
1. Use the script "test_set_deep_medic_1preprocess.py". 
2. Generate config files using test_set_deep_medic_2generate_config_files.py
3. Create 5 test config files: testConfig_HNC_r196_m0.cfg for m0 to m4. Fastest to do manually.
4. Create 'test_hnc_deep_medic.sh' file with commands to run test: deepMedicRun -model ./modelConfig_HNC_f0.cfg -test ../test/testConfig_HNC_r196_m0.cfg -load ../../output/output_HNC_f0/saved_models/trainSessionHNC0/deepMedicHNC_f0.trainSessionHNC0.final.2022-05-04.18.29.22.643919.model.ckpt -dev cuda
See also https://github.com/deepmedic/deepmedic, section: 3.3 Testing.
5. Place the .sh file in folder with model config files, i.e. ../deepMedic/config_files/model

## 2. Prediction needs to be done locally on a local nvme drive, which can be mounted to a docker container. 
In terminal: 
1. screen -S deep_medic_predict or screen -r deep_medic_predict 
2. docker run --gpus '"device=0"' --cpus 12.0 -d -it \
-v ~/../../media/bizon/data2tb/deep_medic/:/deep_medic/ \
tensorflow/tensorflow:latest-gpu bash
3. docker exec -it <docker_instance_name>dockerdoc
4. install deep_medic locally. See https://github.com/deepmedic/deepmedic.
5. go to folder with config files ../deepMedic/config_files/model
6. ./test_hnc_deepmedic.sh

## 3. Majority vote
1. Use test_set_deep_medic_3majority_vote.py. 
2. Adapt the paths to the output of deep medic models. 
3. Apapt output folder. 
4. Run the file: python test_set_deep_medic_3majority_vote.py

## 4 Resample to patient space
1. Use test_set_deep_medic_4resample_to_patient_space.py
2. Apapt path names: Ground truth paths to patient space containers, path to predicted dat and path to output destination. 

