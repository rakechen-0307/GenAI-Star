import os
import moviepy.editor as mp

def extract_hightlight(filename, hightlights_secs):
    video = mp.VideoFileClip(filename)
    merge_hightlights(hightlights_secs)
    # extract the hightlights from the video
    highlight_clips = []
    for start, end in hightlights_secs:
        highlight_clips.append(video.subclip(start, end))

    # concatenate the hightlights
    highlight_video = mp.concatenate_videoclips(highlight_clips)
    highlight_video.write_videofile(f"{filename}_highlight.mp4", codec="libx264")

def merge_hightlights(hightlights_in_seconds):
    idx = 0
    threshold = 1
    while idx < len(hightlights_in_seconds) - 1:
        start1, end1 = hightlights_in_seconds[idx]
        start2, end2 = hightlights_in_seconds[idx + 1]
        if start2 - end1 < threshold:
            hightlights_in_seconds[idx] = (start1, end2)
            hightlights_in_seconds.pop(idx + 1)
        else:
            idx += 1
    return hightlights_in_seconds

if __name__ == "__main__":
    filename = "./Decibels/videos/US_Japan_baseball_full.mp4"
    hightlights_secs = [(2760, 3000)]
    extract_hightlight(filename, hightlights_secs)