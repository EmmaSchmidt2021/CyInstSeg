# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:45:07 2021

@author: emmasch
"""
# load in the ImageJ raw format 
# size of the cropped image and main subject is located in the title
# extract sizing, zero pad all images, rename, and save as .npy files that can then be converted into nifti

# load in libraries
from PIL import Image as im
from PIL import ImageOps
import numpy as np
import os
import fnmatch
import nibabel as nib

# define paths and final padding size
raw_path = r'C:\Users\UAB\Kidney-Segmentation-Jupyter\Unconverted Images'
new_path = r'C:\Users\UAB\Kidney-Segmentation-Jupyter\Unconverted Images\NPY'
final_path = r'C:\Users\UAB\Kidney-Segmentation-Jupyter\AllTrainingImages'
new_size = 512

# create two functions - one to determine the appropriate size, and one to pad

# figure out difference that needs to be made up in rows/columns
def padding(img, expected_size):
    desired_size = expected_size
    delta_width = desired_size - img.size[0]
    delta_height = desired_size - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

#after calculating the padding, add in the padding to rows and columns to meet new expected size
def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

# Create a list of the folders we want to walk through to call later
working_path = raw_path
patient_folders = []
pt_fnames = []

import os
for root, dirs, files in os.walk(os.path.normpath(working_path), topdown=True):
    for name in files:
        #print(os.path.join(root, name))
        pt_fnames.append(os.path.join(root, name))
print('\nPatient Folders have been identified\n')
#sort through and get only the files with ROI in them
#this eliminates the tiff and 3D files 
ROI_list = []
for j in range(len(pt_fnames)):
    ROI_name = 'ROI'
    filename = os.path.basename(pt_fnames[j])
    if ROI_name in filename:
        ROI_list.append(pt_fnames[j])
print('\nFilenames have been found and added\n')

   
#%%
# loop through our generated list and resize, saving the new image in our output path

 #preallocate array
for i in range(len(ROI_list)): # loop through all the available files from the list that had our keyword
    orig_fname = os.path.basename(ROI_list[i])# grab the ith filename in the list
    #extract information from the filename
    num_slice = int(orig_fname[-2:])
    print(num_slice)
    if num_slice < 50:
        print('over 99')
        num_slice = int(orig_fname[-3:])
        num_width = int((orig_fname[-8:-4]))
        print(num_width)
        num_height = int((orig_fname[-12:-8]))
        print(num_height)
    else:
        print('less than 99')
        num_width = int((orig_fname[-7:-3]))
        print(num_width)
        num_height = int((orig_fname[-11:-7]))
        print(num_height)
    pt_numb =(orig_fname[0:6])
    yr_numb = (orig_fname[8])
    if 'Cyst' in orig_fname:
        img_type = 'CY'
    elif 'Kidney' in orig_fname:
        img_type = 'K'
    elif 'Image' in orig_fname:
        img_type = 'MR'
    if 'Right' in orig_fname:
        side = 'R'
    elif 'Left' in orig_fname:
        side = 'L'
    call_file = str(ROI_list[i]) #define our filename with path to open (working_path+'/'+orig_fname)
    resized = np.zeros((num_slice,new_size,new_size), dtype ='uint8')
    with open(r'%s' %call_file, 'rb') as file: #read in raw uint8 and resize correctly
         data = np.fromfile(file, dtype = 'uint8').reshape(num_slice,num_width,num_height)
         for j in range(num_slice):
             orig_slice = data[j]
             re_slice = im.fromarray(orig_slice)
             resized[j] = resize_with_padding(re_slice, (new_size, new_size))
             # now we need to rename this resized array and save it as a .npy
    #new_fname = str('%s' %orig_fname + '_RESIZED_') #keep the original name for now 
    new_fname = str(pt_numb +'_'+ yr_numb +'_'+ str(num_slice) +'_' + side + '_' + img_type )
    file_name = "%s.npy" %new_fname # add our extension
    print('%s has been padded and renamed %s' %(orig_fname, new_fname))
    np.save(os.path.join(new_path, file_name), resized) # save in the new file folder
    #will need to make new code to add the prefix names an organize into the appropriate folders
    #num_slice=0
    #num_height=0
    #num_width=0
    


print("complete --- nice job")
    
#%% --check that we can load in arrays and nothing got messed up in the save
#load in .npy arrays 
from PIL import Image as im
from PIL import ImageOps
import numpy as np
new_path = r'C:\Users\UAB\Pad 512\orig npy'
filename = r'C:/Users/UAB/Pad 512/orig npy/101934_0_L_MR.npy'
#e_array = np.load(str(new_path+'/'+file_name))
e_array = np.load(filename)
e = im.fromarray(e_array[60])
plt.imshow(e, cmap='gray')

#%%
##______now make into nifti files      
import os


directory_path = r"C:\Users\UAB\Kidney-Segmentation-Jupyter\Unconverted Images\NPY"
npy_files = []

for root, dirs, files in os.walk(os.path.normpath(directory_path), topdown=True):
    for name in files:
        npy_files.append(os.path.join(root, name))

#%%

import nibabel as nib
import numpy as np

for i in range(len(npy_files)): 
    filename = npy_files[i]
    data = np.load(filename)
    data = np.arange(512*512*96).reshape(512,512,96)
    new_image = nib.Nifti1Image(data, affine=np.eye(4))
    nib.save(new_image, "%s.nii" %filename[:-4])
    
#%% check nifi file kept shape the same

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
img = nib.load(r"C:\Users\UAB\Kidney-Segmentation-Jupyter\AllTrainingImages\101934_0_96_L_K.nii")
img.shape
imgOG_data = img.get_fdata()
print(type(imgOG_data))
print(imgOG_data.shape)
print(imgOG_data)
mid_slice_x = imgOG_data[:,:,50]
print(mid_slice_x.shape)
plt.imshow(mid_slice_x.T, cmap='gray')


# img = nib.load("MR_101934_0_L.npy.nii")
# img.shape
# img.data

#%%
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import tiffile as tiff
from tifffile import imread, imwrite
im = io.imread('C:/Users/schmi/CyInstSeg/Resized/Training/TIFF/101934 y0 t3.tif')
print(im.shape)     


test_image = im[10]
plt.imshow(test_image, cmap='gray')
print('original tiff image shape:', test_image.shape)

enlarge_img= resize(test_image, (512,512))
plt.imshow(enlarge_img, cmap="gray")


resized_tiff = resize(im, (32,512,512))
resized_test = resized_tiff[15]
plt.imshow(resized_test, cmap='gray')
tiff.imsave('101934 y0 t3_RESIZED.tif', resized_tiff)
#%% 
new_img_tiff = io.imread("./101934 y0 t3_RESIZED.tif")
new_img_tiff_test = new_img_tiff[5]
plt.imshow(new_img_tiff_test, cmap='gray')
print(new_img_tiff.shape)
#%% Convert and resize TIFF

from imio import load, save
import nibabel as nib
import numpy as np
img = load.load_any(r"C:\Users\UAB\Pad 512\101934 y0 t3 binary.tif")
#img2 = np.load(r"C:\Users\UAB\Pad 512\orig npy\101934_0_L_K.npy")
img.shape
imgSM = img[10:14,:,:]
save.to_nii(imgSM, r"C:\Users\UAB\Pad 512\orig npy\101934 y0 t3_4slice_K.nii")

test_load = nib.load( r"C:\Users\UAB\Pad 512\orig npy\101934 y0 t3_4slice_K.nii").get_fdata()
test_load.shape
import matplotlib.pyplot as plt
test3 = test_load[0,:,:]
plt.imshow(test_load, cmap='gray')

from skimage import io
from skimage.transform import resize
enlarge_img= resize(test_load, (4,512,512))
enlarge_img1 = enlarge_img[0,:,:]
plt.imshow(enlarge_img1, cmap="gray")

enlarge_stack = resize(test_load3, (5,512,512))
plt.imshow(enlarge_stack[2,:,:], cmap="gray")
save.to_nii(enlarge_stack, r"C:\Users\UAB\Pad 512\101934 y0 t3_5slice_K.nii")
save.to_nii(enlarge_img, r"C:\Users\UAB\Pad 512\101934 y0 t3_4slice_512_K.nii")
#%%
#%%
  import tensorflow as tf

  gpus = tf.config.list_physical_devices('GPU')
  if gpus:
      try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
          tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
      except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
#%%
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

#%%

filename= '101934_0_106_L_K.npy'

print(filename[-10:-8])

slices= int(filename[-10:-8])

if slices < 50:
    slices = int(filename[-11:-8])
    #print('number of slices', slices)
else:
    slices = int(filename[-11:-9])
    #print('number of slices', slices)
#%%

for i in range(len(npy_files)): 
    filename = npy_files[i]
    data = np.load(filename)
    num_slice = int(filename[-11:-9])
    print(num_slice)
    if num_slice < 50:
        num_slice = int(filename[-12:-9])
        #print('number of slices', slices)
    else:
        num_slice = num_slice
    data = np.arange(new_size*new_size*num_slice).reshape(new_size,new_size,num_slice)
    new_image = nib.Nifti1Image(data, affine=np.eye(4))
    nib.save(new_image, os.path.join(final_path, "%s.nii" %filename[:-4])
#%%
import os
import shutil
path = r'C:\Users\UAB\Kidney-Segmentation-Jupyter\AllTrainingImages'
cyst_names=[]
for root, dirs, files in os.walk(os.path.normpath(path), topdown=True):
    for name in files:
        #print(os.path.join(root, name))
        cyst_names.append(os.path.join(root, name))

C_list = []
for j in range(len(cyst_names)):
    C_name = '_C'
    filename = os.path.basename(cyst_names[j])
    if C_name in filename:
        C_list.append(cyst_names[j])

cyst_path = r"C:\Users\UAB\Kidney-Segmentation-Jupyter\Unconverted Images\CystNII"
for i in range(len(C_list)):
    shutil.move(C_list[i],cyst_path )