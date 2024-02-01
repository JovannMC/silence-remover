# silence-remover
I needed a way to trim out the silence from the beginning and end of many audio files I had, but didn't find a decent solution that was free. So I did it myself (kind of), thanks internet!

## Description
It's self-explanatory; the script trims out silence from the beginning and/or the end of audio files and then saves them either in a trimmed folder, or replaces the original file.<br>
<br>
The program is customizable and has many settings to mess with from scanning a specific directory to specifying the amount of threads allocated to the processing.

## Features
- Scan a specific directory
  - Default: current directory
- Toggle scanning subdirectories
  - Default: no
- Save audio files' metadata
  - Default: yes
- Trim silence from the beginning, end, or both
  - Default: both
- Specify amount of threads allocated to program
  - Default: 1
- Replace original files with trimmed versions
  - Default: no
- Specify path to place trimmed files (if replacing)
  - Default: /trimmed
- Specify minimum duration of silence to trim
  - Default: 1.0 seconds
- Change padding around the detected silence
  - Default: 32 samples
- Change noise floor of silence
  - Default: -64 db

## Acknowledgements
* [Original script](https://sound.stackexchange.com/questions/52246/how-can-i-batch-remove-trailing-silence-from-audio-files) - the StackExchange post and answer i stole from, lol
* [ChatGPT](https://chat.openai.com) - because i'm bad at coding