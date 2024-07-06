from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import csv
import os
import argparse
from tqdm import tqdm

from lib.utils import get_all_files

load_dotenv()
client = OpenAI()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=str, help="input audio folder")
    parser.add_argument("-o", "--output", type=str, help="output transcription file")
    args = parser.parse_args()
    
    # Example usage
    folder_path = args.audio
    audio_files = [args.audio + '/' + path for path in get_all_files(folder_path)]
    # print(audio_files)
    audio_files = sorted(audio_files)

    transcripts = []
    
    start, end = 0*60*1000, 0.25*60*1000
    
    for audio_filename in tqdm(audio_files, desc='Processing audio'):
        audio_file = open(audio_filename, "rb")
        transcript = client.audio.transcriptions.create(
            prompt="sports commentator narrates a specific sports game",
            file=audio_file,
            model="whisper-1",
            # language='zh',
            # response_format="verbose_json",
            # timestamp_granularities=["word"]
        )
        
        # print(transcript.words)
        print(audio_filename)
        print(transcript.text)
        texttime = str(int(start//60000)) + ":" + str(int((start % 60000) / 1000))
        transcripts.append((texttime, transcript.text))
        # print(transcripts)
        start, end = end, end + 0.25*60*1000
        
        with open("transcripts.csv", 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['start', 'transcript'])
            writer.writeheader()
            for transcript in transcripts:
                writer.writerow({
                    'start': str(int(transcript[0].split(':')[0])//60) + ":" + str(int(transcript[0].split(':')[0])%60) + ":" + transcript[0].split(':')[1], 
                    'transcript': transcript[1]
                })
        
        print("Audio transcripted into transcripts.csv")
        