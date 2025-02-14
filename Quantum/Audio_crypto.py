import numpy as np
import wave
import matplotlib.pyplot as plt
import random

class VoiceCrypto:
    def __init__(self, qkd_key):
        self.key = self._expand_key(qkd_key)

    def _expand_key(self, key):
        key_array = np.frombuffer(key, dtype=np.uint8)
        return key_array

    def encrypt_audio(self, audio_path):
        with wave.open(audio_path, 'rb') as audio_file:
            params = audio_file.getparams()
            frames = audio_file.readframes(params.nframes)
            audio_array = np.frombuffer(frames, dtype=np.int16)

        # Repeat the key to match the length of the audio array
        repeated_key = np.tile(self.key, (len(audio_array) // len(self.key)) + 1)[:len(audio_array)]

        # Perform bitwise XOR encryption
        encrypted = np.bitwise_xor(audio_array, repeated_key)

        # Add significant random noise
        noise = np.random.randint(-5000, 5000, size=encrypted.shape, dtype=np.int16)
        encrypted = np.clip(encrypted + noise, -32768, 32767)

        # Frequency domain manipulation
        freq_data = np.fft.fft(encrypted)
        # Randomly modify frequency components
        for i in range(len(freq_data)):
            if random.random() < 0.5:  # 50% chance to modify
                freq_data[i] *= random.uniform(0.5, 1.5)  # Randomly scale frequency component

        # Convert back to time domain
        encrypted = np.fft.ifft(freq_data).real.astype(np.int16)

        return encrypted, params

    def decrypt_audio(self, encrypted_array, params):
        repeated_key = np.tile(self.key, (len(encrypted_array) // len(self.key)) + 1)[:len(encrypted_array)]
        decrypted = np.bitwise_xor(encrypted_array, repeated_key)

        # Attempt to remove noise (this is a naive approach)
        noise_estimate = np.mean(np.random.randint(-5000, 5000, size=decrypted.shape, dtype=np.int16))
        decrypted = np.clip(decrypted - noise_estimate, -32768, 32767)

        return decrypted.tobytes(), params

    def plot_waveform(self, audio_data, title):
        plt.figure(figsize=(10, 4))
        plt.plot(audio_data)
        plt.title(title)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.grid()
        plt.show()

    def visualize_audio(self, original_audio_path, encrypted_audio_array, decrypted_audio_bytes, params):
        with wave.open(original_audio_path, 'rb') as audio_file:
            original_frames = audio_file.readframes(audio_file.getnframes())
            original_audio_array = np.frombuffer(original_frames, dtype=np.int16)
            self.plot_waveform(original_audio_array, 'Original Audio')

        self.plot_waveform(encrypted_audio_array, 'Encrypted Audio')

        decrypted_audio_array = np.frombuffer(decrypted_audio_bytes, dtype=np.int16)
        self.plot_waveform(decrypted_audio_array, 'Decrypted Audio')