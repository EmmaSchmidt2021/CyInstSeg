# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:56:15 2022

@author: UAB
"""


import os
import numpy as np
import keras
import tensorflow

class DataGenerator(tensorflow.keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = np.load('data/' + ID + '.npy')

            # Store class
            y[i] = self.labels[ID]

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

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
#%%
data_path = r"C:\Users\UAB\Kidney-Segmentation-Jupyter\data"

images = gather_set(data_path, '_M')
labels = gather_set(data_path, '_K')

d = {}
for i in images:
    if i not in d:
        d[i] = len(d)

labels_mapping = list(map(d.get, images))

labels = {images[i]:labels_mapping[i] for i in range(len(images))}
print(list(labels.items())[:4])

#%%
from sklearn.model_selection import train_test_split
train, val = train_test_split(list(partition.keys()),train_size = 0.8)
partition = {'train':train, 'validation':val}

print(list(partition.items())[:4])
#%%
params = {'dim': (512,512,1),
          'batch_size': 12,
          'n_classes': 2,
          'n_channels': 1,
          'shuffle': True}
training_generator = DataGenerator(partition['train'], labels, **params)
validation_generator = DataGenerator(partition['validation'], labels, **params)

#%% translate multi slice stacks to single files


import numpy as np
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
#%%
data_path = r"C:\Users\UAB\Kidney-Segmentation-Jupyter\data"

images = gather_set(data_path, '_M.')
labels = gather_set(data_path, '_K')

#%%
new_path = r"C:\Users\UAB\Kidney-Segmentation-Jupyter\data\Single Images"
for i in range(len(images)):
    working_img = np.load(data_path + '\\' + images[i])
    file_name = images[i][:-5]
    for j in range(working_img.shape[-1]):
        save_slice = working_img[:,:,j]
        new_fname = str(file_name + str(j) +'_M')
        np.save(os.path.join(new_path, new_fname), save_slice)
        
for i in range(len(labels)):
    working_img = np.load(data_path + '\\' + labels[i])
    file_name = labels[i][:-7]
    for j in range(working_img.shape[-1]):
        save_slice = working_img[:,:,j]
        new_fname = str(file_name + str(j) +'_K')
        np.save(os.path.join(new_path, new_fname), save_slice)
        