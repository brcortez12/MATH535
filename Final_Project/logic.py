# MATH535 - Final Project - Brandon Cortez
import numpy as np
from skimage import io, util, color
import matplotlib.pyplot as plt

def embed_message(image_path, message):
    # Embed a provided message into the loaded cover image
    # Load the cover image and convert to grayscale
    cover_image = io.imread(image_path)
    cover_image_gray = color.rgb2gray(cover_image)
    cover_image_gray = util.img_as_ubyte(cover_image_gray)
    # Flatten the grayscale cover image
    cover_image_flat = cover_image_gray.ravel()

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Calculate the message length
    message_length = len(binary_message)
    # Convert binary message length to binary string
    binary_message_length = format(message_length, '016b')

    # Embed the message length into the LSBs of the first 16 pixels
    for i in range(16):
        cover_image_flat[i] = (cover_image_flat[i] & 0xFFFE) | int(binary_message_length[i], 2)
    # Embed the entire binary message into the LSBs of the pixels after the message length
    binary_message_bits = [int(bit) for bit in binary_message]
    for i in range(16, 16 + len(binary_message_bits)):
        cover_image_flat[i] = (cover_image_flat[i] & 0xFFFE) | binary_message_bits[i - 16]
    # Reshape the grayscale cover image back to its original shape to form the stego image
    stego_image_gray = cover_image_flat.reshape(cover_image_gray.shape)

    print("Message: ", message)
    print("Binary Message: ", binary_message)
    print("Message Length: ", message_length)
    print("Binary Message Length: ", binary_message_length)
    return stego_image_gray

def extract_message(stego_image_gray): #Does not compute length correctly
    # Load the stego image and convert to grayscale
    # stego_image = io.imread(image_path)
    # stego_image_gray = color.rgb2gray(stego_image)
    # stego_image_gray = util.img_as_ubyte(stego_image_gray)
    # Flatten the grayscale stego image
    stego_image_flat = stego_image_gray.ravel()

    # Extract the message length from the LSBs of the first 16 pixels
    binary_message_length = ''
    for i in range(16):
        binary_message_length += str(stego_image_flat[i] & 1)
    # Convert binary message length to integer
    message_length = int(binary_message_length, 2)

    # Extract the binary message from the LSBs of the pixels after the message length
    binary_message = ''
    for i in range(16, 16 + message_length):
        binary_message += str(stego_image_flat[i] & 1)

    # Convert binary message to ASCII characters
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    print("Message: ", message)
    print("Binary Message: ", binary_message)
    print("Message Length: ", message_length)
    print("Binary Message Length: ", binary_message_length)
    return message


def difference_LSBs(cover_image, stego_image):
    # Compute difference image to display changed LSBs
    difference_image = np.abs(cover_image - stego_image)

    return difference_image
