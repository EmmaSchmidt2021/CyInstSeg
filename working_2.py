# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 15:45:12 2022

@author: emmasch
"""
"""
checking github connection//pushing
"""

from tensorflow.keras.models import load_model
import h5py 
# https://docs.h5py.org/en/stable/quick.html -- documentation on loading in hdf5
# https://docs.h5py.org/en/stable/high/file.html -- explanition of the 'file object' that was loaded in


#model = load_model('instanceCystSeg_modelWeights_3ch_t001.hdf5')

file = h5py.File('instanceCystSeg_modelWeights_3ch_t001.hdf5', 'r')
list(file.keys()) #  ['model_weights', 'optimizer_weights']

#break out and explore
model_weights = file['model_weights']
list(model_weights.keys())
optimizer_weights = file['optimizer_weights']
list(optimizer_weights.keys())


#%%from stack exchage - navigate the HDF5 without knowing the data structure

def traverse_datasets(hdf_file):

    def h5py_dataset_iterator(g, prefix=''):
        for key in g.keys():
            item = g[key]
            path = f'{prefix}/{key}'
            if isinstance(item, h5py.Dataset): # test for dataset
                yield (path, item)
            elif isinstance(item, h5py.Group): # test for group (go down)
                yield from h5py_dataset_iterator(item, path)

    for path, _ in h5py_dataset_iterator(hdf_file):
        yield path

filename = 'instanceCystSeg_modelWeights_3ch_t001.hdf5'
with h5py.File(filename, 'r') as f:
    for dset in traverse_datasets(f):
        print('Path:', dset)
        print('Shape:', f[dset].shape)
        print('Data type:', f[dset].dtype)
#not super helpful but worth a shot
#%%save and load documentation from TensorFlos 
#https://www.tensorflow.org/tutorials/keras/save_and_load

#%% import from unet_inception
import sys
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Dense
from keras.layers import BatchNormalization, Dropout, Flatten, Lambda
from keras.layers.merge import concatenate, add
from keras.layers.advanced_activations import ELU, LeakyReLU
from metric import dice_coef, dice_coef_loss

IMG_ROWS, IMG_COLS = 512,512



#%% import from train_unet
from __future__ import print_function
import cv2
import numpy as np
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, merge
from keras.layers.merge import concatenate, add
from tensorflow.keras.optimizers import Adam, SGD
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as K
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from unet_inception import NConvolution2D, rblock, inception_block, _shortcut
from metric import dice_coef, dice_coef_loss,jaccard_distance_loss
from keras.preprocessing.image import ImageDataGenerator
from _3ch_instanceCystSeg_data_prepare_ALL_2d_n512 import load_train_data, load_val_data

K.set_image_data_format('channels_first') 
# channels first means that it is looking for the information in this order
# (batch, channels, height, width)
img_rows = 512
img_cols = 512


smooth = 1.
do = 0.1
#%% get model from train_unet
from _3ch_instanceCystSeg_train_unet import get_unet

#%%
model = get_unet()
model.summary()

from tensorflow.keras.models import load_model
model = load_model('./instanceCystSeg_modelWeights_3ch_t001.hdf5', compile=False)




