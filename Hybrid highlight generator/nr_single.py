import librosa
import noisereduce as nr
import soundfile as sf
import argparse

def noise_reduction(audio_path):
    audio_data, sample_rate = librosa.load(audio_path, sr=None)
    # Perform noise reduction
    denoised_data = nr.reduce_noise(y=audio_data, sr=sample_rate)
    amplification_factor = 2  # Adjust this value as needed

    # Amplify the denoised audio
    amplified_audio = denoised_data * amplification_factor
    return amplified_audio, sample_rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=str, help="input audio folder")
    parser.add_argument("-o", "--output", type=str, help="output transcription file")
    args = parser.parse_args()
    
    # Load the audio file
    audio_path = args.audio
    denoised_data, sample_rate = noise_reduction(audio_path)

    # Save the denoised audio to a new file
    if not args.output:
        args.output = args.input.split('.')[0] + "_denoise.wav"

    output_path = args.output
    sf.write(output_path, denoised_data, sample_rate)

    print(f"Denoised audio saved to {output_path}")
