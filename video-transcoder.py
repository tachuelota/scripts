#!/usr/bin/env python
import argparse
import ffmpeg
from queue import Queue
import sys
import textwrap
from threading import Thread
from tqdm import tqdm

def reader(pipe, queue):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((pipe, line))
    finally:
        queue.put(None)

parser = argparse.ArgumentParser(description=textwrap.dedent('''\
    Process video and report and show progress bar.

    This is an example of using the ffmpeg `-progress` option with
    stdout to report progress in the form of a progress bar.

    The video processing simply consists of converting the video to
    sepia colors, but the same pattern can be applied to other use
    cases.
'''))

parser.add_argument('in_filename', help='Input filename')

if __name__ == '__main__':
    args = parser.parse_args()
    total_duration = float(ffmpeg.probe(args.in_filename)['format']['duration'])
    error = list()
    
    try:
        video = (
            ffmpeg
                .input(args.in_filename)
                .output(f"{args.in_filename[:args.in_filename.rfind('.')]}.mp4", format='mp4', **{"c:v": "h264", "s": "hd1080", "preset": "ultrafast", "tune": "film", "x264-params": "opencl=true"})
                .global_args('-progress', 'pipe:1', "-hwaccel", "auto")
                .overwrite_output()
                .run_async(pipe_stdout=True, pipe_stderr=True)
        )
        q = Queue()
        Thread(target=reader, args=[video.stdout, q]).start()
        Thread(target=reader, args=[video.stderr, q]).start()
        bar = tqdm(total=round(total_duration, 2))
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
                    elif key == 'progress' and value == 'end':
                        bar.update(bar.total - bar.n)
        bar.close()

    except ffmpeg.Error as e:
        print(error, file=sys.stderr)
        sys.exit(1)
