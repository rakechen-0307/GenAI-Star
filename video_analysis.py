import os
import cv2
import torch
import numpy as np
import ultralytics
from ultralytics import YOLO
import google.generativeai as genai

API_KEY = "AIzaSyALB7z-U4DcPDZ_lwMyXL636LmR_L9ppas"
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

ckpt_file = "scoreboard.pt"
video_file = "./videos/baseball.mp4"
tmp_frames_dir = "./frames_tmp"

yolo_model = YOLO(ckpt_file)
video = cv2.VideoCapture(video_file)
fps = video.get(cv2.CAP_PROP_FPS)
os.system("rm -r {}".format(tmp_frames_dir))
os.mkdir(tmp_frames_dir)

## extract frames
count = 1
img_num = 0
sec = 20
success, image = video.read()
while success:
    if (count % (fps*sec) == 0):
        if (img_num < 10):
            output_num = "000" + str(img_num)
        elif (img_num < 100):
            output_num = "00" + str(img_num)
        elif (img_num < 1000):
            output_num = "0" + str(img_num)
        else:
            output_num = str(img_num)
        img_file = tmp_frames_dir + "/" + str(output_num) + ".jpg"
        cv2.imwrite(img_file, image)
        img_num += 1
    success, image = video.read()
    count += 1

## scoreboard detection
frames_dir = "./frames"
os.system("rm -r {}".format(frames_dir))
os.mkdir(frames_dir)
low, high = 0, 0
scoreboard_pos = []
frames = sorted(os.listdir(tmp_frames_dir))
for i in range(len(frames)):
    target_img = tmp_frames_dir + "/" + frames[i]
    detect_result = yolo_model.predict(source=target_img, conf=0.5, verbose=False)
    classes = torch.Tensor.numpy(detect_result[0].boxes.xyxy.cpu())
    confidence = torch.Tensor.numpy(detect_result[0].boxes.conf.cpu())
    if (len(classes) > 0):
        os.system("mv {tmp} {out}".format(
            tmp=target_img,
            out=frames_dir
        ))
        scoreboard_pos.append(np.ndarray.tolist(classes[np.argmax(confidence)]))
os.system("rm -r {}".format(tmp_frames_dir))

print(scoreboard_pos[0])

## ask LLM
def askLLMLeft(target, ref):
    if (target <= ref):
        answer = target
    else:
        os.system("rm -r ./scoreboard")
        os.mkdir("./scoreboard")
        target_file = frames_dir + "/" + frames[target]
        ref_file = frames_dir + "/" + frames[ref]

        # crop scoreboard
        target_img = cv2.imread(target_file)
        ref_img = cv2.imread(ref_file)
        cropped_target = target_img[int(scoreboard_pos[target][1]):int(scoreboard_pos[target][3]), int(scoreboard_pos[target][0]):int(scoreboard_pos[target][2])]
        cropped_ref = ref_img[int(scoreboard_pos[ref][1]):int(scoreboard_pos[ref][3]), int(scoreboard_pos[ref][0]):int(scoreboard_pos[ref][2])]
        cropped_target_file = "./scoreboard/target.jpg"
        cropped_ref_file = "./scoreboard/ref.jpg"
        cv2.imwrite(cropped_target_file, cropped_target)
        cv2.imwrite(cropped_ref_file, cropped_ref)

        # LLM
        reference_scoreboard = genai.upload_file(path=cropped_ref_file, display_name="reference scoreboard")
        response1 = gemini_model.generate_content(["This is a scoreboard of a baseball game, please give me the information on the scoreboard using the following format: [scores(x:x),inning(x),outs(x)]", reference_scoreboard])
        print(response1.text)

        target_scoreboard = genai.upload_file(path=cropped_target_file, display_name="target scoreboard")
        response2 = gemini_model.generate_content(["This is a scoreboard of a baseball game, please give me the information on the scoreboard using the following format: [scores(x:x),inning(x),outs(x)]", target_scoreboard])
        print(response2.text)

        # the output should be "True" or "False"
        answer = response

    return answer

def askLLMRight(target, ref):
    if (target >= ref):
        answer = target

    return answer

def binarySearch(low, high, highlight_idx):
    mid = (low + high) // 2
    answer_l = askLLMLeft(mid, low)
    answer_r = askLLMRight(mid, high)

    if (answer_l != True and answer_l != False):
        highlight_idx.append(answer_l)
    elif (answer_l == True):
        binarySearch(low, mid, highlight_idx)
    
    if (answer_r != True and answer_r != False):
        highlight_idx.append(answer_r)
    elif (answer_l == True):
        binarySearch(mid + 1, high, highlight_idx)


askLLMLeft(len(frames)-1, 0)