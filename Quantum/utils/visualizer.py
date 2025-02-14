import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def display_images(original, encrypted, decrypted):
    """
    Display the original, encrypted, and decrypted images side by side.
    """
    plt.figure(figsize=(15, 5))

    # Original Image
    plt.subplot(1, 3, 1)
    plt.imshow(original, cmap='gray' if len(original.shape) == 2 else None)
    plt.title("Original Image")
    plt.axis('off')

    # Encrypted Image
    plt.subplot(1, 3, 2)
    plt.imshow(encrypted, cmap='gray' if len(encrypted.shape) == 2 else None)
    plt.title("Encrypted Image")
    plt.axis('off')

    # Decrypted Image
    plt.subplot(1, 3, 3)
    plt.imshow(decrypted, cmap='gray' if len(decrypted.shape) == 2 else None)
    plt.title("Decrypted Image")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def plot_histogram(image, title):
    """
    Plot the histogram of pixel intensities for an image.
    """
    plt.figure()
    plt.hist(image.flatten(), bins=256, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()