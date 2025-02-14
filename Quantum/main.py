# main.py
from qkd import BB84
from image_crypto import ImageCrypto
from Audio_crypto import VoiceCrypto  # Updated import statement
from benchmark import Benchmark
from utils.visualizer import display_images
import numpy as np
from PIL import Image
import wave  # Make sure to import wave for audio handling
from pydub import AudioSegment
from pydub.playback import play

def main():
    # QKD Process
    bb84 = BB84(key_length=29)
    alice_bits, alice_bases = bb84.generate_qubits()
    bob_bases = bb84.measure_qubits(alice_bases)
    sifted_indices = bb84.sift_keys(alice_bases, bob_bases)
    final_key = bb84.generate_final_key(sifted_indices)
    
    # Image Encryption
    crypto_image = ImageCrypto(final_key)
    encryption_time, encrypted_img = Benchmark.time_operation(
        crypto_image.encrypt_image, "input_image.png")
    
    # Image Decryption
    decryption_time, decrypted_img = Benchmark.time_operation(
        crypto_image.decrypt_image, encrypted_img)
    
    # Audio Encryption
    voice_crypto = VoiceCrypto(final_key)
    encryption_time_audio, (encrypted_audio, params) = Benchmark.time_operation(
        voice_crypto.encrypt_audio, "input_audio.wav")  # Updated class reference
    
    # Save encrypted audio
    with wave.open("encrypted_audio.wav", 'wb') as audio_file:
        audio_file.setparams(params)
        audio_file.writeframes(encrypted_audio)  # Save the encrypted audio

    # Play encrypted audio
    play_encrypted_audio(encrypted_audio, params)

    # Audio Decryption
    decryption_time_audio, (decrypted_audio_bytes, params) = Benchmark.time_operation(
        voice_crypto.decrypt_audio, encrypted_audio, params)  # Correct unpacking
    
    # Save decrypted audio
    with wave.open("decrypted_audio.wav", 'wb') as audio_file:
        audio_file.setparams(params)
        audio_file.writeframes(decrypted_audio_bytes)  # This should now work correctly

    # Benchmarking
    original_img = np.array(Image.open("input_image.png"))
    print(f"Image Encryption Time: {encryption_time:.4f}s")
    print(f"Image Decryption Time: {decryption_time:.4f}s")
    print(f"Audio Encryption Time: {encryption_time_audio:.4f}s")
    print(f"Audio Decryption Time: {decryption_time_audio:.4f}s")
    
    # Visualization
    display_images(original_img, encrypted_img, decrypted_img)

def play_encrypted_audio(encrypted_audio, params):
    # Create a new wave file for playback
    with wave.open("temp_encrypted_audio.wav", 'wb') as temp_audio_file:
        temp_audio_file.setparams(params)
        temp_audio_file.writeframes(encrypted_audio)

    # Load the audio file using pydub
    audio = AudioSegment.from_wav("temp_encrypted_audio.wav")
    play(audio)  # Play the audio

if __name__ == "__main__":
    main()