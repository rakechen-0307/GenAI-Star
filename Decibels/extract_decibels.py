import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np
from tqdm import tqdm

# Step 1: Extract audio from video
def extract_decibels(filename):
    video = mp.VideoFileClip(filename)
    audio = video.audio
    audio.write_audiofile(f"{filename}_audio.wav")

    # Step 2: Load audio and analyze decibel levels
    audio_name = f"{filename}_audio.wav"
    audio_segment = AudioSegment.from_file(audio_name)

    # Function to calculate RMS value
    def calculate_rms(frame):
        samples = np.array(frame.get_array_of_samples(), dtype=np.int32)
        return np.sqrt(np.mean(samples**2))

    # Function to convert RMS to decibel
    def rms_to_db(rms):
        if rms == 0:
            return 0
        return 20 * np.log10(rms)

    # Calculate decibel levels for each frame
    def calculate_videoDB(audio_segment, frame_count, segment_duration) -> np.ndarray:
        decibel_levels = []
        for i in range(frame_count):
            frame = audio_segment[i * segment_duration:(i + 1) * segment_duration]
            rms = calculate_rms(frame)
            db = rms_to_db(rms)
            decibel_levels.append(db)
        return np.array(decibel_levels)

    frame_rate = video.fps
    segment_duration = (1000 / frame_rate)
    frame_count = int(len(audio_segment) / segment_duration)

    decibel_levels = calculate_videoDB(audio_segment, frame_count, segment_duration)
    # calculate the average every fps seconds
    total_secs = int(len(decibel_levels) // frame_rate)
    average_decibel_per_second = []
    for i in tqdm(range(total_secs)):
        start = round(i * frame_rate)
        end = round((i + 1) * frame_rate)
        average_decibel_per_second.append(np.mean(decibel_levels[start:end]))
    
    # get the third quartile of the decibel levels
    third_quartile = np.percentile(average_decibel_per_second, 75)

    return average_decibel_per_second, third_quartile

if __name__ == "__main__":
    print(extract_decibels("../VideoAnalysis/videos/table_tennis_full.mp4"))