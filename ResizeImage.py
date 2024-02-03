from PIL import Image
import os
import sys
from typing import Tuple
from tqdm import tqdm
import shutil  # Module for operations on files including moving and copying

# Function to resize an image to the given size
def resize_image(image_path: str, output_path: str, size: Tuple[int, int]) -> None:
    with Image.open(image_path) as img:
        img.thumbnail(size, Image.LANCZOS)  # Resize the image
        img.save(output_path)  # Save the resized image

# Function to resize all images in a given folder to the given size
def resize_images_in_folder(input_folder: str, size: Tuple[int, int]) -> None:
    output_folder = os.path.join(input_folder, 'resize')  # Folder to save resized images
    original_folder = os.path.join(input_folder, 'original')  # Folder to save original images
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the folder if it doesn't exist
    if not os.path.exists(original_folder):  # If the folder to save original images doesn't exist, create it
        os.makedirs(original_folder)

    # Get all image files in the input folder
    images = [f for f in os.listdir(input_folder) if f.endswith(".jpg") or f.endswith(".png")]
    for filename in tqdm(images, desc="Resizing images"):  # Loop over all images
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        original_path = os.path.join(original_folder, filename)  # Path to save the original image
        resize_image(image_path, output_path, size)  # Resize the image
        shutil.move(image_path, original_path)  # Move the original image to the original folder

# Function to calculate the total size of all files in a given folder
def get_folder_size(folder: str) -> int:
    total = 0
    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            total += os.path.getsize(fp)  # Add the size of each file to the total
    return total

# Function to print the size of the original and resized folders and the percentage reduction in size
def print_folder_size_info(input_folder: str) -> None:
    original_folder = os.path.join(input_folder, 'original')
    resized_folder = os.path.join(input_folder, 'resize')

    original_size = get_folder_size(original_folder)
    resized_size = get_folder_size(resized_folder)
    reduction_percent = (original_size - resized_size) / original_size * 100

    print(f"Original folder size: {original_size / (1024 * 1024):.2f} MB")
    print(f"Resized folder size: {resized_size / (1024 * 1024):.2f} MB")
    print(f"Size reduction: {reduction_percent:.2f}%")

# Define the size to resize images to
size = (800, 800)

# Get the input folder from the command line arguments
input_folder = sys.argv[1]
# Resize all images in the input folder
resize_images_in_folder(input_folder, size)
# Print the size information
print_folder_size_info(input_folder)

# This script resizes all images in a given folder to a specified size. 
# It saves the resized images in a subfolder named 'resize' and moves the original images to a subfolder named 'original'.
# It then prints the total size of the original and resized image folders and the percentage reduction in size.