# visual-microphone-project

This project consists of a Python implementation of [Visual Microphone](https://people.csail.mit.edu/mrub/VisualMic/)


## Install requirements:
Simply run:
```
pip install -r requirements.txt
```
If running in a linux environment, then install libgl1 library:
```
apt-get install libgl1
```
## Usage:
```
python main.py --video_path test.avi --output_path out.wav
```

To test the code on a real video from the Visual Microphone project, you can get the video with the following command:
```
## The video size is approximately 11Gb
wget https://data.csail.mit.edu/vidmag/VisualMic/Results/Chips2-2200Hz-Mary_MIDI-input.avi
```

The resulting audio from this video using this code is `result.wav` 