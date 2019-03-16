# toucan_video_parser
Toucan Video Parser is a small Python GUI to extract audio from video files and replace audio in video files

### What does it do?
This is a small GUI has two main functions without reencoding the video: 
1. to take out the audio tracks from any given video files to a designated folder
2. replace audio tracks in any given video files, using .wav files in a designated folder

### What else does it do?
To maintain synchronisation of the video after the replacement of audio (to some extent). In the codes, it reads column "delay relative to video" from the metadata of the video files (if any) and applies the offset automatically. In cases of DJI camcorder, it applies a "-0.1" offset to compensate the 3 frames delay induced by the machines.

### How does it do these tasks?
It uses ffmpeg, mediainfo and their python variants, ffmpy, pymediainfo. tkinter is also used to illustrate the GUI. 

### How does it look?
Well. Ugly. Sort of. I will be more than happy to see the GUI being improved.
![screenshot](https://github.com/littlegtplr/toucan_video_parser/blob/master/Screenshot%202019-03-16%20at%2002.13.56.png)

### What is the context?
I do offline mixing for live performances recorded using camcorders and mixing desks. The main task I do is to mix the recording from the mixer and the audio tracks in the videos recorded. This little GUI is a utility I wrote for myself to handle the process related to audio tracks in videos. It's been quite handy and saved me a bunch of tedious manual work, though it's just a simple GUI. 

### How to use it?
Simply from left to right - 
1. Choose whatever video files you'd like to process
2. Assign a folder for this batch - either a folder to put the audio files extracted, or a folder contains audio files to be used to replace the original audio in the video files, file names have to be exactly the same. E.g., The program will look for 100_001.wav if 100_001.mts is on the list. 
3. Choose whether you'd like to extract the audio tracks or replace the audio tracks. Then wait (if no error). 
4. The progress will be shown in the middle part of the GUI, with 'Done!' at the end of the batch. 

### What if I don't use Python but I still want to use the parser
Well. Sorry mate. I haven't managed to pack the py codes into exe and app. So...

### What to do if I have a question?
Please feel free to ask here!
