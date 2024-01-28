"""Bulk trim silence from all mp3 files in the folder of the script, including subfolders."""
"""Modified from https://sound.stackexchange.com/questions/52246/how-can-i-batch-remove-trailing-silence-from-audio-files"""

import os
import numpy as np
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor

# Noise floor in dB
NOISE_FLOOR = -60

# Trim silence from start?
TRIM_START = True

# Trim silence from end?
TRIM_END = True

# Padding to apply around detected edge of silence
PADDING = 32

epsilon = 10 ** (NOISE_FLOOR / 20)


def process(filename):
    print(f"Processing file: {filename}")
    # Load the mp3 file
    data, samplerate = sf.read(filename, always_2d=True)
    # Find indices of samples above noise floor
    indices = (np.abs(data) >= epsilon).any(axis=1).nonzero()[0]
    # Trim silence (if it found any non-silent samples)
    if len(indices) > 1:
        # Find start and end index to trim (+/- padding)
        start_index = max(0, indices[0] - PADDING) if TRIM_START else 0
        end_index = min(len(data), indices[-1] + PADDING) if TRIM_END else len(data)
        
        # Calculate the amount of silence trimmed at the start
        start_trimmed = indices[0] / samplerate if TRIM_START else 0.0
        
        # Calculate the amount of silence trimmed at the end
        end_trimmed = (len(data) - indices[-1]) / samplerate if TRIM_END else 0.0
        
        # Trim the data
        trimmed_data = data[start_index:end_index]
        
        print(f"Trimmed {start_trimmed:.2f} seconds of silence at the start.")
        print(f"Trimmed {end_trimmed:.2f} seconds of silence at the end.")
    else:
        trimmed_data = data
        print("No silence detected. File remains unchanged.")
    
    # Write trimmed mp3, replacing the original file
    sf.write(filename, trimmed_data, samplerate)
    print("Trimming completed.")


if __name__ == "__main__":
    # List all mp3 files
    mp3_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))

    # Process files in parallel, uses all threads
    with ThreadPoolExecutor() as executor:
        executor.map(process, mp3_files)