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

imgOG = nib.load(r"C:\Users\UAB\CyInstSeg\105005_0_84_R_C.nii")
#imgOG = nib.load(r"C:\Users\UAB\CyInstSeg\101934_0_96_L_C.nii")
print(type(imgOG))
print(imgOG.shape)

imgOG_data = imgOG.get_fdata()

print(type(imgOG_data))
print(imgOG_data.shape)


mid_slice_x = imgOG_data[:,:,50]
print(mid_slice_x.shape)
plt.imshow(mid_slice_x.T, cmap='gray')
