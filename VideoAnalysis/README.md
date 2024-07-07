# Video Analysis

This project analyzes sports videos to generate highlights and summaries. It uses a YOLO model for detecting scoreboards and other elements within the video. This can generate a summary of the score changes in the game.

## Setup

1. Add a `.env` file with your API key:

   ```plaintext
   API_KEY=your_api_key_here
   ```

## Running the Analysis

To run the video analysis, use the following command:

```bash
python video_analysis.py --sports <sports> --ckpt_file <scoreboard_yolo_checkpoint_model> --video_file <video_to_process>
```

This will generate a summary of the video analysis in ./data/{sports}/summary.txt.

Also, it will generate a video with the detected score change fragments in ./videos/{filename}\_highlight.mp4.
