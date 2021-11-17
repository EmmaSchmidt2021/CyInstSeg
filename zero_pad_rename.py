# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:45:07 2021

@author: emmasch
"""
# way to display uint8 image:
from PIL import Image, ImageOps
import numpy as np
import os
import glob

# check ability to load in filepath, image, and array
im = Image.open(r"C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/CYR/CY_101934-3-R02.png")
imarray = np.array(Image.open(r"C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/101934 y0 t3.tif"))

#check out sizing 
print(type(im))
print(type(imarray))
# <class 'numpy.ndarray'>

print(imarray.dtype)
# uint16

print(imarray.shape)
print(im.size)
# (225, 400, 3)


# define path
im_path = "C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/sequence"

#_______________determine new size____________________
new_size = 350

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

#---- only run this when checking the initial resize
# if __name__ == "__main__":
#     img = Image.open(r"C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/sequence/CY_101934-3-R22.png")
#     print(img)
#     img = resize_with_padding(img, (new_size, new_size))
#     print(img.size)
#     img.show()
#     newimg = img.save("resized_img.png")
#     print(newimg.size)

# read uint8 into numpy array
import numpy as np
from keras.preprocessing.image import array_to_img

with open('101934 y0 t3 Cyst ROI Left 8bit 137 178 96', "rb") as infile:
    data = np.fromfile(infile, dtype = 'uint8').reshape(137,178,96)
    single_slice = data[:,:,15]
    b=array_to_img(single_slice)
b

#use glob to create a batch of images out of all the files in our current directory
# if errors - change working directory in spyder itself

images = glob.glob(im_path, "*.png")
for image in images:
    img = Image.open(image)
    img = resize_with_padding(img, (new_size, new_size))
    #move to this new folder
    #filename = 
    #os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save("C:/Users/emmasch/CystInstance/InstanceCystSeg-master/src/data/Pt 101934/dciaca/CYR/"+image)



    
    
    
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
