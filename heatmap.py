import os

import matplotlib.pyplot as plt
import numpy as np

def create_heatmap(data):
    data = _preprocess(data)

    plt.imshow(data, cmap='autumn_r', interpolation='nearest')
    plt.colorbar(label="Deepfake Speech Likelihood")
    plt.title("Deepfake Speech Heatmap")
    plt.xlabel("Video Timeline (minutes)")
    plt.xticks([])
    plt.yticks([])
    plt.savefig('heatmap.png', bbox_inches='tight')

def delete_heatmap():
    os.remove("heatmap.png")

def _preprocess(data):
    data = np.array(data)
    data = np.expand_dims(data, axis=0)

    return data