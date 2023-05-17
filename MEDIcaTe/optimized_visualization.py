'''
Puporse: Plotting this type of case, where you define "this"

Requirements to run this: 

----
By Freja ...
Dato
Affiliation:
Use is your own responsibility (license here)
'''
   
import os
from os.path import dirname, basename, join, isfile
from tabnanny import verbose
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy.ma as ma
from mycolorpy import colorlist as mcp
import pandas as pd
import matplotlib.colors as colors
import argparse


def gen_dataframe(labels,slices):
    '''
    PURPOSE: make dataframe that states whether label exist in slice(TRUE) or not(FALSE) 
    INPUT:
        labels:             ndarray           - 3D array where
                                                     (0)   is background,
                                                     (1)   is label 1,
                                                     (2)   is label 2,
                                                     (3)   is label 3,
                                                     (13)  is overlap between label 1 and 3
                                                     (12)  is overlap between label 1 and 2
                                                     (23)  is overlap between label 2 and 3
                                                     (123) is overlap between label 1,2 and 3
        slices:        List              - List containing slice numbers                                             
    OUTPUT:
       label_exist:         dataframe        
    '''
    z_all=[]
    idx_all=[]
    label1_all=[]
    label2_all=[]
    label3_all=[]

    for i,z in enumerate(slices):
        idx_all.append(i)
        z_all.append(z)
        if (1 or 12 or 13 or 123) in np.unique(labels[:,:,i]):
            label1_all.append(True)
        else:
            label1_all.append(False)
        if (2 or 23 or 12 or 123) in np.unique(labels[:,:,i]):
            label2_all.append(True)
        else:
            label2_all.append(False)
            
        if (3 or 23 or 13 or 123) in np.unique(labels[:,:,i]):
            label3_all.append(True)
        else:
            label3_all.append(False)
            
    
    label_exist=pd.DataFrame({  
        'idx': idx_all,         
        'z': z_all, 
        'label1': label1_all,
        'label2': label2_all,
        'label3': label3_all})
   
    return label_exist



def get_labels(L1_numpy,L2_numpy,L3_numpy):
    '''
    PURPOSE: make numpy array containing all labels. labels are NOT outlined. 
    FUNCTION: get_labels(L1_numpy,L2_numpy,L3_numpy)
    INPUT:
        L1_numpy/L2_numpy/L3_numpy: binary, ndarray   - 3D arrays containing labels. (1) represent outlined area and (0) is bacground.                                                        
    OUTPUT:
        labels:                     ndarray           - 3D array where
                                                                (0)   is background,
                                                                (1)   is label 1,
                                                                (2)   is label 2,
                                                                (3)   is label 3,
                                                                (13)  is overlap between label 1 and 3
                                                                (12)  is overlap between label 1 and 2
                                                                (23)  is overlap between label 2 and 3
                                                                (123) is overlap between label 1,2 and 3        
    '''
    L1_numpy_c=L1_numpy.copy()
    L2_numpy_c=L2_numpy.copy()
    L3_numpy_c=L3_numpy.copy()

    L1_numpy_c=np.ceil(L1_numpy_c)
    L2_numpy_c=np.ceil(L2_numpy_c)
    L3_numpy_c=np.ceil(L3_numpy_c)

    if verbose:
        if (L1_numpy.any()>0 or L2_numpy.any()>0 or L3_numpy.any()>0):
            print('labels exist')
        else:
            print('labels dont exist')

   
    L1_numpy_c = np.where(L1_numpy_c == 1., 2., L1_numpy_c) # L1 = 2
    L2_numpy_c = np.where(L2_numpy_c == 1., 3., L2_numpy_c) # L2 = 3
    L3_numpy_c = np.where(L3_numpy_c == 1., 4., L3_numpy_c) # L4 = 4

    labels=L1_numpy_c+L2_numpy_c+L3_numpy_c
    labels = np.where(labels == 9, 123, labels)   # L1/L2/L3 overlap = 9
    labels = np.where(labels == 5, 12, labels)    # L1/L2    overlap = 5
    labels = np.where(labels == 6, 13, labels)    # L1/  L3  overlap = 6
    labels = np.where(labels == 7, 23, labels)    #    L2/L3 overlap = 7
    labels = np.where(labels == 2, 1, labels)     # L1               = 2
    labels = np.where(labels == 3, 2, labels)     # L2               = 3
    labels = np.where(labels == 4, 3, labels)     # L3               = 4

    
    return labels
    


