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
imx = 'PRNU_MATH535_PYTHON\Other Images Grey Cropped'+os.sep+'IMG_1736.jpeg'
image_PRNU = Ft.NoiseExtractFromImage(imx, sigma=2.)

# Usage for a folder of images to create a PRNU reference image for a device
# (example folder is Regular Scenes folder from Homework 2, 2nd_Camera on the class Google Drive)
image_folder = 'PRNU_MATH535_PYTHON\Camera Fingerprint Images Grey Cropped'
image_paths = glob(os.path.join(image_folder, '*.jpeg'))
ref_Image, _ = gF.getFingerprint(image_paths)
cv.imwrite('PRNU_MATH535_PYTHON\PRNU_Ref_Image.jpeg', ref_Image)

# Note for correlation: use np.corrcoef(x, y)
# This is: the sample correlation between points (treated as a sequence of values)
# Returned as a grid. Upper left gives corrcoef(x,x), upper right gives corrcoef(x,y)
# lower left gives corrcoef(y,x), lower left gives corrcoef(y,y)
# Example: correlation between the above individual reference image and camera reference image
corr = np.corrcoef(np.reshape(ref_Image, (1,len(ref_Image)*len(ref_Image[0]))), np.reshape(image_PRNU, (1,len(image_PRNU)*len(image_PRNU[0]))))
print(corr[0,1])

# NEED TO MODIFY TO FOLLOW STEPS IN HW_3 PDF RATHER THAN THE EXAMPLE CODE: IT SHOULD NOT READ A SINGLE IMAGE BUT 30 THEN OPERATE ON A SET OF 70
# Images have been downloaded from onedrive but need to be transformed beforehand, possibly adding the transform function to the beginning of this file after it it working properly