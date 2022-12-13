#!/usr/bin/env python3
 
import ffmpeg
from queue import Queue
import sys
import os
from threading import Thread
from tqdm import tqdm

from gooey import Gooey, GooeyParser

from contextlib import redirect_stderr
import io

def reader(pipe, queue):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((pipe, line))
    finally:
        queue.put(None)

def is_video_file(file_name):
    return os.path.splitext(file_name)[1] in ['.avi', '.mov', '.flv', '.wmv', '.mkv']

parser = GooeyParser()

parser.add_argument('Directory', widget='DirChooser')

@Gooey(progress_regex=r"(\d+)%", hide_progress_msg=True)
def main():
    args = parser.parse_args()
    if(os.path.isdir(args.Directory)):
        for filename in os.listdir(args.Directory):
            if(is_video_file(filename)):
                full_path = os.path.join(args.Directory, filename)
                total_duration = float(ffmpeg.probe(full_path)['format']['duration'])
                error = list()
                print(filename)
                
                try:
                    video = (
                        ffmpeg
                            .input(full_path)
                            .output(f"{os.path.splitext(full_path)[0]}.mp4", format='mp4', **{"c:v": "h264", "s": "hd1080", "preset": "ultrafast", "tune": "film", "x264-params": "opencl=true"})
                            .global_args('-progress', 'pipe:1', "-hwaccel", "auto")
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True)
                    )
                    q = Queue()
                    Thread(target=reader, args=[video.stdout, q]).start()
                    Thread(target=reader, args=[video.stderr, q]).start()
                    bar = tqdm(total=round(total_duration, 2))
                    progress_bar_output = io.StringIO()
                    with redirect_stderr(progress_bar_output):
                        for _ in range(2):
                            for source, line in iter(q.get, None):
                                line = line.decode()
                                if source == video.stderr:
                                    error.append(line)
                                else:
                                    line = line.rstrip()
                                    parts = line.split('=')
                                    key = parts[0] if len(parts) > 0 else None
                                    value = parts[1] if len(parts) > 1 else None
                                    if key == 'out_time_ms':
                                        time = max(round(float(value) / 1000000., 2), 0)
                                        bar.update(time - bar.n)
                                        print(progress_bar_output.read())
                                    elif key == 'progress' and value == 'end':
                                        bar.update(bar.total - bar.n)
                                        print(progress_bar_output.read())
                        bar.close()
                except ffmpeg.Error as e:
                    print(error, file=sys.stderr)
                    sys.exit(1)
                os.remove(full_path)

if __name__ == "__main__":
    sys.exit(main())
