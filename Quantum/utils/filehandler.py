from PIL import Image
import numpy as np

def save_image(image_array, file_path):
    """
    Save a numpy array as an image file.
    """
    img = Image.fromarray(image_array.astype(np.uint8))
    img.save(file_path)
    print(f"Image saved to {file_path}")

def load_image(file_path):
    """
    Load an image file and return it as a numpy array.
    """
    img = Image.open(file_path)
    return np.array(img)