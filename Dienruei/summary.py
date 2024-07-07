from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import csv
import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str, help="input transcript")
    parser.add_argument("-o", "--output", type=str, help="output summary file")
    parser.add_argument("--outputjson", type=str, help="output highlight json file")
    parser.add_argument("-t", "--timeline", type=str, help="timeline file")
    parser.add_argument("-p", "--prompt", type=str, help="prompt for generating the summary")
    args = parser.parse_args()
    
    load_dotenv()
    client = OpenAI()
    
    transcripts = []
    # PyDub handles time in millisecon
    with open(args.text) as f:
        reader = csv.DictReader(f)
        for row in reader:
            transcripts.append(row)
            
    # MESSAGE_CONTENT = "請分析以下逐字稿，並且切出「適當」的時間軸，以表格形式呈現相對應的摘要，並且與分數變化高度相關，在最後也給出您推薦的本場賽事精華的時間點(3~10個)。"
    MESSAGE_CONTENT = """Please analyze the following transcript and timelines about a specific sports game. You should determine which sports are playing.
    Also, please include USER_CONTENT to generate correct and related 3~10 highlight timelines (intervals)."""
    USER_CONTENT = """
    Please split out appropriate, and correct timelines as distributed as possible, and present the corresponding summary in table format, correlated to the score changes.
    At last, please also recommend 3~10 ordered highlight timelines of this sports game. The game starts at 0-0."""
    # USER_CONTENT = """
    # I want to watch highlights about Mike Trout.
    # """
    if args.prompt:
        USER_CONTENT = args.prompt
    
    MESSAGE_TIMELINE = ""
    if args.timeline:
        f = open(args.timeline)
        for line in f:
            MESSAGE_TIMELINE += line
        f.close()
        # print(MESSAGE_TIMELINE)

    MESSAGES = [
        # {"role": "system", "content": "你是一個得力的助手，並且可以對給定的逐字稿(有對應的時間)做出高品質的摘要。"},
        {"role": "system", "content": "You are a helpful assistant and is able to produce high-quality summary for the given transcript with timestamps."},
        {
            "role": "user", 
            "content": f"\
                {MESSAGE_CONTENT}\n\n\
                USER PROMPT:\n{USER_CONTENT}\n\n\
                TRANSCRIPTS:\n{', '.join([str(t) for t in transcripts])}\n\n\
                TIMELINES:\n{MESSAGE_TIMELINE}"
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=MESSAGES,
        temperature=0.4,
    )
    
    response_highlight = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"""
                Please extract all highlight intervals, and output them into JSON format. The format should be:
                'hightlight': [
                    (start time, end time),
                    (start time, end time),
                    ...
                ]
                
                Text: {response.choices[0].message.content}
            """}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )

    file_name = "generated_summary.md"
    if args.output:
        file_name = args.output

    # Save the text to the file
    with open(file_name, 'w') as file:
        file.write(response.choices[0].message.content)

    print(f"Generated text saved to {file_name}")
    
    json_filename = "highlight.json"
    if args.outputjson:
        json_filename = args.outputjson
    
    data = json.loads(response_highlight.choices[0].message.content)
    
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Generated highlight json saved to {json_filename}")
