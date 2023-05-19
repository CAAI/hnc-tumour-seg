Deep learning for head and neck cancer segmentation<a name="TOP"></a>



# MEDIcaTe
## Purpose
The MEDIcaTe-package is an image processing tools for 3d multimodality medical images (such as PET-CT images). The purpose and function of the MEDIcaTE-package can be devided into two parts, reflected by the two subfolders, implemented_methods and MEDIcaTe. The former includes scripts from external sources and has the purpose of ... . The latter MEDIcaTe subfolder includes scripts purposely designed for medical image processing including tools for visualization and calculating dice and hausdorff coefficient as a measure of comparison between different areas referred to as labels.   


## Installation
MEDIcaTe is tested on and supported by Python 3. Earlier versions are not guaranteed to work.

MEDIcaTe is installed by using the following lines.
```bash
    git clone https://github.com/MedTekHuset/MEDIcaTe
    cd MEDIcaTe
```
### Install editable mode:
```pip install -e .``` 
When using this mode a copy of MEDIcaTE is created on your computer, hence allowing for modifications. 
### Install normal (safe) mode:
```pip install .``` 

## Prerequisites
Running scripts in MEDIcaTe requires installation of specific packages and libaries. medicate-env.txt contains a txt-file copy of a conda environment that fullfill requirements. A copy of the enviorment can be attained by using:
```bash
    conda env create --file medicate-env.txt.
```
To ensure that requirement are fullfilled a test run with example files can be initiated by running test.py. If test.py run succesfully, requirements are fullfilled.

## Usage
When using MEDIcaTe images (ct and pet) and labels must be 3D nifti files (.nii.gz)! An example of how to structure 3D nifti files to use as inputs are illustrated below:
```
  data/
    ├── output
    │     └── 
    │     └── 
    │     └── 
    ├── images
    │     ├── HNC03_000_0000.nii.gz
    │     ├── HNC03_000_0001.nii.gz
    │     ├── HNC03_001_0000.nii.gz
    │     ├── HNC03_001_0001.nii.gz
    │     ├── HNC03_002_0000.nii.gz
    │     ├── HNC03_002_0001.nii.gz
    │     ├── HNC03_003_0000.nii.gz
    │     └── HNC03_003_0001.nii.gz
    ├── labels
    │     ├── label1
    │          ├── HNC03_000.nii.gz
    │          ├── HNC03_001.nii.gz
    │          ├── HNC03_002.nii.gz
    │          └── HNC03_003.nii.gz
    │     ├── label2
    │          ├── HNC03_000.nii.gz
    │          ├── HNC03_001.nii.gz
    │          ├── HNC03_002.nii.gz
    │          └── HNC03_003.nii.gz     
    └── setup.py
```  

Using the above structure, MEDIcaTe tools can be called as command line functions, with the structure descriped in the EXAMPLES below.
Labels must be, when converted from nifti to numpy array, represented as binary array. where 1 represents label and 0 represents background.  
### Command line functions
At the moment this package includes three command line functions.
**The first one**, test, takes no input and simply makes a test run of scripts in MEDIcaTe using example files. test is usefull for initially testing if packages and libraries is installed correctly.

EXAMPLE
```bash
test
```

**The second one**, dice_haus, calculates the dice_haus. To run it you have to specify the paths for two files or folders containing labels and an output path for the result. see ```dice_haus -h``` for more information.

dice_haus [-h] [-out_path OUT_PATH] [-processes PROCESSES] in_path1 in_path2

EXAMPLE
```bash
dice_haus '/data/labels/label1' '/data/labels/label2' -out_path '/data/output'
```

**The third one**, visualization, is used to visualize, 3D ct nifti and/or 3D pet nifty and/or up to three label nifties, as a png-file. multiple options is available, see ```visualization -h``` for more information. 


visualization [-h] [-ct_path CT_PATH] [-pet_path PET_PATH] [-l1_path L1_PATH] [-l1_name L1_NAME] [-l2_path L2_PATH] [-l2_name L2_NAME]
                [-l3_path L3_PATH] [-l3_name L3_NAME] 
                [-slices SLICES] [-cropping CROPPING] [-all_slices ALL_SLICES] [-incl_info INCL_INFO]
                [-outline OUTLINE] [-verbose VERBOSE]
                final_path

EXAMPLE

```bash
visualization '/data/figs/HNC03_002' -ct_path '/data/images/HNC03_002_0000.nii.gz' -pet_path '/data/images/HNC03_002_0001.nii.gz' -l1_path '/data/labels/label1/HNC03_002.nii.gz'
```
