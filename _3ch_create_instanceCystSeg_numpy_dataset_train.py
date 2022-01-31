#Libraries
from numpy.lib.stride_tricks import as_strided as ast
import numpy as np
import nibabel as nib
import sys
import os 
import random
from tqdm import *
import h5py
import os.path
import cv2
#import skimage.transform as ski
import numpy as np
import sys
import nibabel as nib
from tqdm import *
import scipy
print("libraries imported")


#Edit the following two...
input_folder=r'C:\Users\UAB\CyInstSeg\Resized\Training' #Training data folder
output_folder = r'C:\Users\UAB\CyInstSeg\Resized\Training_Output'

image_folder = r'C:\Users\UAB\CyInstSeg\Resized\Training\NII Images'
seg_folder = r'C:\Users\UAB\CyInstSeg\Resized\Training\NII Segments'

#names for corresponding files
oriprefix = 'MR' # MR image extension
segprefix = 'K' # Kidney segmentation extension
cystprefix = 'CY' # Edge-Core segmentation extension
strremove = -len(segprefix)

#CHANGE MADE HERE THAT NEEDS TO BE ADDRESSED WHEN THE LARGER SET IS READY
Scan = 250
Scan2 = 250

count = 0
subdir, dirs, files = os.walk(input_folder).__next__()
files = [k for k in files if segprefix in k]

#make directory if doesn't exist
if not os.path.exists(output_folder):
	print('making directory')
	os.makedirs(output_folder)

#Now loop through files and build up numpy arrays
for filename in tqdm(files):
	count+=1
	if segprefix in filename:
		#try:
			#load MR image files
			img = nib.load(input_folder+'/'+image_folder+'/'+filename[:strremove]+oriprefix)
			data = img.get_data()

			#pre-process - convert to float 32 and threshold to 99th percentile
			data=np.asarray(data).astype(np.float32)
			data = data/np.percentile(data,99) * 255
			data[data>255] = 255
			
			#load kidney seg file and pre-process
			segimg = nib.load(input_folder+'/'+seg_folder+'/'+filename)
			segdata = segimg.get_data()
			segdata = np.asarray(segdata).astype(np.float32)

			#load up cyst edge file (background==0, cysts==1, edges==2)
			cystimg = nib.load(input_folder+'/'+seg_folder+'/'+filename[:strremove]+cystprefix)
			cystdata = cystimg.get_data()
			cystdata = np.asarray(cystdata).astype(np.float32)

			aslice = np.zeros(shape=[Scan,Scan2,4],dtype='float32')

			#format all to same size
			for io in range(0,np.shape(segdata)[2]): 
				#if first slice make a zero padded version of first channel on this first slice
				if io==0:
					dataslice1 = np.zeros(shape=[Scan,Scan2],dtype='float32')
				else:
					dataslice1 = cv2.resize(data[:,:,io-1], (Scan,Scan2), interpolation=cv2.INTER_CUBIC)

				dataslice2 = cv2.resize(data[:,:,io], (Scan,Scan2), interpolation=cv2.INTER_CUBIC)

				#if last slice make a zero padded version of the last channel on this last slice
				if io==np.shape(segdata)[2]-1:
					dataslice3 = np.zeros(shape=[Scan,Scan2],dtype='float32')
				else:
					dataslice3 = cv2.resize(data[:,:,io+1], (Scan,Scan2), interpolation=cv2.INTER_CUBIC)

				segslice = cv2.resize(segdata[:,:,io], (Scan,Scan2), interpolation=cv2.INTER_NEAREST)
				cystslice = cv2.resize(cystdata[:,:,io], (Scan,Scan2), interpolation=cv2.INTER_NEAREST)

				dataslice[:,:,0] = dataslice1
				dataslice[:,:,1] = dataslice2
				dataslice[:,:,2] = dataslice3
				dataslice[:,:,3] = segslice

				#save out as numpy files
				np.save(output_folder+filename[:strremove]+'slice_'+str(io)+'.npy',dataslice)
				np.save(output_folder+filename[:strremove]+'slice_'+str(io)+'_mask.npy',cystslice)

print('done')
