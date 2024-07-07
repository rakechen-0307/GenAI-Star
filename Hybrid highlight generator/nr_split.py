import librosa
import noisereduce as nr
import soundfile as sf
import argparse
import os
from tqdm import tqdm
import numpy as np

from lib.utils import get_all_files

def noise_reduction(audio_path):
    audio_data, sample_rate = librosa.load(audio_path, sr=None)
    # Perform noise reduction
    denoised_data = nr.reduce_noise(y=audio_data, sr=sample_rate, n_fft=512, prop_decrease=0.4)
    amplification_factor = 2  # Adjust this value as needed

    # Amplify the denoised audio
    amplified_audio = denoised_data * amplification_factor
    amplified_audio = np.clip(amplified_audio, -1.0, 1.0)
    return amplified_audio, sample_rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=str, help="input audio folder")
    args = parser.parse_args()
    
    folder_path = args.audio
    audio_files = [args.audio + '/' + path for path in get_all_files(folder_path)]
    # print(audio_files)
    audio_files = sorted(audio_files)
    
    for audio_filename in tqdm(audio_files, desc='Processing audio'):        
        denoised_data, sample_rate = noise_reduction(audio_filename)
        output_path = audio_filename
        sf.write(output_path, denoised_data, sample_rate)
        
    print(f"Denoise audiowaves in {args.audio} successfully")
    