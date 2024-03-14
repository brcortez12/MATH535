import os
import cv2
import numpy as np
from Transform_Images import process_images
from src.getFingerprint import getFingerprint
from src.Filter import NoiseExtractFromImage

def create_camera_fingerprint(image_folder):
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder)]
    image_paths.sort()
    image_paths = image_paths[:30]
    camera_fingerprint, _ = getFingerprint(image_paths)
    return camera_fingerprint

def extract_image_fingerprint(image_path):
    image_fingerprint = NoiseExtractFromImage(image_path, sigma=2.)
    return image_fingerprint

def calculate_correlation(camera_fingerprint, image_fingerprint):
    # Calculates the correlation between camera and image fingerprints.
    # Flatten the fingerprints to 1D arrays
    camera_fingerprint_flat = camera_fingerprint.flatten()
    image_fingerprint_flat = image_fingerprint.flatten()
    # Calculate the correlation coefficient
    correlation_matrix = np.corrcoef(camera_fingerprint_flat, image_fingerprint_flat)
    # The correlation coefficient between camera and image fingerprints is at position (0, 1) of the matrix
    correlation_value = correlation_matrix[0, 1]

    return correlation_value

def decide_match(correlation_value, threshold):
    match = correlation_value >= threshold
    return match

def main():
    camera_input_folder = 'PRNU_MATH535_PYTHON/Camera Fingerprint Images'
    other_input_folder = 'PRNU_MATH535_PYTHON/Other Images'
    output_folder = 'PRNU_MATH535_PYTHON'

    print("Preprocessing images...")
    process_images(camera_input_folder, other_input_folder, output_folder)
    print("Images preprocessed.")

    print("Creating camera fingerprint...")
    camera_fingerprint = create_camera_fingerprint(os.path.join(output_folder, 'Camera Fingerprint Images Grey Cropped'))
    print("Camera fingerprint created.")

    test_image_path = os.path.join(output_folder, 'Other Images Grey Cropped', 'IMG_1736.jpeg')
    test_fingerprint = extract_image_fingerprint(test_image_path)

    with open('ImageFPrint(i).txt', 'w') as f:
        f.write(test_fingerprint)
    print("Fingerprint from test image saved as ImageFPrint(i)")

    print("Extracting image fingerprints and calculating correlation...")
    for image_name in os.listdir(os.path.join(output_folder, 'Other Images Grey Cropped')):
        image_path = os.path.join(output_folder, 'Other Images Grey Cropped', image_name)
        print(f"Processing image: {image_name}")
        image_fingerprint = extract_image_fingerprint(image_path)
        
        # Calculate correlation
        correlation_value = calculate_correlation(camera_fingerprint, image_fingerprint)

        threshold = 0.6
        match = decide_match(correlation_value, threshold)
        print(f"Image: {image_name}, Correlation: {correlation_value}, Match: {match}")

if __name__ == "__main__":
    main()
