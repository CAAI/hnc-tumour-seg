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
from skimage import img_as_ubyte, img_as_uint, img_as_float64
import scipy.ndimage as ndimage
import random
import shutil


def make_label_outline(z,input_nii_1=None,input_nii_2=None):
    '''
    purpose: this function takes nifty image with z number of slices, and convert it into z number numpy arrays
    input: path to folder containing nifty images. path to folder for storing png images.
    '''
    slice=np.zeros((512,512), dtype=int)
    slice_canvas=np.array(slice).astype('uint8')

    
    if (input_nii_1) is not None:
        
        img_1 = nib.load(input_nii_1) #read nii
        img_fdata_1 = img_1.get_fdata()
        slice_1 = img_fdata_1[:, :, z] #Select which direction is the slice
        slice_1=img_as_ubyte(slice_1) #Convert an image to unsigned byte format, with values in [0, 255]
        slice_1 = np.array(slice_1).astype('uint8')
        slice1 = slice_1.copy()

        gray1=slice1.copy() #gray scale image
        if input_nii_2 is not None:
            
            img_2 = nib.load(input_nii_2) #read nii
            img_fdata_2 = img_2.get_fdata()
            slice_2 = img_fdata_2[:, :, z] #Select which direction is the slice
            slice_2=img_as_ubyte(slice_2) #Convert an image to unsigned byte format, with values in [0, 255]
            slice_2 = np.array(slice_2).astype('uint8')
            slice2 = slice_2.copy()
         
            gray2=slice2.copy() #gray scale image
            if gray1.any()>0 and gray2.any()>0 : # if contour exist in slice
                
                _, thresh1 = cv2.threshold(gray1, 1, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
                _, thresh2 = cv2.threshold(gray2, 1, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
                
                #find contours
                contours1,_ = cv2.findContours(thresh1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
                contours2,_ = cv2.findContours(thresh2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
                
                #Numpy array with label1
                im1_countours=cv2.drawContours(slice1, contours1, -1, (255, 0, 255), 5) #overlay contoures from findcontours() on slice1
                img1=cv2.fillPoly(im1_countours, pts =contours1, color=1)
                image1=img1.copy()
                

                #Numpy array with label2
                im2_countours=cv2.drawContours(slice2, contours2, -1, (255, 0, 0), 5) #overlay contoures from findcontours() on slice1
                img2=cv2.fillPoly(im2_countours, pts =contours2, color=1)
                image2=img2.copy()
                

                #Numpy array with label1 and label2
                im3_countours=cv2.drawContours(slice_canvas, contours1, -1, (255, 0, 0), 5) #overlay contoures from findcontours() on slice1
                img3=cv2.fillPoly(im3_countours, pts =contours2, color=1)
                im4_countours=cv2.drawContours(slice_canvas, contours2, -1, (255, 0, 0), 5) #overlay contoures from findcontours() on slice1
                img4=cv2.fillPoly(im4_countours, pts =contours2, color=1)
                image4=img4.copy()
                
                image12_1=np.equal(image1,image2) 
                int_image12_1 = np.multiply(image12_1, 255)
                int_image12_1_c=int_image12_1.copy()
                

                image4_inv=np.invert(image4) 
                image_equal= np.not_equal(image4_inv,int_image12_1_c)
                int_image_equal = np.multiply(image_equal, 255)
                image1_2=int_image_equal-image4_inv
                image1_2_c=image1_2.copy()
                image1_2=np.uint8(image1_2_c)
                

                #convert binary to rgb images  
                im1 = Image.fromarray(image1)
                im1 = im1.convert("RGB")
                im2 = Image.fromarray(image2)
                im2 = im2.convert("RGB")
                im3 = Image.fromarray(image1_2)
                im3 = im3.convert("RGB")
                
                
                a1=im1
                a2=im2
                a3=im3
                exist1=True
                exist2=True
            elif gray2.any()>0:
                _, thresh2 = cv2.threshold(gray2, 1, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
                #find contours
                contours2,_ = cv2.findContours(thresh2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
                
                #Numpy array with label2
                im2_countours=cv2.drawContours(slice2, contours2, -1, (255, 0, 0), 5) #overlay contoures from findcontours() on slice1
                img2=cv2.fillPoly(im2_countours, pts =contours2, color=1)
                image2=img2.copy()
                #cv2.imwrite('/home/fmik/scripts/image2.png', image2)

                im2 = Image.fromarray(image2)
                im2 = im2.convert("RGB")
                
    
                exist1=False
                exist2=True
                a1=[]
                a2=im2
                a3=[]    
            elif gray1.any()>0:
                
                _, thresh1 = cv2.threshold(gray1, 1, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
                #find contours
                contours1,_ = cv2.findContours(thresh1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
                
                #Numpy array with label1
                im1_countours=cv2.drawContours(slice1, contours1, -1, (255, 0, 255), 5) #overlay contoures from findcontours() on slice1
                img1=cv2.fillPoly(im1_countours, pts =contours1, color=1)
                image1=img1.copy()
        
                #convert binary to rgb images  
                im1 = Image.fromarray(image1)
                im1 = im1.convert("RGB")
                
                exist1=True
                exist2=False
                a1=im1
                a2=[]
                a3=[]
                
            else:
                exist1=False
                exist2=False
                a1=[]
                a2=[]
                a3=[]
        
     
    elif input_nii_2 is not None:
      
        img_2 = nib.load(input_nii_2) #read nii
        img_fdata_2 = img_2.get_fdata()
        slice_2 = img_fdata_2[:, :, z] #Select which direction is the slice
        slice_2=img_as_ubyte(slice_2) #Convert an image to unsigned byte format, with values in [0, 255]
        slice_2 = np.array(slice_2).astype('uint8')
        slice2 = slice_2.copy()
        
        gray2=slice2.copy() #gray scale image
        
        if gray2.any()>0:
            
            _, thresh2 = cv2.threshold(gray2, 1, 255, cv2.THRESH_BINARY) #convert grayscale to binary using thresholding
            
            #find contours
            contours2,_ = cv2.findContours(thresh2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) #less time consuming
            
            #Numpy array with label2
            im2_countours=cv2.drawContours(slice2, contours2, -1, (255, 0, 0), 5) #overlay contoures from findcontours() on slice1
            img2=cv2.fillPoly(im2_countours, pts =contours2, color=1)
            image2=img2.copy()
            
            im2 = Image.fromarray(image2)
            im2 = im2.convert("RGB")
            
            
            exist1=False
            exist2=True
            a1=[]
            a2=im2
            a3=[]
        else:
           
            exist1=False
            exist2=False
            a1=[]
            a2=[]
            a3=[]
    
    return exist1,exist2,a1,a2,a3


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

def outline_prep(label,color_map):
    '''
    purpose: prepare outline to enable using Matplotlib
    '''

    numpydata = asarray(label)
    converted_array = np.array(numpydata, dtype=np.float32)
    nifti_file = nib.Nifti1Image(converted_array, affine=np.eye(4))
    img_label = nifti_file.dataobj[...,2]
    img_label = ndimage.rotate(img_label, 90, reshape=False)#rotate
    color_map.set_bad(alpha=0) # set how the colormap handles 'bad' values
    # make background of label image transparent
    img_label_c=copy.copy(img_label) #copy the md label image into a new name
    #defining the "bad" values as all values less than 255 hence only the label selected
    thresh=100
    img_label_c[img_label_c < thresh] = np.nan 
    return img_label_c


def stack_images_labels(z,path_ct=None,path_pet=None,label1=None,label2=None,label3=None):
    '''
    Purpose: generating slice of the ct/pet images with labels (l1 and l2)
    '''
    
    # Make colormaps 
    cMap_cyan=ListedColormap(['cyan']) #create color for the label1
    cyan_map = copy.copy(plt.cm.get_cmap(cMap_cyan)) 
    cMap_mag=ListedColormap(['magenta']) #create color for the label2
    mag_map = copy.copy(plt.cm.get_cmap(cMap_mag)) 
    cMap_blue=ListedColormap(['blue']) #create color for the label12
    blue_map = copy.copy(plt.cm.get_cmap(cMap_blue)) 

    #generate the figure
    fig, axs = plt.subplots(1, 1, figsize=(20, 20))
    axs.set_axis_off()
    # Get information about fig
    #DPI = fig.get_dpi()
    #print("DPI:", DPI)
    #DefaultSize = fig.get_size_inches()
    #print("Default size in Inches", DefaultSize)
    #print(f"Which should result in a {DPI*DefaultSize[0]} x {DPI*DefaultSize[1]} Image")

    if (path_ct and path_pet) is not None: 
        
        ################# create ct image ########################
        nii_img_ct  = nib.load(path_ct)# load nii
        img_ct = nii_img_ct.dataobj[..., z]
        # set window of CT image
        img_ct=window_image(img_ct, -135, 215) #350 // 40 == [-135;215]
        img_ct = ndimage.rotate(img_ct, 90, reshape=False)#rotate
        axs.imshow(img_ct,cmap='gray')
        
        
        ################# create pet image ##############################
        nii_img_pet  = nib.load(path_pet)# load nii
        img_pet = nii_img_pet.dataobj[..., z]
        # set window of pet image
        img_pet=window_image(img_pet, 0.1, 7)
        img_pet = ndimage.rotate(img_pet, 90, reshape=False)#rotate
        axs.imshow(img_pet, cmap='hot',alpha=0.5)
            
        if (label1 and label2) is not None:
            ################# create labels #######################
            img_label_1=outline_prep(label1,cyan_map) #label 1
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1) 

            img_label_2=outline_prep(label2,mag_map) #label 2
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)

            img_label_3=outline_prep(label3,blue_map) #overlap
            axs.imshow(img_label_3,cmap=blue_map,alpha=1) 
        elif label2 is not None:
            ################# create only label 2 image #######################
            img_label_2=outline_prep(label2,mag_map)
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)
        elif label1 is not None:
            ################# create only label 1 image #######################
            img_label_1=outline_prep(label1,cyan_map)
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1) 
        

     
    elif path_pet is not None:
        ################# create pet image ##############################
        nii_img_pet  = nib.load(path_pet)# load nii
        img_pet = nii_img_pet.dataobj[..., z]
        # set window of pet image
        img_pet=window_image(img_pet, 0.1, 7)
        img_pet = ndimage.rotate(img_pet, 90, reshape=False)#rotate
        axs.imshow(img_pet, cmap='hot',alpha=0.5)
        
        if (label1 and label2) is not None:
            
            ################# create labels #######################
            img_label_1=outline_prep(label1,cyan_map) #label 1
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1) 

            img_label_2=outline_prep(label2,mag_map) #label 2
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)

            img_label_3=outline_prep(label3,blue_map) #overlap
            axs.imshow(img_label_3,cmap=blue_map,alpha=1) 
        elif label2 is not None:
            ################# create only label 2 image #######################
            img_label_2=outline_prep(label2,mag_map)
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)
        elif label1 is not None:
            ################# create only label 1 image #######################
            img_label_1=outline_prep(label1,cyan_map)
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1)
        
        
    elif (path_pet and path_ct) is None:
        
        if (label1 and label2) is not None:
                    
            ################# create labels #######################
            img_label_1=outline_prep(label1,cyan_map) #label 1
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1) 

            img_label_2=outline_prep(label2,mag_map) #label 2
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)

            img_label_3=outline_prep(label3,blue_map) #overlap
            axs.imshow(img_label_3,cmap=blue_map,alpha=1)  
        elif label2 is not None:
            
           ################# create only label 2 image #######################
            img_label_2=outline_prep(label2,mag_map)
            axs.imshow(img_label_2,cmap=mag_map,alpha=1)
        elif label1 is not None:
            
           ################# create only label 1 image #######################
            img_label_1=outline_prep(label1,cyan_map)
            axs.imshow(img_label_1,cmap=cyan_map,alpha=1)
        else:
            print('')
    
    plt.close(fig)#to not show figure   
    

    return fig



