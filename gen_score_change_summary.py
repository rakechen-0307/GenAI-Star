import pickle
import os

import cv2

def get_highlight_secs(highlight_sec, frame_count, fps, total_sec=50, left_ratio=0.5, right_ratio=0.5):
    # check if the highlight_sec_next_frame will exceed the total frame count
    if highlight_sec + total_sec*right_ratio >= int(frame_count / fps):
        highlight_sec = int(frame_count / fps) - total_sec
        highlight_sec_next_frame = int(frame_count / fps)
    # check if the highlight_sec will be negative
    elif highlight_sec - total_sec*left_ratio < 0:
        highlight_sec = 0
        highlight_sec_next_frame = total_sec
    else:
        highlight_sec = highlight_sec - total_sec*left_ratio
        highlight_sec_next_frame = highlight_sec + total_sec
    highlight_sec, highlight_sec_next_frame = int(highlight_sec), int(highlight_sec_next_frame)
    return highlight_sec, highlight_sec_next_frame

def gen_score_change_summary(highlight_idx, scoreboard, innings, frame_count, fps, sec=40, frames_dir="./frames"):
    frames = sorted(os.listdir(frames_dir))
    summary = ""
    # get the seconds of the highlight
    highlight_secs = []
    for count, idx in enumerate(highlight_idx):
        if count == len(highlight_idx) - 1:
            break
        highlight_sec = int(frames[idx].split(".")[0]) * sec
        highlight_sec, highlight_sec_next_frame = get_highlight_secs(highlight_sec, frame_count, fps)
        highlight_secs.append((highlight_sec, highlight_sec_next_frame))
        # turn the time into the format of "00:00:00"
        highlight_sec = f"{highlight_sec//3600:02d}:{(highlight_sec%3600)//60:02d}:{highlight_sec%60:02d}"
        highlight_sec_next_frame = f"{highlight_sec_next_frame//3600:02d}:{(highlight_sec_next_frame%3600)//60:02d}:{highlight_sec_next_frame%60:02d}"
        # scoreboards are in the format of "1-2" or "2-1" or "0-0" etc.
        # check if it is top inning or bottom inning by checking if the score changes in the first character or the last character.
        # for example, if the score changes from "1-2" to "2-2", it is the top inning.
        # if the score changes from "2-2" to "2-3", it is the bottom inning.
        if scoreboard[count].split("-")[0] != scoreboard[count+1].split("-")[0]:
            innings[count] = "Top " + innings[count]
        elif scoreboard[count].split("-")[1] != scoreboard[count+1].split("-")[1]:
            innings[count] = "Bottom " + innings[count]
        summary += f"Score change time: {highlight_sec} ~ {highlight_sec_next_frame} --- score: {scoreboard[count]} => {scoreboard[count+1]}, Innings: {innings[count]}\n"
    print(summary)
    return summary, highlight_secs

if __name__ == "__main__":
    with open("highlight_idx.pkl", "rb") as f:
        highlight_idx = pickle.load(f)
    with open("highlight_scoreboard.pkl", "rb") as f:
        scoreboard = pickle.load(f)
    with open("highlight_innings.pkl", "rb") as f:
        innings = pickle.load(f)

    print(highlight_idx)
    print(scoreboard)
    print(innings)
    
    sec = 40
    video_file = "./Decibels/videos/baseball_full.mp4"
    video = cv2.VideoCapture(video_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_cnt = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print(isinstance(True, int))
    frames_dir = "./frames" 
    summary, highlight_secs = gen_score_change_summary(highlight_idx, scoreboard, innings, frame_cnt, fps, sec, frames_dir)