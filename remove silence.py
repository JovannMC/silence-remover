"""Bulk trim silence from all mp3 files in the folder of the script, including subfolders."""
"""Modified from https://sound.stackexchange.com/questions/52246/how-can-i-batch-remove-trailing-silence-from-audio-files"""
""" TODO: 
    support for more audio types
    audio types to scan for
    scan subdirectories
    minimum seconds for it to trim part of song
    add a :3
"""


import os
import numpy as np
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def process(filename, trim_start, trim_end, padding, replace_files):
    print(f"Processing file: {filename}")
    
    # Load the mp3 file and its metadata
    data, samplerate = sf.read(filename, always_2d=True)
    original_audio = MP3(filename, ID3=EasyID3)
    
    # Find indices of samples above noise floor
    epsilon = 10 ** (-60 / 20)
    indices = (np.abs(data) >= epsilon).any(axis=1).nonzero()[0]
    
    # Trim silence (if any non-silent samples are found)
    if len(indices) > 1:
        # Find start and end index to trim (+/- padding)
        start_index = max(0, indices[0] - padding) if trim_start else 0
        end_index = min(len(data), indices[-1] + padding) if trim_end else len(data)
        
        # Calculate the amount of silence trimmed at the start and end
        start_trimmed = indices[0] / samplerate if trim_start else 0.0
        end_trimmed = (len(data) - indices[-1]) / samplerate if trim_end else 0.0
        
        # Trim the audio data
        trimmed_data = data[start_index:end_index]
        
        print(f"Trimmed {start_trimmed:.2f} seconds of silence at the start.")
        print(f"Trimmed {end_trimmed:.2f} seconds of silence at the end.")
    else:
        trimmed_data = data
        print("No silence detected. File remains unchanged.")
    
    # Determine the destination path for the trimmed file
    if replace_files:
        trimmed_filename = filename
    else:
        trimmed_filename = os.path.join("trimmed", os.path.basename(filename))
        os.makedirs("trimmed", exist_ok=True)
    
    # Write the trimmed audio data to the destination file
    sf.write(trimmed_filename, trimmed_data, samplerate)
    print("Trimming completed.")

    # Preserve metadata for MP3 files
    if filename.lower().endswith('.mp3'):
        trimmed_audio = MP3(trimmed_filename, ID3=EasyID3)
        trimmed_audio.update(original_audio)
        trimmed_audio.save()

if __name__ == "__main__":
    # Prompt the user for options
    trim_start = input("Trim silence from the start of the audio files? (y/n): ").lower() == 'y'
    trim_end = input("Trim silence from the end of the audio files? (y/n): ").lower() == 'y'
    padding = int(input("Enter the padding to apply around detected edge of silence (default is 32): ") or 32)
    num_threads = int(input("Enter the number of threads to use for parallel processing (default is CPU count): ")
                      or multiprocessing.cpu_count())
    replace_files = input("Replace original files with trimmed versions? (y/n): ").lower() == 'y'

    # List all mp3 files
    mp3_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process, mp3_files, [trim_start] * len(mp3_files), [trim_end] * len(mp3_files), [padding] * len(mp3_files), [replace_files] * len(mp3_files))
