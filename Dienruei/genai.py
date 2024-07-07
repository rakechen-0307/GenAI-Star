import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=str, help="input video file")
    parser.add_argument("-t", "--timeline", type=str, help="timeline file")
    parser.add_argument("--denoise", type=bool, help="whether to apply denoise")
    parser.add_argument("-p", "--prompt", type=str, help="prompt for generating the summary")
    parser.add_argument("-o", "--output", type=str, help="output transcription file")
    args = parser.parse_args()
    
    try:
        folder_name = os.path.basename(args.video).split('.')[0]
        if os.system(f"python split_audio.py {args.video}") != 0: raise
        if args.denoise:
            if os.system(f"python nr_split.py outputs") != 0: raise
        if os.system("python transcript.py outputs") != 0: raise
        
        if args.timeline and args.prompt:
            if os.system(f"python summary.py transcripts.csv -t {args.timeline} -p {args.prompt}") != 0: raise
        elif args.timeline:
            if os.system(f"python summary.py transcripts.csv -t {args.timeline}") != 0: raise
        elif args.prompt:
            if os.system(f"python summary.py transcripts.csv -p {args.prompt}") != 0: raise
        else:
            if os.system("python summary.py transcripts.csv") != 0: raise
        
        
        
        os.makedirs(folder_name)
        if os.system(f"mv outputs {folder_name}/") != 0: raise
        if os.system(f"mv transcripts.csv {folder_name}/") != 0: raise
        if os.system(f"mv generated_summary.md {folder_name}/") != 0: raise
        if os.system(f"mv highlight.json {folder_name}/") != 0: raise
    except:
        print("\nDetected Ctrl-C! Performing cleanup before exit...")
        os.system("rm -rf outputs")
        os.system(f"rm {folder_name}_audio.wav")
        os.system(f"rm -rf {folder_name}")
        print("Cleanup done. Exiting program.")
        
        
        