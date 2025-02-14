import numpy as np

def calculate_entropy(image):
    """
    Calculate the entropy of an image to measure its randomness.
    """
    hist = np.histogram(image, bins=256)[0]
    prob = hist / hist.sum()
    return -np.sum(prob * np.log2(prob + 1e-10))  # Add small epsilon to avoid log(0)

def calculate_npcr(original, encrypted):
    """
    Calculate the Number of Pixel Change Rate (NPCR) between two images.
    """
    diff = original != encrypted
    return (np.sum(diff) / original.size) * 100

def calculate_uaci(original, encrypted):
    """
    Calculate the Unified Average Changing Intensity (UACI) between two images.
    """
    diff = np.abs(original.astype(int) - encrypted.astype(int))
    return (np.sum(diff) / (255 * original.size)) * 100

def analyze_security(original, encrypted):
    """
    Perform a full security analysis on the encrypted image.
    """
    print("=== Security Analysis ===")
    print(f"Original Image Entropy: {calculate_entropy(original):.2f} bits")
    print(f"Encrypted Image Entropy: {calculate_entropy(encrypted):.2f} bits")
    print(f"NPCR: {calculate_npcr(original, encrypted):.2f}%")
    print(f"UACI: {calculate_uaci(original, encrypted):.2f}%")