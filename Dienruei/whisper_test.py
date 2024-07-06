from openai import OpenAI
from dotenv import load_dotenv
import argparse
from tqdm import tqdm

load_dotenv()
client = OpenAI()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=str, help="input audio folder")
    args = parser.parse_args()
    
    audio_file = open(args.audio, "rb")
    transcript = client.audio.transcriptions.create(
        prompt="sports commentator narrates a table tennis game",
        file=audio_file,
        model="whisper-1",
        # language='zh',
        # response_format="verbose_json",
        # timestamp_granularities=["word"]
    )
    print(transcript.text)
  