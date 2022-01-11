# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:43:06 2021

@author: emmasch
"""

#define padding functions

#get list of files in directory that we will loop over
import glob
import os
import fnmatch

path = "C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Pt 101934"
    
#define loop that will pull size information out of the title as well as the 
#prefix we need to add

# def list_files(path, pattern):
#     paths=[]
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if fnmatch.fnmatch(file, pattern):
#                 paths.append(os.path.join(root, file))  
#     return(paths)

# file_list = list_files(path, "Cyst")

paths =[]
for root, dirs, files in os.walk(path):
    print (root, files)
    for file in files:
        if fnmatch.fnmatch(file,"Cyst"):
            paths.append(os.path.join(root, file))
#return(paths)

# my_files_list = list_files(paths, fnmatch.fnmatch(file, "Cyst"))



path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/small
for root,_, filenames in os.walk(path):
    print(root, filenames)
    for filenames in fnmatch.filter(filenames, "Cyst Left"):
        new_filename = os.path.join(root, filenames)
        if os.access(new_filename, os.R_OK):
            print('%s is here')
filenames[1]

# pattern = "101934 y0 t3 Image ROI Left 8bit 137 178 96"

# new = fnmatch.filter(os.listdir(path), pattern)
#pull in the image, cycle through each slice and resize with padding code
# savr into a new array with image name 

example_string = "Hello world Cyst"
if "Cyst" in example_string:
    print('Yes it works')
else: 
    print('nah fam that aint right')
    
#%%



# import fnmatch
# import os

# path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Small/Pt 101934/dciaca'
# matches=[]
# pt_fnames =[]
# for root, dirs, filenames, in os.walk(path):
#     for name in filenames:
#         matches.append(os.path.join(root, name))
#         print(matches)


# rootdir = path
# for rootdir, dir, files in os.walk(os.path.normpath(rootdir),topdown=True):
#     for file in files:
#         full_path = os.path.join(rootdir, file)
#         print(full_path)




# test_path = pt_path
# print(test_path)


# ROI_list = [] #generate a blank list to fill in
# for i in range(len(pt_fnames)):        
#     ROI_name = 'ROI'  
#     pt_path = str(r'%s' %pt_fnames[i]) 
#     for fname in os.listdir(pt_path):
#         if ROI_name in fname:
#             ROI_list.append(fname)

# for i in range(len(pt_fnames)):
#     ROI_name = 'ROI'
#     if ROI_name in pt_fname[i]:
#         ROI_list.append(pt_fname)

# ROI_name = 'ROI'  
# ROI_list = [] #generate a blank list to fill in
# for fname in os.listdir(path):
#     if ROI_name in fname:
#         ROI_list.append(fname)


#%%

#%%
# Create a list of the folders we want to walk through to call later
working_path = "C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Small"
patient_folders = []
pt_fnames = []

import os
for root, dirs, files in os.walk(os.path.normpath(working_path), topdown=True):
    # for name in files:
    #     print(os.path.join(root, name))
    #     pt_fnames.append(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
        patient_folders.append(os.path.join(root, name))
print('\nPatient Folders have been identified\n')


ROI_name = 'ROI'  
ROI_list = [] #generate a blank list to fill in
for i in range(len(patient_folders)):
    path_sort = patient_folders[i]
    for fname in os.listdir(path_sort):
        if ROI_name in fname:
            ROI_list.append(fname)



filename = os.path.basename(pt_fnames[1])
print(filename)




    orig_fname = os.path.basename(ROI_list[2])# grab the ith filename in the list
    #extract information from the filename
    print(orig_fname)
    num_slice = int(orig_fname[-2:])
    print(num_slice)
    num_width = int((orig_fname[-7:-3]))
    num_height = int((orig_fname[-11:-7]))
    pt_numb =(orig_fname[0:6])
    yr_numb = (orig_fname[8])
    print(pt_numb, yr_numb)

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
        
    new_name = str(img_type +'_' + pt_numb +'_'+ yr_numb +'_'+ side)
    print(new_name)






#%%
# CY_list = []
# K_list = []
# MR_list = []
# for i in range(len(ROI_list)):
#     Cyst = 'Cyst'
#     Kidney = 'Kidney'
#     MR = 'Image'
#     fname = ROI_list[i]
#     if Cyst in fname:
#            CY_list.append(fname)
#     elif Kidney in fname:
#            K_list.append(fname)
#     elif MR in fname:
#          MR_list.append(fname)
#%%
# here we need to filter that ROI list into separate lists for kiney, cyst, and original
# use these lists to rename with the proper prefix
     #%%
# define the phrase we are searching through the folder for
# generate a list of the files we want to edit


# ROI_name = 'ROI'  
# ROI_list = [] #generate a blank list to fill in
# for fname in os.listdir(path):
#     if ROI_name in fname:
#         ROI_list.append(fname)


# ROI_list = [] #generate a blank list to fill in
# for i in range(len(pt_fnames)):        
#     ROI_name = 'ROI'  
#     pt_path = str(r'%s' %pt_fnames[i]) 
#     for fname in os.listdir(pt_path):
#         if ROI_name in fname:
#   
#%% Gather all .tiff files into a single directory

import glob, os
import shutil, sys

direct_path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/KU'
new_path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/TIFF'


for root, dirs, files in os.walk(os.path.normpath(direct_path), topdown=True):
    for name in files:
        if name.endswith('.tif'):
            shutil.copyfile(os.path.join(root, name), os.path.join(new_path,name))
print("**complete**")


#%% move files 

original_path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Resized'
image_path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Resized/MRimg'
segment_path = 'C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Resized/Segment'


for root, dirs, files in os.walk(os.path.normpath(original_path), topdown=True):
    for name in files:
        if name.startswith('MR'):
            shutil.move(os.path.join(root, name), os.path.join(image_path,name))
print("**complete**")

for root, dirs, files in os.walk(os.path.normpath(original_path), topdown=True):
    for name in files:
        if name.startswith(("CY", "K")):
            shutil.move(os.path.join(root, name), os.path.join(segment_path,name))
print("**complete**")


