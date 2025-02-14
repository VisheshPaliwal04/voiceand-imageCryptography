from PIL import Image
import numpy as np

class ImageCrypto:
    def __init__(self, qkd_key):
        self.key = self._expand_key(qkd_key)
        
    def _expand_key(self, key):
        # Convert the key to a NumPy array of uint8
        key_array = np.frombuffer(key, dtype=np.uint8)
        return key_array

    def encrypt_image(self, image_path):
        # Open the image and convert it to a NumPy array
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Flatten the image array into a 1D array
        flattened = img_array.flatten()
        
        # Repeat the key to match the length of the flattened image
        repeated_key = np.tile(self.key, (len(flattened) // len(self.key)) + 1)[:len(flattened)]
        
        # Perform bitwise XOR encryption
        encrypted = np.bitwise_xor(flattened, repeated_key)
        
        # Reshape the encrypted array back to the original image shape
        encrypted_img = encrypted.reshape(img_array.shape)
        return encrypted_img

    def decrypt_image(self, encrypted_array):
        # Flatten the encrypted image array into a 1D array
        flattened = encrypted_array.flatten()
        
        # Repeat the key to match the length of the flattened image
        repeated_key = np.tile(self.key, (len(flattened) // len(self.key)) + 1)[:len(flattened)]
        
        # Perform bitwise XOR decryption
        decrypted = np.bitwise_xor(flattened, repeated_key)
        
        # Reshape the decrypted array back to the original image shape
        decrypted_img = decrypted.reshape(encrypted_array.shape)
        return decrypted_img