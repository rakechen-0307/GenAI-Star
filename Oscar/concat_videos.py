import os

from tqdm import tqdm
os.environ["IMAGEIO_FFMPEG_EXE"] = '/opt/homebrew/bin/ffmpeg'
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_video_clips(input_video_path, output_video_path, clip_segments):
    clips = []
    video = VideoFileClip(input_video_path)

    for idx, (start_time_sec, end_time_sec) in enumerate(tqdm(clip_segments, desc="Clipping segments")):
        clip = video.subclip(start_time_sec - 0.5, end_time_sec + 0.5)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)

    final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    print(f"Concatenated video saved to {output_video_path}")