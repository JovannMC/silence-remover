# silence-remover
I needed a way to trim out the silence from the beginning and end of many audio files I had, but didn't find a decent solution that was *free*. So I did it myself (*kind of*), thanks internet!<br>
<br>
Anyways most people won't need this project, you should really use and learn [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#silenceremove) instead.

## Description
It's *self-explanatory*; the script trims out silence from the beginning and/or the end of audio files and then saves them either in a trimmed folder, or replaces the original file.<br>
<br>
The program is **customizable** and has **various settings** to mess with from specifying the amount of **threads allocated** to changing the **minimum duration** of silence needed to trim.

## Features
- Scan a specific directory
  - **Default:** current directory
- Scan subdirectories
  - **Default:** no
- Save audio files' metadata
  - **Default:** yes
- Trim silence from the beginning, end, or both
  - **Default:** both
- Specify amount of threads allocated to program
  - **Default:** 1
- Replace original files with trimmed versions
  - **Default:** no
- Specify path to place trimmed files (*if replacing*)
  - **Default:** /trimmed
- Specify minimum duration of silence to trim
  - **Default:** 1.0 seconds
- Change padding around the detected silence
  - **Default:** 32 samples
- Change noise floor of silence
  - **Default:** -64 db

## Acknowledgements
* [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#silenceremove) - the project you should really use and learn instead for anything media
* [Original script](https://sound.stackexchange.com/questions/52246/how-can-i-batch-remove-trailing-silence-from-audio-files) - the StackExchange post and answer i stole from (and modified), lol
* [ChatGPT](https://chat.openai.com) - because I'm bad at coding