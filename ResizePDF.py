import os
import subprocess
import sys
from tqdm import tqdm
import shutil  # Module for operations on files including moving and copying

# Path to the Ghostscript executable
gs_path = "C:\\Program Files\\gs\\gs10.02.1\\bin\\gswin64.exe"

# Function to resize a PDF using Ghostscript
def resize_pdf(input_pdf_path: str, output_pdf_path: str) -> None:
    subprocess.call([gs_path, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                     '-dPDFSETTINGS=/screen', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                     '-sOutputFile=' + output_pdf_path, input_pdf_path])

# Function to resize all PDFs in a given folder
def resize_pdfs_in_folder(input_folder: str) -> None:
    output_folder = os.path.join(input_folder, 'resized')  # Folder to save resized PDFs
    original_folder = os.path.join(input_folder, 'original')  # Folder to save original PDFs
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the folder if it doesn't exist
    if not os.path.exists(original_folder):  # If the folder to save original PDFs doesn't exist, create it
        os.makedirs(original_folder)

    # Get all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    for filename in tqdm(pdf_files, desc="Resizing PDFs"):  # Loop over all PDFs
        input_pdf_path = os.path.join(input_folder, filename)
        output_pdf_path = os.path.join(output_folder, filename)
        original_path = os.path.join(original_folder, filename)  # Path to save the original PDF
        resize_pdf(input_pdf_path, output_pdf_path)  # Resize the PDF
        shutil.move(input_pdf_path, original_path)  # Move the original PDF to the original folder

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
    resized_folder = os.path.join(input_folder, 'resized')

    original_size = get_folder_size(original_folder)
    resized_size = get_folder_size(resized_folder)
    reduction_percent = (original_size - resized_size) / original_size * 100

    print(f"Original folder size: {original_size / (1024 * 1024):.2f} MB")
    print(f"Resized folder size: {resized_size / (1024 * 1024):.2f} MB")
    print(f"Size reduction: {reduction_percent:.2f}%")

# Get the input folder from the command line arguments
input_folder = sys.argv[1]
# Resize all PDFs in the input folder
resize_pdfs_in_folder(input_folder)
# Print the size information
print_folder_size_info(input_folder)

# This script resizes all PDFs in a given folder using Ghostscript. 
# It saves the resized PDFs in a subfolder named 'resized' and moves the original PDFs to a subfolder named 'original'.
# It then prints the total size of the original and resized PDF folders and the percentage reduction in size.