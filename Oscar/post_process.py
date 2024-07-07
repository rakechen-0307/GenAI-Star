import json
import pickle
from matplotlib import pyplot as plt
import numpy as np

from Decibels.extract_decibels import extract_decibels

def moving_average(data, window_size):
    pad_size = (window_size - 1) // 2
    padded_data = np.pad(data, (pad_size, pad_size), mode='edge')
    moving_avg = np.convolve(padded_data, np.ones(window_size)/window_size, mode='valid')
    return moving_avg

def filter_results(results, confidences):
    filtered_results = []
    for i in range(len(results)):
        if(confidences[i] >= 0.9 and results[i] < 1):
            filtered_results.append(2 * confidences[i])
        elif(confidences[i] > 0.6):
            filtered_results.append(results[i] * 0.9)
        else:
            filtered_results.append(results[i] * confidences[i])
    
    return filtered_results  

def check_valid(results, i):
    if i == 0:
        if (results[i] == 0 or results[i+1] == 0):
            return False
    elif i == len(results) - 1:
        if (results[i] == 0 or results[i-1] == 0):
            return False
    else:
        if results[i] == 0 or results[i+1] == 0 or results[i-1] == 0:
            return False
    return True
        
def get_clip_segments(smoothed_results, threshold):
    clip_segments = []
    # print(len(results), len(smoothed_results))
    for i in range(len(smoothed_results)):
        if smoothed_results[i] > threshold:
            clip_segments.append(i)
    return clip_segments

def save_list(lst, name):
    file_path = f'{name}.pkl'

    with open(file_path, 'wb') as file:
        pickle.dump(lst, file)

    print(f'List saved to {file_path}')
    
def list_to_ranges(lst):
    config = load_json('config.json')
    merge_threshold = config['merge_threshold']
    average_decibel_per_second, third_quartile = extract_decibels(config['original_video_path'])
    
    if not lst:
        return []
    
    lst.sort()
    ranges = []
    start = lst[0]
    end = lst[0]

    for num in lst[1:]:
        if num == end + 1:
            end = num
        else:
            if ranges and (num - end) < merge_threshold:
                # Merge with the last range
                ranges[-1] = (ranges[-1][0], end)
            elif end - start > 1:
                ranges.append((start, end + 3))
            start = num
            end = num

    ranges.append((start, end))
    return ranges

def plot_results(results, figure_path, interval=1):
    x = [i * interval for i in range(len(results))]
    y = results

    plt.figure(figsize=(24, 12))
    plt.plot(x, y, marker='o')
    plt.xlabel('Time (sec)')
    plt.ylabel('Game State')
    plt.xticks(np.arange(0, max(x)+1, 20))
    plt.yticks([0, 1, 2], ['not-in-play', 'ready-to-play', 'in-play'])
    plt.title('Baseball Game State Over Time')
    plt.grid(True)
    plt.savefig(f"{figure_path}")
    
def plot_conf_results(confidences, figure_path, interval=1):
    x = [i * interval for i in range(len(confidences))]
    y = confidences

    plt.figure(figsize=(24, 12))
    plt.plot(x, y, marker='o')
    plt.xlabel('Time (sec)')
    plt.ylabel('Confidences')
    plt.xticks(np.arange(0, max(x)+1, 20))
    plt.title('Confidence Values Over Time')
    plt.grid(True)
    plt.savefig(f"{figure_path}")

def plot_all_figures(results, confidences, filtered_results, smoothed_results):
    config = load_json('config.json')
    results_path = config['results_path']
    confidences_path = config['confidences_path']
    filtered_results_path = config['filtered_results_path']
    smoothed_results_path = config['smoothed_results_path']
    
    plot_results(results, results_path, interval=1)
    plot_conf_results(confidences, confidences_path, interval=1)
    plot_conf_results(filtered_results, filtered_results_path, interval=1)
    plot_results(smoothed_results, smoothed_results_path, interval=1)
    # count = 0
    # for s in smoothed_results:
    #     if s < 1:
    #         count += 1
    # print(count)

    # plot_conf_results(clip_segments[-50:])
    # plot_conf_results(confidences[9960:9997])
    # plot_conf_results(smoothed_results[9960:9997])
    
def load_json(json_file_path):
    with open(json_file_path, 'r') as file:
        config = json.load(file)
    return config
