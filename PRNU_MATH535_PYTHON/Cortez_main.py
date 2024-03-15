# Brandon Cortez - Homework 3 - MATH535 - MAR 15
import os
import cv2
import numpy as np
from Transform_Images import process_images
from src.getFingerprint import getFingerprint
from src.Filter import NoiseExtractFromImage

camera_input_folder = 'PRNU_MATH535_PYTHON/Camera Fingerprint Images'
other_input_folder = 'PRNU_MATH535_PYTHON/Other Images'
provided_input_folder = 'PRNU_MATH535_PYTHON/Not Your Camera Images'
root_folder = 'PRNU_MATH535_PYTHON'

def create_camera_fingerprint(image_folder):
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder)]
    camera_fingerprint, _ = getFingerprint(image_paths)
    return camera_fingerprint

def extract_and_calculate(ref_image, image_folder, threshold, category):
    print(f"Extracting image fingerprints and calculating correlation for images from {image_folder}...")
    index = 0
    false_positives = 0
    false_negatives = 0
    total_positives = 0
    total_negatives = 0

    for image_name in os.listdir(image_folder):
        index += 1
        image_path = os.path.join(image_folder, image_name)
        image_fingerprint = NoiseExtractFromImage(image_path)
        
        # Calculate correlation
        UA_flat = (ref_image * image_fingerprint).flatten()
        B_flat = image_fingerprint.flatten()
        corrvalue = 1 - np.corrcoef(UA_flat, B_flat)[0, 1]
        match = corrvalue >= threshold
        # print(f"Image: ImageFPrint{index}, Correlation: {corrvalue}, Match: {match}")
        print(f"ImageFPrint{index}, Correlation: {corrvalue}")

        if category: # If it is supposed to be a valid match
            total_positives += 1
            if not match: # False negative
                false_negatives += 1
        elif not category: # If not supposed to be a match
            total_negatives += 1
            if match:  # If there's a match
                false_positives += 1

    fnr_rate = false_negatives / total_positives if total_positives != 0 else 0
    fpr_rate = false_positives / total_negatives if total_negatives != 0 else 0

    print(f"False Positive Rate (FPR): {fpr_rate}")
    print(f"False Negative Rate (FNR): {fnr_rate}")

def main():

    camera_processed_folder, other_processed_folder =process_images(camera_input_folder, other_input_folder, root_folder)

    print("Creating camera fingerprint...")
    PRNU_Ref_Image = create_camera_fingerprint(camera_processed_folder)
    cv2.imwrite('PRNU_MATH535_PYTHON\PRNU_Ref_Image.jpeg', PRNU_Ref_Image)
    print("Camera fingerprint created.")

    threshold = 0.955
    extract_and_calculate(PRNU_Ref_Image, other_processed_folder, threshold, True)
    print('=============================================')
    extract_and_calculate(PRNU_Ref_Image, provided_input_folder, threshold, False)

    # Calculate range of values, average value, and variance
    intensity_values = PRNU_Ref_Image.flatten()
    min_intensity = np.min(intensity_values)
    max_intensity = np.max(intensity_values)
    average_intensity = np.mean(intensity_values)
    variance_intensity = np.var(intensity_values)
    print(f"Range of intensity values: [{min_intensity}, {max_intensity}]")
    print(f"Average intensity value: {average_intensity}")
    print(f"Variance of intensity values: {variance_intensity}")

    # Adjust intensity values to make the image viewable
    adjusted_image = (PRNU_Ref_Image - min_intensity) / (max_intensity - min_intensity) * 255
    adjusted_image = adjusted_image.astype(np.uint8)  # Convert to uint8 for display

    # Save the adjusted image as a JPEG file
    output_filename = 'PRNU_MATH535_PYTHON\adjusted_PRNU_Image.jpeg'
    cv2.imwrite(output_filename, adjusted_image)

    print(f"Adjusted image saved as {output_filename}")
    
if __name__ == "__main__":
    main()
