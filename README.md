# scripts
A collection of scripts I made for personal use

## audio-splitter.py
Requires ffmpeg to work

Put the timestamps of the audio file to split in timestamps.txt along with the name to save the split as, pass the source audio file as an argument and then let the script handle the rest

## yt-downloader-mp3.py
Asks the user to input a YouTube URL and then downloads the video as an mp3 files in a folder called "download", supports playlists

## pdf-merger.py
Merges various pdf files into another called "merged-pdf.pdf"

## pdf-size-reducer.py
Reduces the size of pdf files by doing several things, takes the following optional arguments:
  - --remove-images: removes all the images in the pdf
  - --compress: compresses the pdf

## video-transcoder.py 
Requires ffmpeg to work

Transcodes a video from whatever codec and resolution it has to be 720p, h264 and mp4 for maximum compatibility, it also has a nice loading bar
