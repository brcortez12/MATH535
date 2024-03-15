# The intent of this module is to be imported into the Cortez_main.py module for use cropping and preparing the images before use in the fingerprint generation
import os
import cv2
import numpy as np

def crop_and_save(output_path, img_path):
    print(f"Processing image: {img_path}")
    img = cv2.imread(img_path)
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = grayscale_img.shape
    startx = w//2 - (1024//2)
    starty = h//2 - (1024//2)
    if w != 1024 or h != 1024:
        processed_img = grayscale_img[starty:starty+1024, startx:startx+1024]
    else:
        processed_img = grayscale_img
    cv2.imwrite(output_path, processed_img)

def process_images(camera_input_folder, other_input_folder, root_folder):
    print("Processing images...")
    # Create output folders if they don't exist
    camera_output_folder = os.path.join(root_folder, "Camera Fingerprint Images Grey Cropped")
    other_output_folder = os.path.join(root_folder, "Other Images Grey Cropped")
    os.makedirs(camera_output_folder, exist_ok=True)
    os.makedirs(other_output_folder, exist_ok=True)

    # Process camera fingerprint images
    for img_name in os.listdir(camera_input_folder):
        img_path = os.path.join(camera_input_folder, img_name)
        output_path = os.path.join(camera_output_folder, img_name)
        crop_and_save(output_path, img_path)
        
    # Process other images
    for img_name in os.listdir(other_input_folder):
        img_path = os.path.join(other_input_folder, img_name)
        output_path = os.path.join(other_output_folder, img_name)
        crop_and_save(output_path, img_path)
    print("Processing Done.")

    return camera_output_folder, other_output_folder