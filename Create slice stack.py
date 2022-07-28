# -*- coding: utf-8 -*-
"""
Created on Mon May 30 12:00:31 2022

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


def read_nifti_file(path):
    nifti_image = nib.load(path)
    nib_data = nifti_image.get_fdata()
    return nib_data
def retrieve_images_and_segmentations(data_path, images, segmentations, size=(512,512)):
  x = []
  y = []
  for i in range(len(images)):
    seg = read_nifti_file(data_path+segmentations[i])
    img = read_nifti_file(data_path+images[i])
    assert img.shape == seg.shape
    seg = resize(seg,(size[0], size[1], seg.shape[-1]))
    print(size[0], size[1], seg.shape[-1])
    img = resize(img,(size[0], size[1], img.shape[-1]))
    for j in range(seg.shape[-1]):
      # ignore slices that don't have a segmentation
      if np.sum(seg[:,:,j]) == 0:
        continue
      x.append(img[:,:,j])
      y.append(seg[:,:,j])
  x = np.array(x)[:,:,:,np.newaxis]
  y = np.array(y)[:,:,:,np.newaxis]

  # randomly shuffle slices
  m = x.shape[0]
  order = np.random.permutation(m)

  return x[order], y[order]
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

indices = np.array(range(len(images)))

#%%
images = np.array(images[0:20])
segmentations = np.array(segmentations[0:20])
indices = np.array(range(len(images)))
train, test = train_test_split(indices, test_size=0.25) # TODO: split indices into training and test partitions
path = (data_path+'\\'+images[train][0])
nifti_image = nib.load(path)
nifti_data = nifti_image.get_fdata()
nifti_slice = nifti_data[:,:,50]
plt.imshow(nifti_slice, cmap='gray')
plt.title('Opened Nifti File')
plt.show()
train, valid = train_test_split(train, test_size=0.25)
example_image = read_nifti_file(data_path+'\\'+images[train][0]) # TODO: read in the first image from the training partition
example_segmentation = read_nifti_file(data_path+'\\'+segmentations[train][0])  # TODO: read in the first segmentation from the training partition

print(example_image.shape, example_segmentation.shape)

x_train, y_train = retrieve_images_and_segmentations(data_path, images[train], segmentations[train]) #TODO: get the matrices for the training partition
print(x_train.shape, y_train.shape)