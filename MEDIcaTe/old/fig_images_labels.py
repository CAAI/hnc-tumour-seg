import os
from os.path import dirname, basename, join, isfile, isdir
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from numpy import asarray
import copy
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import glob
import imageio
from skimage import img_as_ubyte, img_as_uint, img_as_float64
from pathlib import Path
import scipy.ndimage as ndimage
from pathlib import Path
import random
import shutil


def make_label_outline(input_nii,z):
    '''
    purpose: this function takes nifty image with z number of slices, and convert it into z number numpy arrays
    input: path to folder containing nifty images. path to folder for storing png images.
    '''
    
    img = nib.load(input_nii) #read nii
    img_fdata = img.get_fdata()
    ####('information about nii',img_fdata)
    ##print('information about nii', img.header.get_data_shape())
    
    slice = img_fdata[:, :, z] #Select which direction is the slice
    slice=img_as_ubyte(slice) #Convert an image to unsigned byte format, with values in [0, 255]
    slice = np.array(slice).astype('uint8')
    #print('information about slice:', slice)
    #print('information about slice:', slice.shape)
    #print('information about slice:', slice.dtype)
    slice1 = slice.copy()

    exist=[]
    
    
    gray=slice1.copy() #gray scale image
    if gray.any()>0: # if contour exist in slice
        
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
        #find contours
        #contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #find all possible contours and draw all points in contour
        contours,_ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
        

        im_countours=cv2.drawContours(slice1, contours, -1, (255, 0, 0), 7) #overlay contoures from findcontours() on slice1
        cv2.fillPoly(im_countours, pts =contours, color=1)
        image=im_countours.copy()
        
        im = Image.fromarray(image)
        im = im.convert("RGB")
        #print(img1.mode)
        #print(np.array(img1).shape)
        
        #im.save(f'{full_path_output}.png', format="png")
        exist=True
        a=im
    else:
        
        exist=False
        a=np.empty(0)
    return exist,a


def window_image(image, img_min, img_max):
    '''
    Purpose: changing brightness and contrast in image by specifing the minimum and maximum value of the window. 
    input: image, img_min and img_max
    output: window_image
    '''
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max


    #print(f'The minimum value in image is: {np.min(img_min)}')
    #print(f'The maximum value in image is: {np.max(img_max)}')  
    return window_image

def print_info_nii(nii_img):
    '''
    purpose print information about nifty
    '''
    # Getting information about images
    print(f'shape of  {nii_img}:', nii_img.shape)
    print(f'Data type of  {nii_img}:', nii_img.get_data_dtype())
    print(f'Voxel size of  {nii_img}:', nii_img.affine[0, 0])

