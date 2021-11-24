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
path = "C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Pt 101934/dciacj"
new_path ="C:/Users/emmasch/CystInstance/InstanceCystSeg-master/data/Resized"
# determine our final padding size
new_size = 250

# create two functions - one to determine the appropriate size, and one to pad
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
# define the phrase we are searching through the folder for
# generate a list of the files we want to edit
ROI_name = 'ROI'  
ROI_list = [] #generate a blank list to fill in
for fname in os.listdir(path):
    if ROI_name in fname:
        ROI_list.append(fname)

#%%
# loop through our generated list and resize, saving in our new path
resized = np.zeros((num_slice,new_size,new_size), dtype ='uint8') #preallocate array
for i in range(len(ROI_list)): # loop through all the available files from the list that had our keyword
    orig_fname = ROI_list[i] # grab the ith filename in the list
    #find the dimmensions from the filename
    num_slice = int(orig_fname[-2:])
    num_width = int((orig_fname[-7:-3]))
    num_height = int((orig_fname[-11:-7]))
    call_file = str(path+'/'+orig_fname) #define our filename with path to open
    
    with open(r'%s' %call_file, 'rb') as file: #read in raw uint8 and resize correctly
         data = np.fromfile(file, dtype = 'uint8').reshape(num_slice,num_width,num_height)
         for i in range(num_slice):
             orig_slice = data[i]
             re_slice = im.fromarray(orig_slice)
             resized[i] = resize_with_padding(re_slice, (new_size, new_size))
             # now we need to rename this resized array and save it as a .npy
    new_fname = str('%s' %orig_fname + '_RESIZED_') #keep the original name for now 
    file_name = "%s.npy" %new_fname # add our extension
    np.save(os.path.join(new_path, file_name), resized) # save in the new file folder
#%% --check that we can load in arrays and nothing got messed up in the save
#load in .npy arrays 

e_array = np.load(str(new_path+'/'+file_name))
e = im.fromarray(e_array[60])
e


#%%
##______now make into nifti files            
         
    %step 1: get the names of the files
            files=dir('*.png');
            file_names={files.name}';

    %step 2: sort the files

            %extract the numbers
            %Here, the format of the name shoul be enterd and %d should replate the
            %number, this is so that the files will be load in the right order
              filenum = cellfun(@(x)sscanf(x,'%d.png'), file_names);
            % sort them, and get the sorting order
              [~,Sidx] = sort(filenum) ;
            % use to this sorting order to sort the filenames
              SortedFilenames = file_names(Sidx);

   %step 3: combine images to single matrix:
            %get number of files
            num_of_files=numel(SortedFilenames);
            for i=1:num_of_files
                nifti_mat(:,:,i)=imread(SortedFilenames{i});
            end
  %step 4: conver to nifti and save:
            filename='here_goes_the_name_of_the_file';
            niftiwrite(nifti_mat,filename);
