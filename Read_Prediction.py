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


data_path = r'C:\Users\UAB\Pad 512'
filename = '101934_0_L__instanceCystSeg_modelWeights_3ch_t001CY_PREDICTION.npy.nii'
imgOG = nib.load(filename)

print(type(imgOG))
print(imgOG.shape)

imgOG_data = imgOG.get_fdata()

print(type(imgOG_data))
print(imgOG_data.shape)

print(imgOG_data)


mid_slice_x = imgOG_data[:,:,288]
print(mid_slice_x.shape)
plt.imshow(mid_slice_x.T, cmap='summer')
