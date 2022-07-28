# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 12:01:07 2022

@author: UAB
"""

import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import matplotlib.pyplot as plt
from skimage import measure
from skimage.transform import resize
from keras_unet.metrics import dice_coef
from keras_unet.models import custom_unet
from keras_unet.losses import jaccard_distance
from sklearn.model_selection import train_test_split
from PIL import Image
from PIL import ImageOps
import fnmatch
import nibabel as nib
import shutil


raw_path = r'C:\Users\UAB\data\KU'
new_path = r'C:\Users\UAB\data\AllNPY'
final_path = r'C:\Users\UAB\data\NII_Binarized'
new_size = 512

#%%

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




patient_folders = []
pt_fnames = []

import os
for root, dirs, files in os.walk(os.path.normpath(raw_path), topdown=True):
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
print('Converting', str(len(ROI_list)), 'files')
for i in range(len(ROI_list)): # loop through all the available files from the list that had our keyword
    orig_fname = os.path.basename(ROI_list[i])# grab the ith filename in the list
    print(orig_fname)
    #extract information from the filename
    num_slice = int(orig_fname[-2:])
    #print(num_slice)
    if num_slice < 50:
        #print('over 99')
        num_slice = int(orig_fname[-3:])
        num_width = int((orig_fname[-8:-4]))
        #print(num_width)
        num_height = int((orig_fname[-12:-8]))
        #print(num_height)
    else:
        #print('less than 99')
        num_width = int((orig_fname[-7:-3]))
        #print(num_width)
        num_height = int((orig_fname[-11:-7]))
        #print(num_height)
    pt_numb =(orig_fname[0:6])
    yr_numb = (orig_fname[8])
    if 'Cyst' in orig_fname:
        img_type = 'C'
    elif 'Kidney' in orig_fname:
        img_type = 'M_K'
    elif 'Image' in orig_fname:
        img_type = 'M'
    if 'Right' in orig_fname:
        side = 'R'
    elif 'Left' in orig_fname:
        side = 'L'
    call_file = str(ROI_list[i]) #define our filename with path to open (working_path+'/'+orig_fname)
    resized = np.zeros((num_slice,new_size,new_size), dtype ='uint8')
    transposed = np.zeros((new_size, new_size, num_slice), dtype='uint8')
    with open(r'%s' %call_file, 'rb') as file: #read in raw uint8 and resize correctly
         data = np.fromfile(file, dtype = 'uint8').reshape(num_slice,num_width,num_height)
         for j in range(num_slice):
             orig_slice = data[j]
             re_slice = Image.fromarray(orig_slice)
             resized[j] = resize_with_padding(re_slice, (new_size, new_size))
         for i in range(resized.shape[0]):
             old_slice = resized[i,:,:]
             transposed[:,:,i] = old_slice
             
             # now we need to rename this resized array and save it as a .npy
    #new_fname = str('%s' %orig_fname + '_RESIZED_') #keep the original name for now 
    new_fname = str(pt_numb +'_'+ yr_numb +'_'+ str(num_slice) +'_'+ side + '_' +  img_type )
    file_name = "%s" %new_fname # add our extension
    np.save(os.path.join(new_path, file_name), transposed) # save in the new file folder
    converted_array = np.array(transposed, dtype=np.float32)
    affine = np.eye(4)
    nifti_file = nib.Nifti1Image(converted_array, affine)
    nib.save(nifti_file, os.path.join(final_path, "%s" %new_fname))


print("complete --- nice job")
#%%
path = r'C:\Users\UAB\data\512_AllNII\\'
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

cyst_path = r"C:\Users\UAB\data\512_Cyst"
#cyst_path = r"C:\Users\schmi\data\NPY Cyst"
for i in range(len(C_list)):
    shutil.move(C_list[i],cyst_path )
#%%
data_path = r'C:\Users\UAB\data\512_AllNII\\'
images = []
segmentations = []
for f in os.listdir(data_path):
  if '_K' in f:
    continue
  else:
    images.append(f)
    segmentations.append(f.replace('.nii', '_K.nii'))

print(images[0], segmentations[0])
images = np.array(images)
segmentations = np.array(segmentations)

indices = np.array(range(len(images))) # we will use this in the next step.
#%%
import os
def gather_set(data_path, phrase):
    set_of = []
    path = data_path + '\\'
    for f in os.listdir(data_path):
      if phrase in f:
        set_of.append(f)
      else:
        continue
    #set_of = np.array(set_of)

    indices = np.array(range(len(set_of))) # we will use this in the next step.

    return set_of

data_path = r'C:\Users\UAB\data\512_AllNII'
final_path = r'C:\Users\UAB\data\NII_Binarized'
kidney_non = gather_set(data_path, '_K')


seg_list=kidney_non
for i in range(len(seg_list)):
    segment = nib.load(data_path+"\\"+seg_list[i])
    seg_data = segment.get_fdata()
    binarized = np.where(seg_data>1,1,seg_data)
    affine = np.eye(4)
    nifti_file = nib.Nifti1Image(binarized, affine)
    nib.save(nifti_file, os.path.join(final_path, "%s" %seg_list[i]))
    

#%%
src = r'C:\Users\UAB\data\512_AllNII'
trg = r'C:\Users\UAB\data\NII_Binarized'
mr_set = gather_set(src, "_M.nii")

for i in range(len(mr_set)):
    shutil.copy2(os.path.join(src, mr_set[i]),trg)