def image_processing(filename,image_path,output_path):
    '''
    Purpose: identify contours in binary image and use area as classifier to identify patient outline.
    output: png image containing patient and with added black background to make image quadrant
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
        thresh = cv2.threshold(gray,2,255,cv2.THRESH_BINARY)[1] #binarize image
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        ROI_number = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
            #we are only interested in large ROI since this is the patient in the image
            if w>150 and h>150:
                
                cv2.rectangle(copy,(x,y),(x+w,y+h),(0,0,0),1)
                #print ('shape of image before cropping',ROI.shape)
                # adding space around ROI and make sure the final image is a quadrant
                #s_max=max(ROI.shape[0:2])
                #print('largest dimension of image is: ', s_max)
                s=1000 #wanted size of image
                f = np.zeros((s,s,3),np.uint8) #make quadrat array to put image in
                ax,ay = (s - ROI.shape[1])//2,(s - ROI.shape[0])//2
                f[ay:ROI.shape[0]+ay,ax:ax+ROI.shape[1]] = ROI
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
        
        # adding text to each slice within final image
        cur_slice_num = infile[10:-4] #
        if font is not None:
            draw = ImageDraw.Draw(cur_im) #
            draw.text((10, 300), text=(f'z={cur_slice_num}'), font = font, align ="left", fill="white", width = 20)
        
        
        cur_idx = (iter_idx[i,:])
        t = ((cur_idx[1]-1)*size_x,(cur_idx[0]-1)*size_x,
            (cur_idx[1])*size_x,(cur_idx[0])*size_x) #(left, upper, right, lower)
        im_all.paste(cur_im,t)
        
    

    im_final = Image.new('RGB', (size_x*cols, size_y*rows))
    w=size_x*cols
    h=size_y*rows
    im_final.paste(im_all, (0,0))
    
    name="_".join(filename.split("_")[:-1])
    draw1 = ImageDraw.Draw(im_final)
    draw1.rectangle( (w-1000,0,w,120), fill="white" )
    draw1.text((w-950,20),text=(f'nn_unet_id: {name}'), font=font,fill='black')
    draw1.line((0, 30, w-4900, 30), fill='cyan', width=10)
    draw1.line((0, 90, w-4900, 90), fill='magenta', width=10)
    draw1.line((0, 150, w-4900, 150), fill='blue', width=10)
    #cyan - label 1
    #mag - label 2
    #blue- overlap
    draw1.text((w-4850, 0), text="label 1",font=font,fill="white",width = 20)
    draw1.text(( w-4850, 55), text="label 2",font=font,fill="white",width = 20)
    draw1.text(( w-4850, 105), text="overlapping region",font=font,fill="white",width = 20)
   

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




def vizualization(final_path,ct_path=None,pet_path=None,label1_path=None,label2_path=None,slice_range=None,font=None, verbose = False):
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
        if ct_path is not None:
            nii_img=nib.load(ct_path)
            [x,y,z]=nii_img.shape
            slice_range=list(range(0, z))
        elif pet_path is not None:
            nii_img=nib.load(pet_path)
            [x,y,z]=nii_img.shape
            slice_range=list(range(0, z))
        elif label1_path is not None:
            nii_img=nib.load(label1_path)
            [x,y,z]=nii_img.shape
            slice_range=list(range(0, z))
        elif label2_path is not None:
            nii_img=nib.load(label2_path)
            [x,y,z]=nii_img.shape
            slice_range=list(range(0, z))
        

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
            if verbose:
                print(f'//////////////////  slice {z} ////////////////////////')
            ################ Generate label 1 outline ##############################
            exist_l1,exist_l2,a1,a2,a3=make_label_outline(z,label1_path,label2_path)
            
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,label1=a1)
                    saving_figure(fig,img_f_path,filename,z)
                elif exist_l1==False and exist_l2==True:
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,label2=a2)
                    saving_figure(fig,img_f_path,filename,z)
                else:
                    fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,label1=a1,label2=a2,label3=a3)
                    saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
              
    elif ((label2_path and ct_path and pet_path) is not None) and (label1_path is None): 
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            ################ Generate label 2 outline ##############################
            exist_l1,exist_l2,a1,a2,a3=make_label_outline(z,label2_path)
            
            if exist_l2==True:
                fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,label2=a2)
                saving_figure(fig,img_f_path,filename,z)     
            else:
                z+=1
                
    elif ((label1_path and ct_path and pet_path) is not None) and (label2_path is None): 
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            ################ Generate label 1 outline ##############################
            exist_l1,exist_l2,a1,a2,a3=make_label_outline(z,label1_path)
            
            if exist_l1==True:
                fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path,label1=a1)
                saving_figure(fig,img_f_path,filename,z)     
            else:
                z+=1
               
    elif ((label1_path and label2_path and pet_path) is not None) and (ct_path is None): 
       
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
            exist_l1,exist_l2,a1,a2,a3=make_label_outline(z,label1_path,label2_path)
            
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    fig=stack_images_labels(z,path_pet=pet_path,label1=a1)
                    saving_figure(fig,img_f_path,filename,z)
                elif exist_l1==False and exist_l2==True:
                    fig=stack_images_labels(z,path_pet=pet_path,label2=a2)
                    saving_figure(fig,img_f_path,filename,z)
                else:
                    fig=stack_images_labels(z,path_pet=pet_path,label1=a1,label2=a2,label3=a3)
                    saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                
    elif ((label1_path and label2_path and ct_path) is not None) and (pet_path is None):
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
            exist_l1,exist_l2,a1,a2,a3=make_label_outline(z,label1_path,label2_path)
            
            if exist_l1==True or exist_l2==True:
                if exist_l1==True and exist_l2==False:
                    fig=stack_images_labels(z,path_ct=ct_path,label1=a1)
                    saving_figure(fig,img_f_path,filename,z)
                elif exist_l1==False and exist_l2==True:
                    fig=stack_images_labels(z,path_ct=ct_path,label2=a2)
                    saving_figure(fig,img_f_path,filename,z)
                else:
                    fig=stack_images_labels(z,path_ct=ct_path,label1=a1,label2=a2,label3=a3)
                    saving_figure(fig,img_f_path,filename,z)
            else:
                z+=1
                
      
    else:
        
        for z in slice_range: 
            print(f'//////////////////  slice {z} ////////////////////////')
            
            fig=stack_images_labels(z,path_ct=ct_path,path_pet=pet_path)
            saving_figure(fig,img_f_path,filename,z)
                
    
     
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # //////////////// image process slices \\\\\\\\\\\\\\\\\\\\\
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
       
    if (ct_path or pet_path) is not None:
        
        #image_crop_path=join(final_path,'test_mosiac_cropped')
        #image_processing(filename,temp_path,image_crop_path)

    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # ////////////////////CREATE MOSAIC\\\\\\\\\\\\\\\\\\\\\\\\\
    # //////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        if font is not None:
            mosaic_fig=generate_mosaic_fig(temp_path,filename,font=font)
        else:
            mosaic_fig=generate_mosaic_fig(temp_path,filename)
        
    else:
        if font is not None:
            mosaic_fig=generate_mosaic_fig(temp_path,filename,font=font)
        else:
            mosaic_fig=generate_mosaic_fig(temp_path,filename)
    mosaic_fig.save(join(final_path,f'{filename}.png'),bbox_inches='tight')  
    
    #delete temp folder
    shutil.rmtree(temp_path)

if __name__ == '__main__':
    final_path='/home/fmik/data'
    ct='/home/fmik/data/MD_answers/t_l64/images/HNC03_040_0000.nii.gz'
    pet='/home/fmik/data/MD_answers/t_l64/images/HNC03_040_0001.nii.gz'
    l1='/home/fmik/data/MD_answers/t_l64/labels/md/HNC03_040_md.nii.gz'
    l2='/home/fmik/data/MD_answers/t_l64/labels/ref/HNC03_040_ref.nii.gz'
    z_list=list(range(80, 101))

    font = ImageFont.truetype('/home/fmik/data/AdventPro-ExtraLight.ttf',size=52)
             
    vizualization(final_path,ct_path=ct,pet_path=pet,label1_path=l1,label2_path=l2,slice_range=z_list,font=font)
   