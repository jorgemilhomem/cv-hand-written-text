import matplotlib.pyplot as plt
import os
import requests
import tarfile
import cv2
import numpy as np




def display_image(image):
    """
    Displays a given image.

    Parameters:
    - image: The image to be displayed.
    """
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def download_file(url, local_filename):
    if os.path.exists(local_filename):
        print(f"File {local_filename} already exists. Skipped download.")
        return local_filename
    else:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                print(f"Downloading {file_url} to {local_filename}")
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

def extract_files(filename, extract_path):
    # Check if the file is a tar archive
    if filename.endswith('.tar') or filename.endswith('.tgz'):
        if os.path.exists(extract_path):
            print(f"Files already extracted in {extract_path}. Skipped extraction.")
            return
        else:
            with tarfile.open(filename, 'r:*') as tar:
                tar.extractall(extract_path)
                print(f"Extracted {filename} to {extract_path}")
    else:
        print("File is not a tar or tgz archive.")

def distortion_free_resize(image, target_size=(128, 32)):
# Calculate the ratio of the target dimensions and the image
    target_ratio = target_size[1] / target_size[0]
    img_ratio = image.shape[0] / image.shape[1]

    # Determine the dimensions to which the image should be resized
    if img_ratio <= target_ratio:
        # Image is more horizontal; fit to width
        new_size = (target_size[0], int(image.shape[0] * target_size[0] / image.shape[1]))
    else:
        # Image is more vertical; fit to height
        new_size = (int(image.shape[1] * target_size[1] / image.shape[0]), target_size[1])
    
    # Resize the image to fit within the target rectangle
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

    # Calculate padding to center the image
    pad_x = (target_size[0] - resized_image.shape[1]) // 2
    pad_y = (target_size[1] - resized_image.shape[0]) // 2

    # Apply padding to center the image within the target rectangle
    padded_image = cv2.copyMakeBorder(resized_image, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=0)

    # Adjust if the padding isn't perfectly even (e.g., due to odd number dimensions)
    if padded_image.shape[0] != target_size[1] or padded_image.shape[1] != target_size[0]:
        padded_image = cv2.resize(padded_image, target_size, interpolation=cv2.INTER_AREA)

    return padded_image

def load_image(file_path):
    # Load an image in grayscale mode
    return cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)

def preprocess_image(image, target_size=(128, 32)):
    """
    Preprocesses an image by resizing it to the target size, normalizing it, and adding a channel dimension.

    Parameters:
    - image: The input image to be preprocessed.
    - target_size: The desired size of the image after resizing. Default is (128, 32).

    Returns:
    - The preprocessed image.
    """

    image = load_image(image)

    
    # Resize the image to the target size
    #image = cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)
    image = distortion_free_resize(image, target_size)

    # Normalize the image
    image = image.astype(np.float32) / 255.0
    
    # Add a channel dimension ([height, width] -> [height, width, 1])
    image = np.expand_dims(image, axis=-1)
    

    # reduce noise
    
    return image