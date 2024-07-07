import cv2
from tqdm import tqdm

fps = 29.97
def extract_frames(video_path, interval=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    success, frame = cap.read()
    count = 0
    current_sec = 1

    with tqdm(total=total_frames_count, desc="Extracting frames") as pbar:
        while success:
            if count > fps * current_sec:
                frames.append(frame)
                current_sec += 1
            success, frame = cap.read()
            count += 1
            pbar.update(1)

    cap.release()
    return frames