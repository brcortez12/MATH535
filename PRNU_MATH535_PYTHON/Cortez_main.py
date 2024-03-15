import os
import cv2
import numpy as np
from Transform_Images import process_images
from src.getFingerprint import getFingerprint
from src.Filter import NoiseExtractFromImage

def create_camera_fingerprint(image_folder):
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder)]
    image_paths = image_paths[:30]
    camera_fingerprint, _ = getFingerprint(image_paths)
    return camera_fingerprint

def main():
    camera_input_folder = 'PRNU_MATH535_PYTHON/Camera Fingerprint Images'
    other_input_folder = 'PRNU_MATH535_PYTHON/Other Images'
    output_folder = 'PRNU_MATH535_PYTHON'

    process_images(camera_input_folder, other_input_folder, output_folder)

    print("Creating camera fingerprint...")
    PRNU_Ref_Image = create_camera_fingerprint(os.path.join(output_folder, 'Camera Fingerprint Images Grey Cropped'))
    cv2.imwrite('PRNU_MATH535_PYTHON\PRNU_Ref_Image.jpeg', PRNU_Ref_Image)
    print("Camera fingerprint created.")

    test_image_path = os.path.join(output_folder, 'Other Images Grey Cropped', 'IMG_1736.jpeg')
    test_fingerprint = NoiseExtractFromImage(test_image_path)

    # Save the fingerprint as ImageFPrint(i)
    output_file_path = os.path.join(output_folder, 'ImageFPrint(i).txt')
    with open(output_file_path, 'wb') as f:
        np.savetxt(f, test_fingerprint, fmt='%f')

    print("Fingerprint from test image saved as ImageFPrint(i)")

    print("Extracting image fingerprints and calculating correlation...")
    for image_name in os.listdir(os.path.join(output_folder, 'Other Images Grey Cropped')):
        image_path = os.path.join(output_folder, 'Other Images Grey Cropped', image_name)
        print(f"Processing image: {image_name}")
        image_fingerprint = NoiseExtractFromImage(image_path)
        
        # Calculate correlation
        # Compute the element-wise product of U and A, then flatten the result
        UA_flat = (PRNU_Ref_Image * image_fingerprint).flatten()
        # Flatten the image fingerprint
        B_flat = image_fingerprint.flatten()
        corrvalue = 1 - np.corrcoef(UA_flat, B_flat)[0, 1]
        threshold = 0.6
        match = corrvalue >= threshold
        print(f"Image: {image_name}, Correlation: {corrvalue}, Match: {match}")

if __name__ == "__main__":
    main()