def get_outlined_labels(L1_numpy,L2_numpy,L3_numpy):
    '''
    PURPOSE: make numpy array containing all labels. labels are outlined. 
    FUNCTION: get_outlined_labels(L1_numpy,L2_numpy,L3_numpy)
    INPUT:
        L1_numpy/L2_numpy/L3_numpy:  binary, ndarray   - 3D arrays containing labels. (1) represent outlined area and (0) is bacground.
    OUTPUT:
        labels:                      ndarray           - 3D array where
                                                            (0)   is background,
                                                            (1)   is Label 1,
                                                            (2)   is label 2,
                                                            (3)   is label 3,
                                                            (13)  is overlap between label 1 and 3
                                                            (12)  is overlap between label 1 and 2
                                                            (23)  is overlap between label 2 and 3
                                                            (123) is overlap between label 1,2 and 3
    '''
   
    L1_numpy_c=L1_numpy.copy()
    L2_numpy_c=L2_numpy.copy()
    L3_numpy_c=L3_numpy.copy()


    #L1_numpy_c=np.ceil(L1_numpy_c)
    #L2_numpy_c=np.ceil(L2_numpy_c)
    #L3_numpy_c=np.ceil(L3_numpy_c)


    L1_numpy_c=L1_numpy_c.round()
    L2_numpy_c=L2_numpy_c.round()
    L3_numpy_c=L3_numpy_c.round()
    L1_numpy_c = np.where(L1_numpy_c > 0, 1., L1_numpy_c)
    L2_numpy_c = np.where(L2_numpy_c > 0, 1., L2_numpy_c)
    L3_numpy_c = np.where(L3_numpy_c >0, 1., L3_numpy_c)

    if verbose:
        if (L1_numpy.any()>0 or L2_numpy.any()>0 or L3_numpy.any()>0):
            print('labels exist')
        else:
            print('labels dont exist')


    # Creating 3x3 kernel
    kernel = np.ones((3, 3), np.uint8)
    # erode label area two iteration
    L1_eroded = cv2.erode(L1_numpy_c, kernel,iterations = 2)
    L2_eroded = cv2.erode(L2_numpy_c, kernel,iterations = 2)
    L3_eroded = cv2.erode(L3_numpy_c, kernel,iterations = 2)

 
    # outline label area
    l1_outline=L1_numpy_c-L1_eroded # l1 is represented with number 1.
    l1_outline = np.where(l1_outline == 1, 2, l1_outline) # L1 = 2

    l2_outline=L2_numpy_c-L2_eroded   
    l2_outline = np.where(l2_outline == 1, 3, l2_outline) # L2 = 3
    
    l3_outline=L3_numpy_c-L3_eroded   
    l3_outline = np.where(l3_outline == 1, 4, l3_outline) # L4 = 4

    labels=l2_outline+l1_outline+l3_outline
    labels = np.where(labels == 9, 123, labels)   # L1/L2/L3 overlap = 9
    labels = np.where(labels == 5, 12, labels)    # L1/L2    overlap = 5
    labels = np.where(labels == 6, 13, labels)    # L1/  L3  overlap = 6
    labels = np.where(labels == 7, 23, labels)    #    L2/L3 overlap = 7
    labels = np.where(labels == 2, 1, labels)     # L1               = 2
    labels = np.where(labels == 3, 2, labels)     # L2               = 3
    labels = np.where(labels == 4, 3, labels)     # L3               = 4
    return labels



