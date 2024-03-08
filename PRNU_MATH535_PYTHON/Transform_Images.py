# The intent of this module is to be imported into the Cortez_main.py module for use cropping and preparing the images before use in the fingerprint generation
import os
import cv2
import numpy as np

def center_crop(image):
    h, w = image.shape[:2]
    size = min(h, w)
    top = (h - size) // 2
    bottom = top + size
    left = (w - size) // 2
    right = left + size
    cropped_image = image[top:bottom, left:right]
    return cropped_image

def process_images(camera_input_folder, other_input_folder, output_folder):
    print("Processing images...")
    # Create output folders if they don't exist
    camera_output_folder = os.path.join(output_folder, "Camera Fingerprint Images Grey Cropped")
    other_output_folder = os.path.join(output_folder, "Other Images Grey Cropped")
    os.makedirs(camera_output_folder, exist_ok=True)
    os.makedirs(other_output_folder, exist_ok=True)

    # Process camera fingerprint images
    print(f"Processing camera fingerprint images from: {camera_input_folder}")
    for img_name in os.listdir(camera_input_folder):
        img_path = os.path.join(camera_input_folder, img_name)
        print(f"Processing image: {img_name}")
        img = cv2.imread(img_path)
        grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cropped_img = center_crop(grayscale_img)
        output_path = os.path.join(camera_output_folder, img_name)
        cv2.imwrite(output_path, cropped_img)
        print(f"Image processed and saved at: {output_path}")

    # Process other images
    print(f"Processing other images from: {other_input_folder}")
    for img_name in os.listdir(other_input_folder):
        img_path = os.path.join(other_input_folder, img_name)
        print(f"Processing image: {img_name}")
        img = cv2.imread(img_path)
        grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cropped_img = center_crop(grayscale_img)
        output_path = os.path.join(other_output_folder, img_name)
        cv2.imwrite(output_path, cropped_img)
        print(f"Image processed and saved at: {output_path}")

def main():
    # Paths
    camera_input_folder = 'PRNU_MATH535_PYTHON/Camera Fingerprint Images'
    other_input_folder = 'PRNU_MATH535_PYTHON/Other Images'
    output_folder = 'PRNU_MATH535_PYTHON'

    # Process images
    process_images(camera_input_folder, other_input_folder, output_folder)

if __name__ == "__main__":
    main()
