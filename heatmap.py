import os
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np

def create_heatmap(data):
    """generate matplotlib heatmap of the segmented prediction output of the prediciton job 
    """
    # format xticks
    end = len(data) - 1
    mid = int(end/2)
    xticks = [0, mid, end]
    labels = [_to_date_string(x) for x in xticks]


    data = _preprocess(data)

    plt.imshow(data, cmap='RdYlGn_r', interpolation='nearest')
    plt.title("Deepfake Speech Heatmap")
    
    plt.xlabel("Video Timeline")
    plt.xticks(xticks, labels)
    plt.yticks([])
    # plt.colorbar(label="Key: Deepfake Speech Likelihood", orientation="horizontal", location="top")
    plt.savefig('heatmap.png', bbox_inches='tight')

def delete_heatmap():
    os.remove("heatmap.png")

def _to_date_string(index):
    """produces a 00:00 (minutes:seconds) format given the index of embedding list
    """
    time = str(timedelta(seconds=index * 3))
    h,m,s = time.split(":")
    if h != "0":
        return time
    return f"{m}:{s}"

def _preprocess(data):
    data = np.array(data, dtype=np.float32)
    data = np.expand_dims(data, axis=0)

    return data