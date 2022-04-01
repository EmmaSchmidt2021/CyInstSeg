# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 07:27:25 2022

@author: emmasch
"""

from PIL import Image as im
from PIL import ImageOps
import numpy as np
import os
import fnmatch
import nibabel as nib


working_path = r"C:\Users\emmasch\data"
new_path = r"C:\Users\emmasch\data\NPY"
# determine our final padding size
new_size = 250

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
#%%
pt_fnames=[]
for root, dirs, files in os.walk(os.path.normpath(working_path), topdown=True):
    for name in files:
        pt_fnames.append(os.path.join(root, name))
  print('\nPatient Folders have been identified\n')

ROI_list = []
for i in range(len(pt_fnames)):
    ROI_name = 'ROI'
    filename = os.path.basename(pt_fnames[i])
    if ROI_name in filename:
        ROI_list.append(pt_fnames[i])
  print('\nFilenames have been found and added\n')

#%%
call_file = str(ROI_list[3])
print(call_file)
num_slice = 96
num_width = 221
num_height = 125
with open(r'%s' %call_file, 'rb') as file: #read in raw uint8 and resize correctly
    data = np.fromfile(file, dtype = 'uint8').reshape(96,221,125)

import matplotlib.pyplot as plt
display_slice = im.fromarray(data[15,:,:])
plt.imshow(display_slice, cmap='gray')
#%%
 resized = np.zeros((num_slice,new_size,new_size), dtype ='uint8')
with open(r'%s' %call_file, 'rb') as file: #read in raw uint8 and resize correctly
     data = np.fromfile(file, dtype = 'uint8').reshape(num_slice,num_width,num_height)
     for j in range(num_slice):
         orig_slice = data[j]
         re_slice = im.fromarray(orig_slice)
         resized[j] = resize_with_padding(re_slice, (new_size, new_size))

resize_slice = im.fromarray(resized[15,:,:])
plt.imshow(resize_slice, cmap='gray')
#%%
pt_numb = str('0')
yr_numb = str('0')
side=str('0')
img_type = 'MR'
new_fname = str(pt_numb +'_'+ yr_numb +'_'+ str(num_slice) +'_'+ side + '_' +  img_type )
file_name = "%s" %new_fname # add our extension
np.save(os.path.join(new_path, file_name), resized)
#%%

filename = r"C:\Users\emmasch\data\NPY\0_0_96_0_MR.npy"
e_array = np.load(filename)
print(e_array.shape)
e = im.fromarray(e_array[15,:,:])
plt.imshow(e, cmap='gray')

#%%

#%%
print('Converting', str(len(ROI_list)), 'files')
for i in range(len(ROI_list)): # loop through all the available files from the list that had our keyword
    orig_fname = os.path.basename(ROI_list[i])# grab the ith filename in the list
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
        img_type = 'K'
    elif 'Image' in orig_fname:
        img_type = 'M'
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
    new_fname = str(pt_numb +'_'+ yr_numb +'_'+ str(num_slice) +'_'+ side + '_' +  img_type )
    file_name = "%s.npy" %new_fname # add our extension
    print('%s has been padded and renamed %s' %(orig_fname, new_fname))
    np.save(os.path.join(new_path, file_name), resized) # save in the new file folder
    #will need to make new code to add the prefix names an organize into the appropriate folders
    num_slice=0
    num_height=0
    num_width=0


print("complete --- nice job")