# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:50:56 2022

@author: UAB
"""

#look at prediction
#https://lukas-snoek.com/NI-edu/fMRI-introduction/week_1/python_for_mri.html

import numpy as np
from PIL import Image as img
import matplotlib.pyplot as plt
import nibabel as nib

imgM = nib.load(r"C:\Users\UAB\Successful Predictions and new images\105005_0_84_L_M.nii")
imgK = nib.load(r"C:\Users\UAB\Successful Predictions and new images\105005_0_84_L_M_K.nii") 
imgC = nib.load(r"C:\Users\UAB\Successful Predictions and new images\105005_0_84_L_C.nii")
imgPred=nib.load(r"C:\Users\UAB\Successful Predictions and new images\105005_0_84_L__instanceCystSeg_modelWeights_3ch_t001CY_PREDICTION.nii")
print(type(imgM))
print(imgM.shape)

imgM_data = imgM.get_fdata()

print(type(imgM_data))
print(imgM_data.shape)


mid_slice_M = imgM_data[:,:,60]
print(mid_slice_M.shape)
plt.imshow(mid_slice_M.T, cmap='gray')


print(type(imgK))
print(imgK.shape)

imgK_data = imgK.get_fdata()

print(type(imgK_data))
print(imgK_data.shape)


mid_slice_K = imgK_data[:,:,60]
print(mid_slice_K.shape)
plt.imshow(mid_slice_K.T, cmap='gray')

print(type(imgC))
print(imgC.shape)

imgC_data = imgC.get_fdata()

print(type(imgC_data))
print(imgC_data.shape)


mid_slice_C = imgC_data[:,:,60]
print(mid_slice_C.shape)
plt.imshow(mid_slice_C.T, cmap='gray')

print(type(imgPred))
print(imgPred.shape)

imgPred_data = imgPred.get_fdata()

print(type(imgPred_data))
print(imgPred_data.shape)


mid_slice_P2 = imgPred_data[:,:,180]
print(mid_slice_P2.shape)
plt.imshow(mid_slice_P2.T, cmap='gray')


#%% 
print(mid_slice_C.shape, np.ptp(mid_slice_C))
print(mid_slice_P.shape, np.ptp(mid_slice_P))
print(mid_slice_P.shape, np.ptp(mid_slice_P))
print(mid_slice_P.shape, np.ptp(mid_slice_P2))
print(mid_slice_P.shape, np.ptp(mid_slice_P3))


#%%
mid_slice_P3 = imgPred_data[:,:,200]
plt.imshow(mid_slice_P3.T, cmap='summer')
#%%
print(mid_slice_C.shape, np.ptp(mid_slice_C))
print(mid_slice_P.shape, np.ptp(mid_slice_K))
print(mid_slice_P.shape, np.ptp(mid_slice_M))
print(mid_slice_P.shape, np.ptp(mid_slice_P2))
print(mid_slice_P.shape, np.ptp(mid_slice_P3))


#%%  
def read_nifti_file(path):
    nifti_image = nib.load(path)
    nib_data = nifti_image.get_fdata()
    return nib_data

def retrieve_images_and_segmentations(data_path, images, segmentations, size=(256,256)):
  x = []
  y = []
  for i in range(len(images)):
    seg = read_nifti_file(data_path+segmentations[i])
    img = read_nifti_file(data_path+images[i])
    assert img.shape == seg.shape
    seg = resize(seg,(size[0], size[1], seg.shape[-1]))
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

def visualise_data(x, y):
  n=4
  dim = int(np.ceil(np.sqrt(n)))
  fig = plt.figure(figsize=(10,10))
  for i in range(n):
    ax = fig.add_subplot(dim, dim, i+1)
    ax.imshow(x[50*i,:,:,0], cmap='gray')
    contours = measure.find_contours(y[50*i,:,:,0], .99)
    for contour in contours:
      ax.plot(contour[:,1], contour[:,0], color='#FB3640', lw=4)
    ax.axis('off')


def visualise_data_and_prediction(x, y, y_pred):
  n=4
  dim = int(np.ceil(np.sqrt(n)))
  fig = plt.figure(figsize=(10,10))
  for i in range(n):
    ax = fig.add_subplot(dim, dim, i+1)
    ax.imshow(x[50*i,:,:,0], cmap='gray')
    contours = measure.find_contours(y[50*i,:,:,0], .99)
    for j,contour in enumerate(contours):
      ax.plot(contour[:,1], contour[:,0], color='#FB3640', lw=4)
    contours = measure.find_contours(y_pred[50*i,:,:,0], .99)
    for contour in contours:
      ax.plot(contour[:,1], contour[:,0], color='#35A7FF', lw=4)
    ax.axis('off')
    

#%%

data_path = r'C:\Users\UAB\Successful Predictions and new images\Successful trial 5.16.22\\'
images = []
segmentations = []
for f in os.listdir(data_path):
  if '_C' in f:
    continue
  else:
    images.append(f)
    segmentations.append(f.replace('.nii', '_C.nii'))

print(images[0], segmentations[0])
images = np.array(images)
segmentations = np.array(segmentations)

indices = np.array(range(len(images))) # we will use this in the next step.
#%%

x_, y_ = retrieve_images_and_segmentations(data_path, images, segmentations) #TODO: get the
visualise_data(x_,y_)

#%%
