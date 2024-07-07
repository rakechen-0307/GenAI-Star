import os
from tqdm import tqdm

from post_process import load_json
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
    
def get_video_duration(video_path):
    # Load the video file
    clip = VideoFileClip(video_path)

    # Get the duration in seconds
    duration = clip.duration

    # Convert duration to hours, minutes, and seconds
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)

    # Print the duration
    print(f"Video Duration: {hours}h {minutes}m {seconds}s")

    # Close the clip to release resources
    clip.close()