def get_ROI(numpy_3d):
    '''
    PUPOSE: identify contours in binary image and use area as classifier to identify patient outline.
    FUNCTION: get_ROI(numpy_3d)
    INPUT:
        numpy_3d:            ndarray       -   ct image as 3d array
    OUTPUT:
        width,height:        list, int     -  list with width and height of patient (ROI) for each slice
        numpy_out:           list, int     -  numpy_3d with noise removed fom background
    '''
    mask=numpy_3d.copy()
    numpy_out=numpy_3d.copy()
    # generate the ROI which has 0 for air and 1 for everything else
    threshold = -700
    mask[mask >= threshold] = 1
    mask[mask < threshold] = 0
    
    width=[]
    height=[]

    for i in range(mask.shape[2]):
        # defining the kernel i.e. Structuring element
        kernel = np.ones((15, 15), np.uint8)

        # defining the opening function and apply to masked image
        opening = cv2.morphologyEx(mask[:,:,i], cv2.MORPH_OPEN, kernel)
        dilated=cv2.dilate(opening,kernel,iterations = 2)

        dilated=dilated.astype(np.uint8)
        numpy_out[:,:,i]=numpy_out[:,:,i]*dilated


        cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        x,y,w,h = cv2.boundingRect(cnts[0])

        ROI = dilated[y:y+h, x:x+w]
        width.append(ROI.shape[0])
        height.append(ROI.shape[1])
        

    height=np.amax(height)
    width=np.amax(width)


    return numpy_out,width,height

