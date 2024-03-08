import src.Functions as Fu
import src.Filter as Ft
import src.getFingerprint as gF
import src.maindir as md
import src.extraUtils as eu
import numpy as np
import os
from glob import glob
from PIL import Image
import cv2 as cv
import scipy.io as sio

# Example code for how to use PRNU Python code
# Written for Math 535 Spring 2023 by Abby Martin
# Updated 3/1/23

# Usage for an individual image
# (example image is from Homework 2, 2nd_Camera, Regular Scenes folder
# on the class Google Drive
imx = 'PRNU_MATH535_PYTHON\images1'+os.sep+'dune.jpg'
print(imx)
image_PRNU = Ft.NoiseExtractFromImage(imx, sigma=2.)


# Usage for a folder of images to create a PRNU reference image for a device
# (example folder is Regular Scenes folder from Homework 2, 2nd_Camera on the class Google Drive)
ref_Image_Folder = glob(os.path.join('images2', '*.jpg'))
ref_Image,_ = gF.getFingerprint(ref_Image_Folder)
# sio.savemat('referenceImage.mat', {'ref_Image': ref_Image})
Image.fromarray(ref_Image).save('PRNU_Ref_Image.jpg')

# Note for correlation: use np.corrcoef(x, y)
# This is: the sample correlation between points (treated as a sequence of values)
# Returned as a grid. Upper left gives corrcoef(x,x), upper right gives corrcoef(x,y)
# lower left gives corrcoef(y,x), lower left gives corrcoef(y,y)
# Example: correlation between the above individual reference image and camera reference image
corr = np.corrcoef(np.reshape(ref_Image, (1,len(ref_Image)*len(ref_Image[0]))), np.reshape(image_PRNU, (1,len(image_PRNU)*len(image_PRNU[0]))))
print(corr[0,1])