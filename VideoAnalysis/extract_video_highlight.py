import os
import json
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
    filename = "./videos/Mexico_Japan_baseball_full.mp4"
    with open("./data/baseball/highlight.json", "r") as f:
        hightlights_json = json.load(f)

    hightlights_secs = []
    # turn the time from format of "00:00:00" to seconds
    for highlight_secs in hightlights_json["highlight"]:
        start = int(highlight_secs[0].split(":")[0]) * 3600 + int(highlight_secs[0].split(":")[1]) * 60 + int(highlight_secs[0].split(":")[2])
        end = int(highlight_secs[1].split(":")[0]) * 3600 + int(highlight_secs[1].split(":")[1]) * 60 + int(highlight_secs[1].split(":")[2])
        hightlights_secs.append((start, end))

    # sort the hightlights by the start time
    hightlights_secs.sort(key=lambda x: x[0])
    print(hightlights_secs)
    extract_hightlight(filename, hightlights_secs)