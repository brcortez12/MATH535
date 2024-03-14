# Import necessary modules
import os
import cv2
import numpy as np
from Transform_Images import process_images
from src.getFingerprint import getFingerprint
from src.Filter import NoiseExtractFromImage
# Import other provided code files as needed

# Define Functions

def create_camera_fingerprint(image_folder):
    """
    Creates the camera fingerprint using provided code.
    """
    # Get the list of image paths
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder)]
    # Ensure the images are sorted to maintain consistency
    image_paths.sort()
    # Use only the first 30 images
    image_paths = image_paths[:30]
    # Create the camera fingerprint using the first 30 images
    camera_fingerprint, _ = getFingerprint(image_paths)
    
    return camera_fingerprint

def extract_image_fingerprint(image_path):
    """
    Extracts fingerprint from a single image.
    """
    # Read the image
    img = cv2.imread(image_path)

    # Extract noise from the image
    image_fingerprint = NoiseExtractFromImage(image_path, sigma=2.)

    return image_fingerprint

def calculate_correlation(camera_fingerprint, image_fingerprint):
    """
    Calculates the correlation between camera and image fingerprints.
    """
    # Implement the logic to calculate correlation
    # Placeholder implementation
    correlation_value = np.random.uniform(-1, 1)  # Placeholder random correlation value
    return correlation_value

def decide_match(correlation_value, threshold):
    """
    Decides if the correlation value qualifies as a match.
    """
    # Implement the logic to decide match based on threshold
    # Placeholder implementation
    match = correlation_value >= threshold  # Placeholder logic
    return match

def main():
    # Paths
    camera_input_folder = 'PRNU_MATH535_PYTHON/Camera Fingerprint Images'
    other_input_folder = 'PRNU_MATH535_PYTHON/Other Images'
    output_folder = 'PRNU_MATH535_PYTHON'

    # Step 1: Preprocess images
    print("Preprocessing images...")
    process_images(camera_input_folder, other_input_folder, output_folder)
    print("Images preprocessed.")

    # Step 2: Create camera fingerprint
    print("Creating camera fingerprint...")
    camera_fingerprint = create_camera_fingerprint(os.path.join(output_folder, 'Camera Fingerprint Images Grey Cropped'))
    print("Camera fingerprint created.")

    # Step 3: Extract image fingerprints and calculate correlation
    print("Extracting image fingerprints and calculating correlation...")
    for image_name in os.listdir(os.path.join(output_folder, 'Other Images Grey Cropped')):
        image_path = os.path.join(output_folder, 'Other Images Grey Cropped', image_name)
        print(f"Processing image: {image_name}")
        image_fingerprint = extract_image_fingerprint(image_path)
        correlation_value = calculate_correlation(camera_fingerprint, image_fingerprint)

        # Step 4: Decide if the correlation value qualifies as a match
        threshold = 0.8
        match = decide_match(correlation_value, threshold)
        print(f"Image: {image_name}, Correlation: {correlation_value}, Match: {match}")

if __name__ == "__main__":
    main()

