from keras.models import Sequential, load_model
import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import matplotlib.pyplot as plt
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

data_path = r"C:\Users\UAB\data\512_AllNII"


def gather_set(data_path, phrase):
    set_of = []
    path = data_path + '\\'
    for f in os.listdir(data_path):
      if phrase in f:
        set_of.append(f)
      else:
        continue
    set_of = np.array(set_of)

    indices = np.array(range(len(set_of))) # we will use this in the next step.

    return set_of

def gather_images(data_path):
    images = []
    path = data_path + '\\'
    for f in os.listdir(data_path):
      if '_K' in f:
        continue
      else:
        images.append(f)
        #segmentations.append(f.replace('.nii', '_K.nii'))

    #print(images[0], segmentations[0])
    images = np.array(images)
    #segmentations = np.array(segmentations)

    indices = np.array(range(len(images))) # we will use this in the next step.

    return images

def retrieve_images_for_prediction(data_path, images,num, size=(512,512)):
  x = []
  for i in range(num):
    img = read_nifti_file(data_path+'\\'+images[i])
    img = resize(img,(size[0], size[1], img.shape[-1]))
    for j in range(img.shape[-1]):
      x.append(img[:,:,j])
  x = np.array(x)[:,:,:,np.newaxis]

  return x

def visualise_data(x, y):
  n=4
  dim = int(np.ceil(np.sqrt(n)))
  fig = plt.figure(figsize=(20,10))
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
  fig = plt.figure(figsize=(20,10))
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
segmentations = gather_set(data_path, '_K')
images = gather_images(data_path)
image_set = retrieve_images_for_prediction(data_path, images, 5, size=(512,512))
seg_set = retrieve_images_for_prediction(data_path, segmentations, 5, size = (512,512))

visualise_data(image_set, seg_set)

path = r'C:\Users\UAB\data\512_AllNII\Kidney Predict 50 epoch'
predictions = gather_set(path, '_P50')
prediction_set = retrieve_images_for_prediction(path, predictions, 3, size=(512,512))


test = nib.load(r"C:\Users\UAB\data\512_AllNII\Kidney Predict 50 epoch\101934_1_96_L_M_P50_2.nii")
test_data = test.get_fdata()
print(test_data.shape)
plt.imshow(test_data[50,:,:], cmap='gray')

#%%
def retrieve_prediction(data_path, images,num, size=(512,512)):
  x = []
  for i in range(num):
    img = read_nifti_file(data_path+'\\'+images[i])
    img = resize(img,(size[0], size[1], img.shape[0]))
    for j in range(img.shape[0]):
        x.append(img[:,:,j])
  x = np.array(x)[:,:,:,np.newaxis]

  return x

#%%
test = nib.load(r"C:\Users\UAB\data\512_AllNII\Kidney Predict 50 epoch\101934_1_96_L_M_P50_3.nii")
test_data = test.get_fdata()
print(test_data.shape)
new_set = np.zeros((512,512, 96))
for i in range(test_data.shape[0]):
    new_set[:,:,i] = test_data[i,:,:]

    

plt.imshow(test_data[50,:,:], cmap='gray')
plt.imshow(test_data[:,:,50], cmap='gray')















