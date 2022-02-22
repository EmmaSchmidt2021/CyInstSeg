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

# define paths
path = r"C:\Users\UAB\CyInstSeg\Pad 512"
new_path = r"C:\Users\UAB\CyInstSeg\Pad 512"
# determine our final padding size
new_size = 512

#%%   
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

#--- check that functions work as we expect
# if __name__ == "__main__":
#     img = Image.open(r"C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/sequence/CY_101934-3-R22.png")
#     print(img)
#     img = resize_with_padding(img, (new_size, new_size))
#     print(img.size)
#     img.show()
#     newimg = img.save("resized_img.png")
#     print(newimg.size)
#%%
# Create a list of the folders we want to walk through to call later
working_path = path
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
#%%
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
    if num_slice > 99:
        num_width = int((orig_fname[-8:-4]))
        print(num_width)
        num_height = int((orig_fname[-12:-8]))
        print(num_height)
    else:
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
    new_fname = str(pt_numb +'_'+ yr_numb +'_'+ side + '_' + img_type )
    file_name = "%s.npy" %new_fname # add our extension
    print('%s has been padded and renamed %s' %(orig_fname, new_fname))
    np.save(os.path.join(new_path, file_name), resized) # save in the new file folder
    #will need to make new code to add the prefix names an organize into the appropriate folders
    num_slice=0
    num_height=0
    num_width=0


print("complete --- nice job")
    
#%% --check that we can load in arrays and nothing got messed up in the save
#load in .npy arrays 

# e_array = np.load(str(new_path+'/'+file_name))
# e = im.fromarray(e_array[60])
# e

#%%
##______now make into nifti files      
import os


directory_path = r"C:\Users\UAB\CyInstSeg\Pad 512"
npy_files = []

for root, dirs, files in os.walk(os.path.normpath(directory_path), topdown=True):
    for name in files:
        npy_files.append(name)
        
#%%

import nibabel as nib
import numpy as np

for i in range(len(npy_files)): 
    filename = npy_files[i]
    data = np.load(filename)
    data = np.arange(512*512*96).reshape(512,512,96)
    new_image = nib.Nifti1Image(data, affine=np.eye(4))
    nib.save(new_image, "%s.nii" %filename)
    
#%% check nifi file kept shape the same
img = nib.load("MR_101934_0_L.npy.nii")
img.shape
img.data

            
