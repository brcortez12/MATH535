import os
import cv2
import glob

def center_crop(image):
    """
    Center crops the input image to a square.
    
    Parameters:
    - image (numpy.ndarray): Input image to be cropped.
    
    Returns:
    - numpy.ndarray: Cropped image.
    """
    # Get dimensions of the image
    h, w = image.shape[:2]
    
    # Determine the size of the square crop
    size = min(h, w)
    
    # Calculate cropping coordinates
    top = (h - size) // 2
    bottom = top + size
    left = (w - size) // 2
    right = left + size
    
    # Perform the center crop
    cropped_image = image[top:bottom, left:right]
    
    return cropped_image

def crop_to_square(image, size=1024):
    """
    Crops the input image to a square with the specified size.
    
    Parameters:
    - image (numpy.ndarray): Input image to be cropped.
    - size (int): Size of the output square image.
    
    Returns:
    - numpy.ndarray: Cropped image.
    """
    # Get dimensions of the image
    h, w = image.shape[:2]
    
    # Calculate cropping coordinates
    top = (h - size) // 2
    bottom = top + size
    left = (w - size) // 2
    right = left + size
    
    # Perform the crop
    cropped_image = image[top:bottom, left:right]
    
    return cropped_image

def resize_and_save_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of image file paths in the input folder
    image_paths = glob.glob(os.path.join(input_folder, '*.jpeg'))

    for img_path in image_paths:
        # Read the image
        img = cv2.imread(img_path)

        # Center crop the image to a square
        cropped_img = center_crop(img)

        # Crop the square image to 1024x1024
        cropped_img = crop_to_square(cropped_img, size=1024)

        # Convert the image to grayscale
        grayscale_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

        # Save the grayscale image to the output folder in .jpg format
        img_name = os.path.basename(img_path)
        img_name = os.path.splitext(img_name)[0] + '.jpg'
        output_path = os.path.join(output_folder, img_name)
        cv2.imwrite(output_path, grayscale_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # Save with 100% quality

if __name__ == "__main__":
    input_folder = 'PRNU_MATH535_PYTHON\Camera Fingerprint Images'  # Specify the path to your input folder containing images
    output_folder = 'PRNU_MATH535_PYTHON\Camera Fingerprint Images Alt'  # Specify the path to the output folder where resized grayscale images will be saved

    resize_and_save_images(input_folder, output_folder)
