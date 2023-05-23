from MEDIcaTe.calculate_dice_haus import * 
from MEDIcaTe.visualization import * 
from MEDIcaTe.roi_generators import *
from MEDIcaTe.nii_resampling import * 
from MEDIcaTe.utilities import * 


def run_test():
    '''
    PURPOSE: load scripts included in MEDIcaTe, and check if scripts run succesfully by using example nifti files given in "MEDIcaTe/test/*"
    
    '''
    
    #path=dirname(__file__)
    path='/home/fmik/scripts/test'
    ###############################################################################################
    # Testing calculate_dice_haus()
    print('checking calculate_dice_haus.py...')
    calculate_dice_haus(in_path1=join(path,'md'),in_path2=join(path,'ref'),out_path=path)
    csv_path=join(path,'summary_MEDIcaTe.csv')
    df=pd.read_csv(csv_path, sep=',')
    if ((df.iloc[0, 1]==0.8741) and (df.iloc[0, 2]==4.1231)):
        print('   succes')
        os.remove(csv_path)
    else: 
        os.remove(csv_path)
        raise Exception("   error occur within calculate_dice_haus.py.")

    ###############################################################################################
    # Testing resample_nii_to_voxel_size() and resample_back_to_patient_space()
    input_path_abs=join(path,'HNC03_000_0000.nii.gz')
    os.mkdir(join(path,'resample'))
    output_path=join(path,'resample')
    output_path_abs=join(output_path,'HNC03_000_0000.nii.gz')
    print('checking nii_resampling.py...')
    resample_nii_to_voxel_size(input_path_abs, (-0.9765625, 0.9765625, 2.0),output_path=output_path)
    output_path_abs_2=join(output_path,'HNC03_000_0000_2.nii.gz')
    resample_back_to_patient_space(output_path_abs, input_path_abs,outname=output_path_abs_2)  
    equality_test=(get_affine(input_path_abs)==get_affine(output_path_abs_2))
    if equality_test.all():
        print('   succes')
        shutil.rmtree(output_path)
    else:
        shutil.rmtree(output_path)
        raise Exception("   error occur within nii_resampling.py.")
    
    


    ct=join(path,'HNC03_000_0000.nii.gz')
    pet=join(path,'HNC03_000_0001.nii.gz')
    ###############################################################################################    
    # Testing visualization()
    print('checking visualization.py...')
    visualization(final_path=join(path,'HNC03_000'),ct_path=ct,pet_path=pet,
                    l1_path=join(path,r'md/HNC03_000.nii.gz'),
                    cropping=False ,all_slices=False,
                    incl_info=True,outline=True,verbose=False)
    if os.path.exists(join(path,'HNC03_000.png')):
        print('   succes')
    else:
        raise Exception("   error occur within visualization.py.")

    ############################################################################################### 
    # Testing roi_generators.py
    print('checking roi_generators.py...')
    generate_rois_dm_ct(ct, path)
    generate_rois_dm_pt(pet, path)

    if os.path.exists(join(path,'HNC03_000_0001_roi.nii.gz')) and os.path.exists(join(path,'HNC03_000_0000_roi.nii.gz')):
        print('   succes')
        os.remove(join(path,'HNC03_000_0001_roi.nii.gz'))
        os.remove(join(path,'HNC03_000_0000_roi.nii.gz'))
    else:
        raise Exception("   error occur within roi_generators.py.")

def Entry_Point():
    parser = argparse.ArgumentParser(description='load scripts included in MEDIcaTe, and check if scripts run succesfully by using example nifti files given in "MEDIcaTe/test/*')
    
    run_test()

if __name__ == '__main__':
    run_test()

    # NOTE: har kun pushed test.py, nii-filerne som benyttes kan jeg ikke pushe de er for store. Men der ligger en folder som hedder test i "Loggede Data(:L)"" 