def crop_numpy(numpy_3d,w,h):
    '''
    PUPOSE: identify contours in binary image and use area as classifier to identify patient outline.
    FUNCTION: crop_numpy(numpy_3d,w,h)
    INPUT:
        numpy_3d:  ndarray       -   3d numpy
        w:         int           -   minimum width of image based on area of maximum structure in numpy
        h:         int           -   minimum height of image based on area of maximum structure in numpy
    OUTPUT:
        numpy_crop: ndarray      -  cropped 3d numpy
    '''
   
    x,y,_=numpy_3d.shape
   
    if w>h:
        s_max=w
    else:
        s_max=h
    ax,ay = (s_max - ((w//2)*2))//2,(s_max - ((h//2)*2))//2

    startx = (x//2 - w//2)-ax
    stopx = (x//2 + w//2)+ax
    starty = (y//2 -h//2)-ay
    stopy = (y//2 + h//2)+ay
    
    numpy_crop=numpy_3d[startx:stopx,starty:stopy,:].copy()

    return numpy_crop

def window_image(image, img_min, img_max):
    '''
    PURPOSE: changing brightness and contrast in image by specifing the minimum and maximum value of the window.
    FUNCTION: window_image(image, img_min, img_max)
    INPUT:
        image:         ndarray       - image
        img_min:       int, float    - min value for window
        img_max:       int, float    - max value for window
    OUTPUT:
        window_image:  ndarray       - windowed image
    '''
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max

    return window_image

def numpy_prep(slices,numpy_input):
    '''
    PURPOSE: process of numpy that is slicing and rotation
    FUNCTION: numpy_prep(slices,numpy_input)
    INPUT:
        slices:   list    - slices to include in output numpy
        numpy_input:   ndarray - 3d array
    OUTPUT:
        numpy:         ndarray  - numpy array including slices specified in slices and rotated
    '''

    numpy=numpy_input[:, :, slices[:]].copy()
    numpy=np.rot90(numpy, k = 1, axes = (0, 1))

    return numpy



def get_slices(d,ct=None,pet=None,labels=None):
    '''
    PURPOSE: generate 3d numpy arrays containing only slices WITH labels
    FUNCTION: get_slices(d,ct,pet,labels)
    INPUT:
          d:         dataframe            - dataframe with column 'idx', 'z' and two columns 'label1' and 'label2' stating whether countour exist in slice z
          ct:        ndarray, (optional)  - 3d numpy array
          pet:       ndarray, (optional)  - 3d numpy array
          labels:    ndarray, (optional)  - 3d numpy array
    OUTPUT
          ct_n:      ndarray              - 3d numpy array only containing slices with contour
          pet_n:     ndarray              - 3d numpy array only containing slices with contour
          labels_n:  ndarray              - 3d numpy array only containing slices with contour
          slice_num: list                 - list with number on slices with countour
    '''
    slice_num=[]
    slice_idx=[]
    pet_n=np.asarray([])
    ct_n=np.asarray([])
    labels_n=np.asarray([])
    for i,r in d.iterrows():
        if (r.label1 or r.label2 or r.label3) is True:
            slice_idx.append(r.idx)
            slice_num.append(r.z)
    if not pet is None:
        pet_n=pet[:,:,slice_idx[:]]
    if not ct is None:
        ct_n=ct[:,:,slice_idx[:]]
    if not labels is None:
        labels_n=labels[:,:,slice_idx[:]]
    return ct_n,pet_n,labels_n,slice_num


def draw_info(path,slices,HU_window,SUV_window,cmap_col,cmap_info):
    '''
    PURPOSE: Draw information on .png. Information includes; slice number, patient ID, max and min values in ct and pet and cmap_info.
             The input path is overwritten with .png file containing text.
    FUNCTION: draw_info(path,slices,HU_window,SUV_window,cmap_col,cmap_info):
    INPUT:
          path:          str               - path to .png file with slices shown side-by-side
          slices    list              - list with slice numbers
          HU_window      list              - HU_window[0] is maximum value and HU_window[1] is minimum value in ct image.
          SUV_window     list              - SUV_window[0] is maximum value and SUV_window[1] is minimum value in pet image.
          cmap_col       ListedColormap    - color of labels. together with cmap_info, cmap_col makes legend for labels
          cmap_info      list, str         - info of labels.  together with cmap_col, cmap_info makes legend for labels
    '''
    

    coords=len(slices)
    if coords <=10:
        cols = coords
    else:
        cols = 10
    rows = int(np.ceil(coords/cols))
    s_fac=10/coords
    
    font_file_abspath = join(dirname(__file__), 'AdventPro-ExtraLight.ttf')
    if isfile(font_file_abspath) is False:
        raise Exception(f"Font dont exist in dir: {dirname(__file__)}")


    font1 = ImageFont.truetype(font_file_abspath,size=int(np.ceil(60+((s_fac)**2))))
    font2 = ImageFont.truetype(font_file_abspath,size=int(np.ceil(100+((s_fac)**2))))
    font3 = ImageFont.truetype(font_file_abspath,size=int(np.ceil(70+((s_fac)**3))))

    cur_im = Image.open(f'{path}.png').convert('RGB') #
    width, height= cur_im.size #
    # adding text to each slice within final image
    a = np.repeat(np.arange(1,rows+1),cols)
    b = np.tile(np.arange(1,cols+1),rows)
    iter_idx = np.vstack((a,b)).T
    #Draw slice number 
    for i,z in enumerate(slices):
        cur_idx = (iter_idx[i,:])
        position1=(cur_idx[1]-1)*width/cols
        position2=(cur_idx[0]-1)*width/cols
        draw = ImageDraw.Draw(cur_im) #
        draw.text((position1, position2), text=(f'z={z}'),font=font3, align ="left", fill="white", width = 60)
    # add space on top of PIL image
    delta=(height//8)
    new_width = width
    new_height = height + delta
    result = Image.new(cur_im.mode, (new_width, new_height))
    result.paste(cur_im, (0, delta))

  
    w2=width//3
    w3=(width//3)*2 
    w4=width

    h2=delta

    draw1 = ImageDraw.Draw(result)
    # Draw cmap_info 
    for i,c in enumerate(cmap_col.colors):
        if i == 0:
            draw1.rectangle( (0,0,w2//6,h2//6), fill=f'{c}' )
            draw1.text((w2//6, 0), text=cmap_info[i],font=font1,fill="white")#label 1
        if i==1:
            draw1.rectangle( (0, h2//3,w2//6,(h2//6)*3), fill=f'{c}' )
            draw1.text((w2//6, h2//3), text=cmap_info[i],font=font1,fill="white") #label 2
        if i==2:
            draw1.rectangle( (0,  (h2//3)*2,w2//6,(h2//6)*5), fill=f'{c}' )
            draw1.text((w2//6, (h2//3)*2), text=cmap_info[i],font=font1,fill="white")#label 3
        if i==3:
            draw1.rectangle( (w2//3,0, (w2//6)*3,h2//6), fill=f'{c}' )
            draw1.text(((w2//6)*3, 0), text=cmap_info[i],font=font1,fill="white")#label 1 and 2 overlap
        if i==4:
            draw1.rectangle( (w2//3, h2//3,(w2//6)*3,(h2//6)*3), fill=f'{c}' )
            draw1.text(((w2//6)*3, h2//3), text=cmap_info[i],font=font1,fill="white")# label 1 and 3 overlap
        if i==5:
            draw1.rectangle( (w2//3,(h2//3)*2,(w2//6)*3,(h2//6)*5), fill=f'{c}' )
            draw1.text(((w2//6)*3, (h2//3)*2), text=cmap_info[i],font=font1,fill="white")#label 2 and 3 overlap
        if i==6:
            draw1.rectangle( ((w2//3)*2,0,(w2//6)*5,h2//6), fill=f'{c}' )
            draw1.text(((w2//6)*5, 0), text=cmap_info[i],font=font1,fill="white",width = 60)#label 1, 2 and 3 overlap
   
    filename = basename(path).split('.')[0]
    draw1.rectangle( (w2+200,0,w3-200,delta), fill="white" )
    draw1.text( ((w2)+220, 0), text=f'{filename}',font=font2,fill="black" )
    
    # Draw information about HU min and max and SUV min and max
    if not HU_window[0].all()==0: 
        draw1.text((w3-50, 0), text="HU",font=font1,fill="white")
        draw1.text((w3-50, h2//3), text=f'Max:{HU_window[0]}',font=font1,fill="white")
        draw1.text((w3-50, (h2//3)*2), text=f'Min:{HU_window[-1]}',font=font1,fill="white")
    if not SUV_window[0].all()==0: 
        SUV_min = float("{0:.2f}".format(SUV_window[-1]))
        SUV_max = float("{0:.2f}".format(SUV_window[0]))
        draw1.text((w3+((w4-w3)//2), 0), text="SUV",font=font1,fill="white")
        draw1.text((w3+((w4-w3)//2), h2//3), text=f'Max:{SUV_max}',font=font1,fill="white") 
        draw1.text((w3+((w4-w3)//2), (h2//3)*2), text=f'Min:{SUV_min}',font=font1,fill="white")

    result.save(f'{path}.png')



def gen_tiled_numpy(numpy_array):
    '''
    PURPOSE: Generate 2D numpy with slices side-by-side.
    FUNCTION: gen_tiled_numpy(numpy_array)
    INPUT:
          numpy_array:   ndarray    - 3d array
    OUTPUT
          numpy_2d:      ndarray    - 2d numpy
    '''
    # specifying number of slices pr row in the output 2d numpy
    coords=np.size(numpy_array,2) # number of slices pr row
    if coords <=10:
        cols = coords
    else:
        cols = 10
    
    rows = int(np.ceil(coords/cols)) # number of rows


    size_x=numpy_array.shape[0]
    size_y=numpy_array.shape[1]

    # set size for output 2d numpy
    numpy_2d=np.zeros((size_x*rows,size_y*cols))

    a = np.repeat(np.arange(1,rows+1),cols)
    b = np.tile(np.arange(1,cols+1),rows)
    iter_idx = np.vstack((a,b)).T
    # iterate over slices in 3d numpy and insert slices in 2d numpy
    for i in range(numpy_array.shape[2]):
        numpy_a= numpy_array[:,:,i]
        cur_im = numpy_a.copy()
        cur_idx = (iter_idx[i,:])
        lower2=(cur_idx[1]-1)*size_x
        upper2=(cur_idx[1])*size_x
        lower1=(cur_idx[0]-1)*size_x
        upper1=(cur_idx[0])*size_x

        numpy_2d[lower1:upper1, lower2:upper2] = cur_im
    return numpy_2d

def gen_cmap(labels,l1_name,l2_name,l3_name):
    '''
    PURPOSE: Generate cmap with unique color for each unique value in labels numpy.
    FUNCTION: gen_cmap(labels)
    INPUT:
        labels:                      ndarray           - 3D array where
                                                            (0)   is background,
                                                            (1)   is Label 1,
                                                            (2)   is label 2,
                                                            (3)   is label 3,
                                                            (13)  is overlap between label 1 and 3
                                                            (12)  is overlap between label 1 and 2
                                                            (23)  is overlap between label 2 and 3
                                                            (123) is overlap between label 1,2 and 3
    OUTPUT
          cmap_col:   ListedColormap    - color of labels. together with cmap_info, cmap_col makes legend for labels
          norm:
          cmap_info:  list, str
    '''
    u = np.unique(labels)
    bounds = np.concatenate(([labels.min()-1], u[:-1]+np.diff(u)/2. ,[labels.max()+1]))
    norm = colors.BoundaryNorm(bounds, len(bounds)-1)
    
    # #use additive color mixing 
    col=list()
    info=list()
    if 1 in labels:
        col.append('#FF00FF') # pink #FF00FF 
        info.append(l1_name)
    if 2 in labels:
        col.append('#00FF00') # green # 
        info.append(l2_name)
    if 3 in labels:
        col.append('#B30838') # red
        info.append(l3_name)
    if 12 in labels:
        col.append('#00FFFF') # blue
        info.append(f'{l1_name}/{l2_name}')
    if 13 in labels:
        col.append('#850C70') # purple
        info.append(f'{l1_name}/{l3_name}')
    if 23 in labels:
        col.append('#FFFF00') # yellow
        info.append(f'{l2_name}/{l3_name}')
    if 123 in labels:
        col.append('white') # white
        info.append(f'{l1_name}/{l2_name}/{l3_name}')
    cmap_col= ListedColormap(col)# 
    cmap_info=info
    return cmap_col,norm,cmap_info




def stack_tiled_numpy(final_path,ct_tile,pet_tile,labels_tile,cmap_col,norm):
    '''
    PURPOSE: stack CT, Pet and labels.
    FUNCTION: stack_tiled_numpy(final_path,ct_tile,pet_tile,labels_tile,cmap_col,norm):
    INPUT:
          final_path:       str                 - directory used to store final png-file
          ct_tile:          ndarray             - 2D ct numpy array
          pet_tile:         ndarray             - 2D pet numpy array
          labels_tile:      ndarray             - 2D labels numpy array
    '''
    fig, axs = plt.subplots(1, 1, figsize=(20, 20))
    axs.set_axis_off()
    axs.imshow(ct_tile,cmap='gray',alpha=1)
    axs.imshow(pet_tile,cmap='hot',alpha=0.4)
    axs.imshow(labels_tile, cmap=cmap_col,norm=norm, alpha = 1)
    fig.savefig(final_path,facecolor='black',bbox_inches='tight',dpi=500)
    return

def visualization(final_path,ct_path=None,pet_path=None,
                  l1_path=None,l1_name='L1',
                  l2_path=None,l2_name='L2',
                  l3_path=None, l3_name='L3',
                  slices=None,cropping=False,all_slices=False,
                  incl_info=True,outline=True,verbose=False):
    '''
    PURPOSE: Visualize labels drawn on ct/pet images. A total of 3 labels can be given as input.
            The final image is a .png file where labels are drawn with following colors: 
                blue    - label 1.
                green   - label 2.
                red     - label 3.
                cyan    - label 1 and 2 overlap.
                magenta - label 1 and 3 overlap.
                yellow  - label 2 and 3 overlap
                white   - label 1, 2 and 3 overlap.
    FUNCTION:
    visualization_optimized(final_path,ct_path,pet_path,l1_path,l1_name,l2_path,l1_name,l3_path,l1_name,slices,cropping,all_slices,incl_info):
    INPUT:
        final_path      str             - full path to where output .png file will be stored, including name of final .png file(.png should not be included).
        ct_path:        str,  (optional)   - Path to .nii file containing ct images from single patient.
        pet_path:       str,  (optional)   - Path to .nii file containing pet images from single patient.
        l1_path:        str,  (optional)   - Path to .nii file containing one set of labels drawn on single patient.
        l1_name:        str,  (optional)   - name of label 1, used for legend when incl_info is True
        l2_path:        str,  (optional)   - Path to .nii file containing one set of labels drawn on single patient.
        l2_name:        str,  (optional)   - name of label 2, used for legend when incl_info is True
        l3_path:        str,  (optional)   - Path to .nii file containing one set of labels drawn on single patient.
        l3_name:        str,  (optional)   - name of label 3, used for legend when incl_info is True
        slices:         bool, (optional)  - list containing slice numbers to be visualized.
        cropping:       bool, (optional)  - if True images are cropped before plotted.
        all_slices:     bool, (optional)  - if False only slices containing labels is plotted.
        incl_info:      bool, (optional)  - if True slice numbers and min and max intensity values are is included in final .png file
        outline:        bool, (optional)  - if False label is shown as filled area.
    '''
    print('generating image...')
    if ct_path is not None:
        ct_nii = nib.load(ct_path)
        ct_numpy = ct_nii.get_fdata()
        [X,Y,Z]=ct_numpy.shape 
    if pet_path is not None:
        pet_nii = nib.load(pet_path)
        pet_numpy = pet_nii.get_fdata()
        [X,Y,Z]=pet_numpy.shape
    if l1_path is not None:
        L1_nii = nib.load(l1_path)
        L1_numpy = L1_nii.get_fdata()
        [X,Y,Z]=L1_numpy.shape  
    if l2_path is not None:
        L2_nii = nib.load(l2_path)
        L2_numpy = L2_nii.get_fdata()
        [X,Y,Z]=L2_numpy.shape
    if l3_path is not None:
        L3_nii = nib.load(l3_path)
        L3_numpy = L3_nii.get_fdata()
        [X,Y,Z]=L3_numpy.shape
    if all(v is None for v in [ct_path, pet_path, l1_path, l2_path, l3_path]):
        raise Exception("At least one input path must be given, that is either a ct, pet or label nifty path must be given.")

    if slices is None:
        if ct_path is not None:
            slices=list(range(0, Z))
        elif pet_path is not None:
            slices=list(range(0, Z))
        elif l1_path is not None:
            slices=list(range(0, Z))
        elif l2_path is not None:
            slices=list(range(0, Z))
        elif l3_path is not None:
            slices=list(range(0, Z))

    if ct_path is None:
        ct_numpy=np.zeros((X,Y,Z), dtype=float)
    if pet_path is None:
        pet_numpy=np.zeros((X,Y,Z), dtype=float)
    if l1_path is None:
        L1_numpy=np.zeros((X,Y,Z), dtype=int)
    if l2_path is None:
        L2_numpy=np.zeros((X,Y,Z), dtype=int)
    if l3_path is None:
        L3_numpy=np.zeros((X,Y,Z), dtype=int)

    
    if outline == False:  
        labels_numpy=get_labels(L1_numpy,L2_numpy,L3_numpy)
    else:
        labels_numpy=get_outlined_labels(L1_numpy,L2_numpy,L3_numpy)


    labels=numpy_prep(slices,labels_numpy) # labels
    ct=numpy_prep(slices,ct_numpy) # CT
    pet=numpy_prep(slices,pet_numpy) # PET

    if (cropping is True):
        if ct_path is not None:
            ct,w,h=get_ROI(ct)
            ct=np.where(ct == -0.0, np.amin(ct), ct)
        elif pet_path is not None:
            pet,w,h=get_ROI(pet)

        ct=crop_numpy(ct,w,h)
        pet=crop_numpy(pet,w,h)
        labels=crop_numpy(labels,w,h)


    if all_slices==False:
        labels_exist=gen_dataframe(labels,slices)
        
        if (sum((labels_exist[['label1', 'label2', 'label3']].sum(axis=1)))) == 0:
             raise Exception("Trying to plot only slices with labels, but labels dont exist!")
        if verbose:
            print(labels_exist)
        ct,pet,labels,slices=get_slices(labels_exist,ct,pet,labels)
    
    #Set window
    HU_min=-135
    HU_max=215
    SUV_min=0.0
    SUV_max=7.0
    if verbose:
        print(f'HU window for ct image is {HU_min}-{HU_max}')
        print(f'SUV window for pet image is {SUV_min}-{SUV_max}')
    pet=window_image(pet, SUV_min, SUV_max)
    ct=window_image(ct, HU_min, HU_max)
    
   
    # generate 2d numpy with slices side-by-side
    ct_tile=gen_tiled_numpy(ct)
    pet_tile=gen_tiled_numpy(pet)
    labels_tile=gen_tiled_numpy(labels)


    if labels_tile.any()>0.0:
        labels_tile=ma.masked_where(labels_tile==0,labels_tile)# mask labels
    if pet_tile.any()>0.0:
        pet_tile=ma.masked_where(pet_tile<0.1,pet_tile)# mask pet
    
    HU_window=[np.amax(ct_tile),np.amin(ct_tile)]
    SUV_window=[np.amax(pet_tile),np.amin(pet_tile)]

    labels_tile=labels_tile.round()
    labels_tile = labels_tile.astype(int)

    cmap_col,norm,cmap_info=gen_cmap(labels_tile,l1_name,l2_name,l3_name)

    stack_tiled_numpy(final_path,ct_tile=ct_tile,pet_tile=pet_tile,labels_tile=labels_tile,cmap_col=cmap_col,norm=norm)
    if incl_info is True:
        draw_info(final_path,slices,HU_window,SUV_window,cmap_col,cmap_info)
 
def Entry_Point():
   
    parser = argparse.ArgumentParser(description='Visualize labels drawn on ct/pet images. A total of 3 labels can be given as input. The final image is a .png file where labels and overlapping labels are drawn with unique colors.')
    parser.add_argument( 'final_path',   type=str,                help='Input path to store final png-file. (.png should not be included in str)')
    parser.add_argument( '-ct_path',     type=str,                help='Input path to ct nii-file')
    parser.add_argument( '-pet_path',    type=str,                help='Input path to pet nii-file')
    parser.add_argument( '-l1_path',     type=str,                help='Input path to label nii-file')
    parser.add_argument( '-l1_name',     type=str,                help='legend name for label 1.______________________________________________________(default: L1)')
    parser.add_argument( '-l2_path',     type=str,                help='Input path to label nii-file')
    parser.add_argument( '-l2_name',     type=str,                help='legend name for label 2.______________________________________________________(default: L2)')
    parser.add_argument( '-l3_path',     type=str,                help='Input path to label nii-file')
    parser.add_argument( '-l3_name',     type=str,                help='legend name for label 3.______________________________________________________(default: L3)')
    parser.add_argument( '-slices',      type=list,               help='Input list with int values of slices to be included.__________________________(default: all slices in nii is used)')
    parser.add_argument( '-cropping',    type=bool,default=False, help='Input (True) to crop image.___________________________________________________(default: (False))')
    parser.add_argument( '-all_slices',  type=bool,default=False, help='Input (True) to visualize all slices, that is both with and without labels.___(default: (False))')
    parser.add_argument( '-incl_info',   type=bool,default=True,  help='Input (False) to exclude information, slice number, legends ect. on image.____(default: (True))')
    parser.add_argument( '-outline',     type=bool,default=True,  help='Input (False) to not outline labels, that is draw labels as solid areas.______(default: (True))')
    parser.add_argument( '-verbose',     type=bool,default=False, help='Input (True) print information while running code.____________________________(default: (False))')
    args = parser.parse_args()
    visualization(args.final_path,args.ct_path,args.pet_path,args.l1_path,args.l1_name,
                    args.l2_path,args.l2_name,
                    args.l3_path,args.l3_name,
                    args.slices,args.cropping,args.all_slices,
                    args.incl_info,args.outline,args.verbose)




if __name__ == '__main__':
    
    final_path=f'/home/fmik/data/figs/HNC03_029_13'
    ct=f'/home/fmik/data/t_l64_doctors/t_l64/images/HNC03_029_0000.nii.gz' #0000
    pet=f'/home/fmik/data/t_l64_doctors/t_l64/images/HNC03_029_0001.nii.gz' #0001
    l1=f'/home/fmik/data/t_l64_doctors/t_l64/labels/md/HNC03_029_md.nii.gz' #md
    l2=None#f'/home/fmik/data/t_l64_doctors/t_l64/labels/ref/HNC03_029_ref.nii.gz' #clinical
    l3=f'/home/fmik/data/t_l64_doctors/t_l64/labels/ref/HNC03_029_ref.nii.gz' #clinical
    z=None#list(range(4, 7))
    visualization(final_path,ct_path=ct,pet_path=pet,
                  l1_path=l1, l1_name='label1',
                  l2_path=l2, l2_name='label2',
                  l3_path=l3, l3_name='label3',
                  slices=z,cropping=False ,all_slices=False,
                  incl_info=True,outline=True,verbose=True)
 
    
    
    
