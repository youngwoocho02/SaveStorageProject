from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
import os
import sys
from typing import Tuple
from tqdm import tqdm
import shutil  # Module for operations on files including moving and copying

# Function to resize a video using ffmpeg
def resize_video(video_path: str, output_path: str, size: Tuple[int, int]) -> None:
    ffmpeg_resize(video_path, output_path, size)

# Function to resize all videos in a given folder
def resize_videos_in_folder(input_folder: str, size: Tuple[int, int]) -> None:
    output_folder = os.path.join(input_folder, 'resize')  # Folder to save resized videos
    original_folder = os.path.join(input_folder, 'original')  # Folder to save original videos
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the folder if it doesn't exist
    if not os.path.exists(original_folder):  # If the folder to save original videos doesn't exist, create it
        os.makedirs(original_folder)

    # Get all video files in the input folder
    videos = [f for f in os.listdir(input_folder) if f.endswith(".mp4") or f.endswith(".avi")]
    for filename in tqdm(videos, desc="Resizing videos"):  # Loop over all videos
        video_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        original_path = os.path.join(original_folder, filename)  # Path to save the original video
        resize_video(video_path, output_path, size)  # Resize the video
        shutil.move(video_path, original_path)  # Move the original video to the original folder

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

# Define the size for resizing
size = (800, 800)

# Get the input folder from the command line arguments
input_folder = sys.argv[1]
# Resize all videos in the input folder
resize_videos_in_folder(input_folder, size)
# Print the size information
print_folder_size_info(input_folder)

# This script resizes all videos in a given folder using ffmpeg. 
# It saves the resized videos in a subfolder named 'resize' and moves the original videos to a subfolder named 'original'.
# It then prints the total size of the original and resized video folders and the percentage reduction in size.