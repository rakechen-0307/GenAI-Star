import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input video file")
    parser.add_argument("-o", "--output", type=str, help="output video file")
    args = parser.parse_args()
    
    if not args.output:
        args.output = args.input.split('.')[-2] + "_audio.wav"
    
    os.system(f"ffmpeg -i {args.input} -q:a 0 -map a {args.output}")
    
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    os.system(f"ffmpeg -i {args.output} -f segment -segment_time 15 -c copy outputs/output_segment_%03d.wav")