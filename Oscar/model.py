import torch
from tqdm import tqdm
from ultralytics import YOLO

from post_process import load_json

json_file_path = 'config.json'

config = load_json(json_file_path)

RUN_DIR = config['RUN_DIR']

model = YOLO(f"{RUN_DIR}/in-play-classifier-model.pt")
scoreboard_model = YOLO(f'{RUN_DIR}/scoreboard-detection-model.pt')

def predict(img):
    labels = ['in-play', 'not-in-play', 'ready-to-play']
    results = model.predict(img, verbose=False)
    max_index = torch.argmax(results[0].probs.data).item()
    return labels[max_index]

def detect_scoreboard(img):
    detections = scoreboard_model.predict(img, verbose=False)
    if detections[0].boxes.conf.numel() > 0:
        confidences_np = detections[0].boxes.conf.cpu().numpy()
        confidences = confidences_np[0]
    else:
        confidences = 0
    return confidences

label_to_num = {
    'not-in-play': 0,
    'ready-to-play': 1,
    'in-play': 2
}

def classify_frames(frames):
    results = []
    confidences = []
    count = 0
    for frame in tqdm(frames, desc="Classifying frames"):
        count += 1
        confidence = detect_scoreboard(frame)
        confidences.append(confidence)
        label = predict(frame)
        results.append(label_to_num[label])
    return results, confidences