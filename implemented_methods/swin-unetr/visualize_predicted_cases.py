from MEDIcaTe.optimized_visualization import visualization_optimized

if __name__ == '__main__':
    '''
    PURPOSE: Visualize labels drawn on ct/pet images. 
    The final image is a .png file where labels are drawn with following colors: 
        magenta - label 1.
        cyan - label 2.
        blue - overlapping region between label 1 and label 2.
    FUNCTION:
    visualization_optimized(final_path,ct_path,pet_path,label1_path,label2_path,slice_range,crop_image,full_visual,incl_info):

    INPUT:
        final_path      str             - full path to where output .png file will be stored, including name of final .png file(.png should not be included).
        ct_path:        str, optional   - Path to .nii file containing ct images from single patient.
        pet_path:       str, optional   - Path to .nii file containing pet images from single patient.
        label1_path:    str, optional   - Path to .nii file containing one set of labels drawn on single patient.
        label2_path:    str, optional   - Path to .nii file containing one set of labels drawn on single patient.
        slice_range:    bool, optional  - list containing slice numbers to be visualized.
        crop_image:     bool, optional  - if True images are cropped before plotted.
        full_visual:    bool, optional  - if False only slices containing labels is plotted.
        incl_info:      bool, optional  - if True slice numbers and min and max intensity values are is included in final .png file
        outline_label:  bool, optional  - if False label is shown as filled area.
    '''

   
    final_path=f'/homes/kovacs/project_scripts/hnc_segmentation/swin-unetr/research-contributions/SwinUNETR/BTCV/outputs/test_hnc1/output_visualized/HNC01_002'
    ct=f'/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train_norm/images/HNC01_002_0000.nii.gz' #0000
    pet=f'/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train_norm/images/HNC01_002_0001.nii.gz' #0001
    l1='/homes/kovacs/project_data/hnc-auto-contouring/inner-eye/d_train_norm/labels/HNC01_002.nii.gz'#f'/home/fmik/data/MD_answers/t_l64/labels/md/HNC03_060_md.nii.gz'
    l2='/homes/kovacs/project_scripts/hnc_segmentation/swin-unetr/research-contributions/SwinUNETR/BTCV/outputs/test_hnc1/HNC01_002.nii.gz'#f'/home/fmik/data/MD_answers/t_l64/labels/ref/HNC03_060_ref.nii.gz'
    visualization_optimized(final_path,ct_path=ct,pet_path=pet,label1_path=l1,label2_path=l2,crop_image=False ,full_visual=True,incl_info=True,outline_label=True,verbose=True)

