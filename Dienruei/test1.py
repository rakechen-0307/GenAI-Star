import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

video = cv2.VideoCapture("./baseball.mp4")
if not video.isOpened():
    print("Error: Could not open video.")
    raise

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

base64Frames = []
# while video.isOpened():
for _ in tqdm(range(frame_count), desc="Video"):
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. Generate suggestions of hightlights along with the corresponding timestamps.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    # "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)

