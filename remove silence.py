# Modified from https://sound.stackexchange.com/questions/52246/how-can-i-batch-remove-trailing-silence-from-audio-files

# Bulk trim silence from mp3 audio files with many settings to customize
""" TODO: 
    support for more audio types
    choose specific folder to save trimmed versions to
    (?) choose new name of files [eg Rickroll_trimmed.mp3] and place in same/specific directory
    audio types to scan for
    !! save other metadata such as lyrics and comments
"""


import os
import numpy as np
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def print_friendly(prefix, message):
    print(f"({prefix}): " + message)


def process(filepath, trim_start, trim_end, padding, noise_floor, replace_files, min_silence_duration, save_metadata):
    filename = os.path.basename(filepath)
    print(f"Processing file: {filepath}")
    
    # Load the mp3 file and its metadata
    data, samplerate = sf.read(filepath, always_2d=True)
    original_audio = MP3(filepath, ID3=EasyID3)
    
    # Find indices of samples above noise floor
    epsilon = 10 ** (noise_floor / 20)
    indices = (np.abs(data) >= epsilon).any(axis=1).nonzero()[0]
    
    # Trim silence (if any non-silent samples are found)
    if len(indices) > 1:
        # Find start and end index to trim (+/- padding)
        start_index = max(0, indices[0] - padding) if trim_start else 0
        end_index = min(len(data), indices[-1] + padding) if trim_end else len(data)
        
        # Calculate the duration of silence trimmed at the start and end
        start_trimmed_duration = indices[0] / samplerate if trim_start else 0.0
        end_trimmed_duration = (len(data) - indices[-1]) / samplerate if trim_end else 0.0
        
        if start_trimmed_duration >= min_silence_duration:
            trimmed_data = data[start_index:end_index]
            print_friendly(filename, f"Trimmed {start_trimmed_duration:.2f} seconds of silence at the start.")
        else:
            trimmed_data = data
            print_friendly(filename, f"Start silence duration ({start_trimmed_duration:.2f} seconds) is less than the minimum threshold ({min_silence_duration} seconds).")
        
        if end_trimmed_duration >= min_silence_duration:
            trimmed_data = data[start_index:end_index]
            print_friendly(filename, f"Trimmed {end_trimmed_duration:.2f} seconds of silence at the end.")
        else:
            trimmed_data = data
            print_friendly(filename, f"End silence duration ({end_trimmed_duration:.2f} seconds) is less than the minimum threshold ({min_silence_duration} seconds).")

    
    # Determine the destination path for the trimmed file
    if replace_files:
        trimmed_filepath = filepath
    else:
        trimmed_filename = os.path.basename(filepath)
        if destination_folder:
            trimmed_filepath = os.path.join(destination_folder, trimmed_filename)
        else:
            trimmed_filepath = os.path.join("trimmed", trimmed_filename)
    
    # Write the trimmed audio data to the destination file
    sf.write(trimmed_filepath, trimmed_data, samplerate)
    print_friendly(filename, "Trimming completed.")

    # Save metadata if requested
    if save_metadata and filepath.lower().endswith('.mp3'):
        print_friendly(filename, "Copying metadata to trimmed file.")
        trimmed_audio = MP3(trimmed_filepath, ID3=EasyID3)
        trimmed_audio.update(original_audio)
        trimmed_audio.save()


if __name__ == "__main__":
    # Options for the user
    current_directory = os.getcwd()
    folder_to_scan = input(f"Which directory should be scanned for audio files? ({os.getcwd()}): ")
    if folder_to_scan:
        if not os.path.isdir(folder_to_scan):
            print("Error: The specified directory does not exist")
            exit()
    else:
        folder_to_scan = current_directory

    scan_subdirectories = input("Scan subdirectories? (Y/n): ").lower() == 'y'
    save_metadata = input("Save audio metadata? (Y/n): ").lower() == 'y'
    replace_files = input("Replace original files with trimmed versions? (y/N): ").lower() == 'y'
    if not replace_files:
        default_destination = os.path.join(os.getcwd(), "trimmed")
        destination_folder = input(f"Enter the directory to save trimmed files ({default_destination}): ") or default_destination
        destination_folder = os.path.abspath(destination_folder)
        os.makedirs(destination_folder, exist_ok=True)
    else:
        destination_folder = None


    trim_start = input("Trim silence from the start of the audio files? (Y/n): ").lower() == 'y'
    trim_end = input("Trim silence from the end of the audio files? (Y/n): ").lower() == 'y'
    minimum_duration = float(input("Enter the minimum duration of silence to be trimmed (1.0): ") or 1.0)
    padding = int(input("Enter the padding to apply around detected edge of silence (32): ") or 32)
    noise_floor = int(input("Enter the noise floor for silence in dB (-60): ") or -60)
    num_threads = int(input(f"Enter the number of threads to use for parallel processing (1): ") or 1)
    if (num_threads > multiprocessing.cpu_count()):
        print(f"Error: Allocated more threads than the system has available ({multiprocessing.cpu_count()} threads)")
        exit()

    # Reverse boolean to make the default "true" instead
    trim_start = trim_start != 'n'
    trim_end = trim_end != 'n'
    scan_subdirectories = scan_subdirectories != 'n'
    save_metadata = save_metadata != 'n'

    print("Scanning directory:", folder_to_scan)

    # Find all mp3 files in the specified directory
    mp3_files = []
    if scan_subdirectories:
        for root, dirs, files in os.walk(folder_to_scan):
            for file in files:
                if file.endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_to_scan):
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(folder_to_scan, file))

    print("Found", len(mp3_files), "MP3 files in the directory.")

    # Process files in parallel (if user chooses to multithread)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process, mp3_files, [trim_start] * len(mp3_files), [trim_end] * len(mp3_files), [padding] * len(mp3_files), [noise_floor] * len(mp3_files), [replace_files] * len(mp3_files), [minimum_duration] * len(mp3_files), [save_metadata] * len(mp3_files))

    print("Done processing! :3")