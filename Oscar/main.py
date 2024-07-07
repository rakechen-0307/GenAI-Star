from concat_videos import concatenate_video_clips
from extract_frames import extract_frames
from model import classify_frames
from post_process import filter_results, get_clip_segments, list_to_ranges, load_json, moving_average, plot_all_figures, plot_conf_results, plot_results

        
json_file_path = 'config.json'

config = load_json(json_file_path)

video_path = config['original_video_path']
output_video_path = config['output_video_path']
RUN_DIR = config['RUN_DIR']

frames = extract_frames(video_path, interval=1)

print(len(frames))
results, confidences = classify_frames(frames)
smoothed_confidences = moving_average(confidences, 3)
filtered_results =  filter_results(results, confidences)

window_size = 7
smoothed_results = moving_average(filtered_results, window_size)

threshold = 1
clip_segments = get_clip_segments(smoothed_results, threshold)
print(clip_segments[-50:])
clip_segments = list_to_ranges(clip_segments)
print(f"Clip segments: {clip_segments}")

# Concatenate video clips
concatenate_video_clips(video_path, output_video_path, clip_segments)

# Plot results
plot_all_figures(results, confidences, filtered_results, smoothed_results)

