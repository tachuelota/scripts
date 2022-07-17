import argparse
from os import system
import ffmpeg

count = -1
filename = 'timestamps.txt'
timestamps = {}

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to split")
args = parser.parse_args()

with open(filename) as fh: 
	for line in fh:
		if line.startswith('#'):
			continue
		command, description = line.strip().split(None, 1) 
		timestamps[command] = description.strip() 

for i in iter(timestamps):
	count += 1

for time in range(0, count):
	ffmpeg.input(args.file).trim(start = f"00:{list(timestamps.keys())[time]}", end = f"00:{list(timestamps.keys())[time + 1]}").output(f'{list(timestamps.values())[time]}.mp3').run()
