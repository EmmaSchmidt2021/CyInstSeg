# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 07:22:37 2021

@author: emmasch
"""
resized = np.zeros((num_slice,new_size,new_size), dtype ='uint8')


for i in range(num_slice):
             orig_slice = data[i]
             re_slice = im.fromarray(orig_slice)
             resized[i] = resize_with_padding(re_slice, (new_size, new_size))
             

d = im.fromarray((resized * 255).astype(np.uint8))
d



np.save("b.npy", np.array(resized))

b_array = np.load("b.npy")

b_slice = im.fromarray(b_array[45])
b_slice

orig_fname = 'e'
new_fname = str('%s' %orig_fname + '_RESIZE_')
new_fname
file_name = "%s.npy" %new_fname
file_name
np.save(os.path.join(new_path, file_name), resized)


e_array = np.load(str(new_path+'/'+file_name))

e = im.fromarray(e_array[60])
e


#ensure our function is working correctly and that the new string doesnt look funny
# ROI_list[4]
# calling_ROI_img1 = str(path+'/'+ROI_list[4])
# print(calling_ROI_img1)
# #make sure that string looks right
# print(r'%s' %calling_img_1)

# #block to search for the size in the filename
# working_filename = ROI_list[4]
# num_slice = int(working_filename[-2:])
# num_width = int((working_filename[-7:-3]))
# num_height = int((working_filename[-11:-7]))


# open the file and resize that particular slice
#%% 
working_path = "C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/small"
patient_folders = []
pt_fnames = []

import os
for root, dirs, files in os.walk(".", topdown=False):
    # for name in files:
    #     print(os.path.join(root, name))
    #     pt_fnames.append(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
        patient_folders.append(os.path.join(root, name))
        
        
ROI_list = [] #generate a blank list to fill in
for i in range(len(patient_folders)):        
    ROI_name = 'ROI'  

    pt_path = patient_folders[i]
    for fname in os.listdir(pt_path):
        if ROI_name in fname:
            ROI_list.append(fname)
        




#%%
pt_path = patient_folders[4]
pt_path
    ROI_name = 'ROI'  
    ROI_list = [] #generate a blank list to fill in
    pt_path = patient_folders[i]
    for fname in os.listdir(pt_path):
        if ROI_name in fname:
            ROI_list.append(fname)




#%%

filename = 'MR_101934_0_L.npy'
			img = np.load(input_folder+'/'+image_folder+'/'+filename)
			#data = img.get_data()

			#pre-process
			data=np.asarray(img).astype(np.float32)
			data = data/np.percentile(data,99) * 255
			data[data>255] = 255
			


import nibabel as nib
import numpy as np
from PIL import Image as im
from PIL import ImageOps
print(img.shape)
print(data.shape)

data = np.asarray(img).astype(np.float32)

e = im.fromarray(data[60])
e = e.convert("L")
e