def stack_images_labels(z,path_ct=None,path_pet=None,path_label1=None,path_label2=None):
    '''
    Purpose: generating slice of the ct/pet images with labels (l1 and l2)
    '''
    
    #generate the figure
    fig, axs = plt.subplots(1, 1, figsize=(20, 20))
    axs.set_axis_off()
    # Get information about fig
    #DPI = fig.get_dpi()
    #print("DPI:", DPI)
    #DefaultSize = fig.get_size_inches()
    #print("Default size in Inches", DefaultSize)
    #print(f"Which should result in a {DPI*DefaultSize[0]} x {DPI*DefaultSize[1]} Image")

    if path_ct is not None: 
        
        ################# create ct image ########################
        nii_img_ct  = nib.load(path_ct)# load nii
        img_ct = nii_img_ct.dataobj[..., z]
        # set window of CT image
        img_ct=window_image(img_ct, -135, 215) #350 // 40 == [-135;215]
        img_ct = ndimage.rotate(img_ct, 90, reshape=False)#rotate
        axs.imshow(img_ct,cmap='gray')
        
        if path_pet is not None:
            
            ################# create pet image ##############################
            nii_img_pet  = nib.load(path_pet)# load nii
            img_pet = nii_img_pet.dataobj[..., z]
            # set window of pet image
            img_pet=window_image(img_pet, 0.1, 7)
            img_pet = ndimage.rotate(img_pet, 90, reshape=False)#rotate
            axs.imshow(img_pet, cmap='hot',alpha=0.5)
            
        if path_label1 is not None:
           
            ################ create label 1 image #########################
            numpydata_md = asarray(path_label1)
            converted_array_md = np.array(numpydata_md, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l1 = nib.Nifti1Image(converted_array_md, affine)
            #print('md image header',nifti_file_l1.header)
            #print('shape of md label image', nifti_file_l1.header.get_data_shape())
            img_label_l1 = nifti_file_l1.dataobj[...,2]
            img_label_l1 = ndimage.rotate(img_label_l1, 90, reshape=False)#rotate
            cMap_blue=ListedColormap(['blue']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_blue)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l1_v1=copy.copy(img_label_l1) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l1_v1[img_label_l1_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l1_v1,cmap=my_cmap,alpha=0.7) 
        if path_label2 is not None:
            
            ################# create label 2 image #######################
            numpydata_ref = asarray(path_label2)
            converted_array_ref = np.array(numpydata_ref, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l2 = nib.Nifti1Image(converted_array_ref, affine)
            #print('ref image header',nifti_file_l2.header)
            #print('shape of ref label image', nifti_file_l2.header.get_data_shape()
            img_label_l2 = nifti_file_l2.dataobj[...,2]
            img_label_l2 = ndimage.rotate(img_label_l2, 90, reshape=False)#rotate
            cMap_green=ListedColormap(['green']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_green)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l2_v1=copy.copy(img_label_l2) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l2_v1[img_label_l2_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l2_v1,cmap=my_cmap,alpha=0.6)

    elif path_pet is not None:
       
        ################# create pet image ##############################
        nii_img_pet  = nib.load(path_pet)# load nii
        img_pet = nii_img_pet.dataobj[..., z]
        # set window of pet image
        img_pet=window_image(img_pet, 0.1, 7)
        img_pet = ndimage.rotate(img_pet, 90, reshape=False)#rotate
        axs.imshow(img_pet, cmap='hot',alpha=0.5)
        
        if path_label1 is not None:
            ################ create label 1 image #########################
            numpydata_md = asarray(path_label1)
            converted_array_md = np.array(numpydata_md, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l1 = nib.Nifti1Image(converted_array_md, affine)
            #print('md image header',nifti_file_l1.header)
            #print('shape of md label image', nifti_file_l1.header.get_data_shape())
            img_label_l1 = nifti_file_l1.dataobj[...,2]
            img_label_l1 = ndimage.rotate(img_label_l1, 90, reshape=False)#rotate
            cMap_blue=ListedColormap(['blue']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_blue)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l1_v1=copy.copy(img_label_l1) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l1_v1[img_label_l1_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l1_v1,cmap=my_cmap,alpha=0.7) 
        if path_label2 is not None:
            
            ################# create label 2 image #######################
            numpydata_ref = asarray(path_label2)
            converted_array_ref = np.array(numpydata_ref, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l2 = nib.Nifti1Image(converted_array_ref, affine)
            #print('ref image header',nifti_file_l2.header)
            #print('shape of ref label image', nifti_file_l2.header.get_data_shape()
            img_label_l2 = nifti_file_l2.dataobj[...,2]
            img_label_l2 = ndimage.rotate(img_label_l2, 90, reshape=False)#rotate
            cMap_green=ListedColormap(['green']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_green)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l2_v1=copy.copy(img_label_l2) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l2_v1[img_label_l2_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l2_v1,cmap=my_cmap,alpha=0.6)
        
    elif (path_pet and path_ct) is None:
        
        if path_label1 is not None:
            ################ create label 1 image #########################
            numpydata_md = asarray(path_label1)
            converted_array_md = np.array(numpydata_md, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l1 = nib.Nifti1Image(converted_array_md, affine)
            #print('md image header',nifti_file_l1.header)
            #print('shape of md label image', nifti_file_l1.header.get_data_shape())
            img_label_l1 = nifti_file_l1.dataobj[...,2]
            img_label_l1 = ndimage.rotate(img_label_l1, 90, reshape=False)#rotate
            cMap_blue=ListedColormap(['blue']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_blue)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l1_v1=copy.copy(img_label_l1) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l1_v1[img_label_l1_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l1_v1,cmap=my_cmap,alpha=0.7) 
        if path_label2 is not None:
            ################# create label 2 image #######################
            numpydata_ref = asarray(path_label2)
            converted_array_ref = np.array(numpydata_ref, dtype=np.float32)
            affine = np.eye(4)
            nifti_file_l2 = nib.Nifti1Image(converted_array_ref, affine)
            #print('ref image header',nifti_file_l2.header)
            #print('shape of ref label image', nifti_file_l2.header.get_data_shape()
            img_label_l2 = nifti_file_l2.dataobj[...,2]
            img_label_l2 = ndimage.rotate(img_label_l2, 90, reshape=False)#rotate
            cMap_green=ListedColormap(['green']) #create color for the label
            my_cmap = copy.copy(plt.cm.get_cmap(cMap_green)) #making the colormap
            my_cmap.set_bad(alpha=0) # set how the colormap handles 'bad' values
            # make background of label image transparent
            img_label_l2_v1=copy.copy(img_label_l2) #copy the md label image into a new name
            #defining the "bad" values as all values less than 255 hence only the label selected
            thresh=255
            img_label_l2_v1[img_label_l2_v1 < thresh] = np.nan # the "bad" are defines as NaN
            axs.imshow(img_label_l2_v1,cmap=my_cmap,alpha=0.6)
    
    plt.close(fig)#to not show figure   
    
    #print_info_nii(nii_img_pet)
    #print_info_nii(nii_img_ct)

    return fig



def image_processing(filename,image_path,output_path):
    '''
    Purpose: crop slice to a quadrant, thus removing part of background
    '''
    #create input and output path
    image_path=join(image_path,filename)
    output_path=join(output_path,filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path) 
    
    for filename in os.listdir(image_path):
        fullpath=join(image_path,filename)
      
        image = cv2.imread(fullpath) #loading image
        copy = image.copy() # make copy of image


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert image to grayscale
        thresh = cv2.threshold(gray,200,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1] #binarize image
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        ROI_number = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
            #we are only interested in large ROI since this is the patient in the image
            if w>150 and h>150:
                
                cv2.rectangle(copy,(x,y),(x+w,y+h),(155,155,0),1)
                #print ('shape of image before cropping',ROI.shape)
                
                # adding space around ROI and make sure the final image is a quadrant
                #s_max=max(ROI.shape[0:2])
                #print('largest dimension of image is: ', s_max)
                s=1000
                f = np.zeros((s,s,3),np.uint8) #make quadrat array to put image in
                ax,ay = (s - ROI.shape[1])//2,(s - ROI.shape[0])//2
                f[ay:ROI.shape[0]+ay,ax:ax+ROI.shape[1]] = ROI
                #print ('shape of image after cropping',f.shape)
                cv2.imwrite(f'{output_path}/{filename}', f)
                
            ROI_number += 1
        


def generate_mosaic_fig(image_path,filename,font=None):
    '''
    Purpose: generate an tiled image structure containing all slices with labels.  
    '''
    #full path to image
    image_path=join(image_path,filename)
    list_dir = os.listdir(image_path) 
    number_files = len(list_dir) #count number of files thus number of slices 
   
    coords=list(range(0, number_files))
    cols = 5
    rows = int(np.ceil(len(coords)/cols))

    # loading test image to set dimension on image that has to contain all the slices
    test_image=random.choice(os.listdir(image_path))
    test_image_path=join(image_path,test_image)
  
    #open slice as PIL image
    im1 = Image.open(test_image_path)
    a = np.repeat(np.arange(1,rows+1),cols)
    b = np.tile(np.arange(1,cols+1),rows)
    iter_idx = np.vstack((a,b)).T
    size_x, size_y = im1.size
    #print(f'the size of the image slices {im1.size}')
    im_all = Image.new('RGB', (size_y*cols, size_x*rows)) #create image to paste all slices in
    #print(f'size of im_all is: rows:{size_x*rows} and cols: {size_y*cols}')

    #make list with full path to png images
    slices_to_plot_list = []
    for filename in list_dir:
        slices_to_plot_list.append(os.path.join(image_path, filename))
    # sort the lists
    slices_to_plot_list.sort()
   
    for i, n in enumerate(slices_to_plot_list):
        
        infile=basename(n)
        cur_im = Image.open(join(image_path, infile)).convert('RGB') #
        size_x, size_y = cur_im.size #
        
        # print information 
        '''
        print('//////////////////////////////////')
        print('filepath is: ',n)
        print('the number is: ', i)
        print('the filename is: ',infile)
        print('size of image is: ',cur_im.size)
        print('//////////////////////////////////')
        '''
        

        
        # adding text to each slice within final image
        cur_slice_num = infile[-7:-4] #
        if font is not None:
            draw = ImageDraw.Draw(cur_im) #
            draw.text((10, 10), text=(f'z={cur_slice_num}'), font = font, align ="left", fill="white", width = 20)
        
        
        cur_idx = (iter_idx[i,:])
        t = ((cur_idx[1]-1)*size_x,(cur_idx[0]-1)*size_x,
            (cur_idx[1])*size_x,(cur_idx[0])*size_x) #(left, upper, right, lower)
        im_all.paste(cur_im,t)
        
    

    im_final = Image.new('RGB', (size_x*cols, size_y*rows))
    im_final.paste(im_all, (0,0))
    plt.axis('off')
    plt.imshow(im_final)
    return im_final

def saving_figure(fig,image_path,filename,z):

    if 10>z>=0:
        fig.savefig(f'{image_path}/{filename}_00{z}.png',bbox_inches='tight',facecolor='black')
    elif 100>z>9:
        fig.savefig(f'{image_path}/{filename}_0{z}.png',bbox_inches='tight',facecolor='black')
    elif z>99:
        fig.savefig(f'{image_path}/{filename}_{z}.png',bbox_inches='tight',facecolor='black')


def vizualization(final_path,ct_path=None,pet_path=None,label1_path=None,label2_path=None,slice_range=None,font=None):
    #checking input
    if ct_path is not None:
        filename=basename(ct_path)
        filename="_".join(filename.split("_")[:-1])
    elif pet_path is not None:
        filename=basename(pet_path)
        filename="_".join(filename.split("_")[:-1])
    elif label1_path is not None:
        filename=basename(label1_path)
        filename="_".join(filename.split("_")[:-1])
    elif label2_path is not None:
        filename=basename(label2_path)
        filename="_".join(filename.split("_")[:-1])

    if slice_range is None:
        slice_range=list(range(0, 174))

    #make temporary folder to store png images
    temp_path=join(final_path,'tmp')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    
    img_f_path = os.path.join(temp_path, filename)
    #Create a folder corresponding to the image of nii
    if not os.path.exists(img_f_path):
        os.mkdir(img_f_path) #New folder
    

    if (label1_path and label2_path and ct_path and pet_path) is not None: 
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            ################ Generate label 1 outline ##############################
            exist_l1,label_array_l1=make_label_outline(label1_path,z)
            ################ Generate label 2 outline ##############################
            exist_l2,label_array_l2=make_label_outline(label2_path,z)
            
            #make image if l1 or l2 exist in slice
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,path_label1=label_array_l1)
                     
                elif exist_l1==False and exist_l2==True:
                    
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,path_label2=label_array_l2)
                         
                else:
                   
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,path_label1=label_array_l1,path_label2=label_array_l2)
                
                #save slice
                saving_figure(fig,img_f_path,filename,z)
                
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')
    elif ((label2_path and ct_path and pet_path) is not None) and (label1_path is None): 
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            ################ Generate label 2 outline ##############################
            exist_l2,label_array_l2=make_label_outline(label2_path,z)
            if exist_l2==True:
                
                fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,path_label2=label_array_l2)     
               
                
                #save slice
                saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')
    elif ((label1_path and ct_path and pet_path) is not None) and (label2_path is None): #TODO handle when other cases is given to vizualization!!
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
           ################ Generate label 1 outline ##############################
            exist_l1,label_array_l1=make_label_outline(label1_path,z)
            if exist_l1==True:
                
                fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,path_label1=label_array_l1)
               

                #save slice
                saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')
    elif ((label1_path and label2_path and pet_path) is not None) and (ct_path is None): #TODO handle when other cases is given to vizualization!!
       
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
            ################ Generate label 1 outline ##############################
            exist_l1,label_array_l1=make_label_outline(label1_path,z)
            ################ Generate label 2 outline ##############################
            exist_l2,label_array_l2=make_label_outline(label2_path,z)
            
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    
                    fig=fig=stack_images_labels(z,path_pet=pet_path,path_label1=label_array_l1) 
                elif exist_l1==False and exist_l2==True:
                    
        
                    fig=fig=stack_images_labels(z,path_pet=pet_path,path_label2=label_array_l2)      
                else:
                    
                
                    fig=fig=stack_images_labels(z,path_pet=pet_path,path_label1=label_array_l1,path_label2=label_array_l2)  
                
            
                #save slice
                saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')
    elif ((label1_path and label2_path and ct_path) is not None) and (pet_path is None):
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
        
            ################ Generate label 1 outline ##############################
            exist_l1,label_array_l1=make_label_outline(label1_path,z)
            ################ Generate label 2 outline ##############################
            exist_l2,label_array_l2=make_label_outline(label2_path,z)
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    print('Only label1 exist')
                    
                    
                    fig=stack_images_labels(z,path_ct=ct_path,path_label1=label_array_l1) 
                elif exist_l1==False and exist_l2==True:
                    print('Only label2 exist')
        
                    fig=stack_images_labels(z,path_ct=ct_path,path_label2=label_array_l2)     
                else:
                    print('both label1 and label2 exist')
                
                    fig=stack_images_labels(z,path_ct=ct_path,path_label1=label_array_l1,path_label2=label_array_l2) 
                
                
                
                #save slice
                saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')
      
    else:
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
            
            ################ Generate label 1 outline ##############################
            exist_l1,label_array_l1=make_label_outline(label1_path,z)
            ################ Generate label 2 outline ##############################
            exist_l2,label_array_l2=make_label_outline(label2_path,z)
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    print('Only label1 exist')
                    
                    
                    fig=stack_images_labels(z,path_label1=label_array_l1) 
                elif exist_l1==False and exist_l2==True:
                    print('Only label2 exist')
        
                    fig=stack_images_labels(z,path_label2=label_array_l2)     
                else:
                    print('both label1 and label2 exist')
                
                    fig=stack_images_labels(z,path_label1=label_array_l1,path_label2=label_array_l2) 
                
    
                #save slice
                saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                print('No label exist in slice, thus incrementing slice number')

     
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # //////////////// image process slices \\\\\\\\\\\\\\\\\\\\\
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
       
    if (ct_path or pet_path) is not None:
        
        image_crop_path=join(final_path,'test_mosiac_cropped')
        image_processing(filename,temp_path,image_crop_path)

    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # ////////////////////CREATE MOSAIC\\\\\\\\\\\\\\\\\\\\\\\\\
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        if font is not None:
            mosaic_fig=generate_mosaic_fig(image_crop_path,filename,font=font)
        else:
            mosaic_fig=generate_mosaic_fig(image_crop_path,filename)
        
    else:
        if font is not None:
            mosaic_fig=generate_mosaic_fig(temp_path,filename,font=font)
        else:
            mosaic_fig=generate_mosaic_fig(temp_path,filename)
    mosaic_fig.save(join(final_path,f'{filename}_v1.png'),bbox_inches='tight')   
    #delete temp folder
    shutil.rmtree(temp_path)


if __name__ == '__main__':
    final_path='/home/fmik/data'
    ct='/home/fmik/data/MD_answers/t_l64/images/HNC03_003_0000.nii.gz'
    pet='/home/fmik/data/MD_answers/t_l64/images/HNC03_003_0001.nii.gz'
    l1='/home/fmik/data/MD_answers/t_l64/labels/md/HNC03_003_md.nii.gz'
    l2='/home/fmik/data/MD_answers/t_l64/labels/ref/HNC03_003_ref.nii.gz'
    z_list=list(range(84, 87))

    font = ImageFont.truetype('/home/fmik/data/AdventPro-ExtraLight.ttf',size=52)

    #vizualization(final_path,ct_path=ct,pet_path=pet,label1_path=l1,label2_path=l2)              
    vizualization(final_path,ct_path=ct,pet_path=pet,label1_path=l1,label2_path=l2,slice_range=z_list,font=font)
   