'''
Purpose: 
    - From nifty files generate af grid of content to view data. 

Inputs: 
    - Nifty images. 

Outputs: 
    - Png image saved on destination path. 

By David Gergely Kovacs Petersen 25-FEB-2022
'''

import os
import random
import subprocess
import stat

def create_figs(pet = True, lab = True):
    path_to_labels = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/labelsTr'
    path_to_images = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/imagesTr'
    path_to_dest = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/figs'
    path_to_dest_tmp = '/homes/kovacs/project_data/hnc-auto-contouring/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task500_HNC01/figs/tmp_files'
    c = os.listdir(path_to_labels) # cases
    random.seed(20211202)
    #t = random.sample(c, k=100) # test cases
    t = ['HNC01_133.nii.gz']

    for p in t:
        print(p)
        s_ct = f'{path_to_images}/{p[:-7]}_0000.nii.gz'
        s_pt = f'{path_to_images}/{p[:-7]}_0001.nii.gz'
        d_ct = f'{path_to_dest_tmp}/{p[:-7]}_0000_rgb.nii.gz'
        d_pt = f'{path_to_dest_tmp}/{p[:-7]}_0001_rgb.nii.gz'
        d_pt_m = f'{path_to_dest_tmp}/{p[:-7]}_0001_rgb_mask.nii.gz'
        
        o = f'{path_to_dest}/{p[:-7]}.png'# out image

        c0 = f'ThresholdImage 3 {s_pt} {d_pt_m} 0 0 0 1'
        c1 = f'ConvertScalarImageToRGB 3 {s_ct} {d_ct} none grey none -115 215 0 255'
        c2 = f'ConvertScalarImageToRGB 3 {s_pt} {d_pt} none hot none 1 7 0 255'
        
        if lab & pet:
            s_rt = f'{path_to_labels}/{p}'
            d_rt = f'{path_to_dest_tmp}/{p[:-7]}_rgb.nii.gz'
            d_rt_m = f'{path_to_dest_tmp}/{p[:-7]}_rgb_mask.nii.gz'
            c3 = f'ThresholdImage 3 {s_rt} {d_rt_m} 0 0 0 1'
            c4 = f'ConvertScalarImageToRGB 3 {s_rt} {d_rt} none green none 0 1 0 255'
            c5 = f'CreateTiledMosaic -i {d_ct} -e [{d_pt},{d_pt_m},0.3] [{d_rt},{d_rt_m},0.6] -o {o} -d z -f 0x1' #
            p0 = subprocess.Popen(c0, shell = True, stderr = subprocess.PIPE)
            p0.wait()
            p1 = subprocess.Popen(c1, shell = True, stderr = subprocess.PIPE)
            p1.wait()
            p2 = subprocess.Popen(c2, shell = True, stderr = subprocess.PIPE)
            p2.wait()
            p3 = subprocess.Popen(c3, shell = True, stderr = subprocess.PIPE)
            p3.wait()
            p4 = subprocess.Popen(c4, shell = True, stderr = subprocess.PIPE)
            p4.wait()
            p5 = subprocess.Popen(c5, shell = True, stderr = subprocess.PIPE)
            p5.wait()
            error = p5.communicate()
            print(f'wi GTV PET - ERROR={error}')
        elif pet & (not lab): 
            c3 = f'CreateTiledMosaic -i {d_ct} -e [{d_pt},{d_pt_m},0.3] -o {o} -d z -f 0x1' #
            p0 = subprocess.Popen(c0, shell = True, stderr = subprocess.PIPE)
            p0.wait()
            p1 = subprocess.Popen(c1, shell = True, stderr = subprocess.PIPE)
            p1.wait()
            p2 = subprocess.Popen(c2, shell = True, stderr = subprocess.PIPE)
            p2.wait()
            p3 = subprocess.Popen(c3, shell = True, stderr = subprocess.PIPE)
            p3.wait()
            error = p3.communicate()
            print(f'no GTV_PET - ERROR={error}')
        elif (not pet) & (not lab):
            c3 = f'CreateTiledMosaic -i {d_ct} -o {o} -d z -f 0x1'
            p0 = subprocess.Popen(c0, shell = True, stderr = subprocess.PIPE)
            p0.wait()
            p1 = subprocess.Popen(c1, shell = True, stderr = subprocess.PIPE)
            p1.wait()
            p3 = subprocess.Popen(c3, shell = True, stderr = subprocess.PIPE)
            p3.wait()
            error = p3.communicate()
            print(f'CT alone - ERROR={error}')
        for f in os.listdir(path_to_dest_tmp):
            fi = f'{path_to_dest_tmp}/{f}'
            try:
                st = os.stat(fi)
                os.chmod(fi,st.st_mode | stat.S_IEXEC)
                os.remove(fi)
            except OSError:
                raise


if __name__ == '__main__':
    create_figs()

