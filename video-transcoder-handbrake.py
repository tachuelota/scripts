#!/usr/bin/env python3

import subprocess
import re
import os
import sys

from gooey import Gooey, GooeyParser
from colored import stylize, attr

def is_video_file(file_name: str):
    return os.path.splitext(file_name)[1] in ['.avi', '.mov', '.flv', '.wmv', '.mkv']

parser = GooeyParser(description="Transcode all videos from a directory")

parser.add_argument('Directory', help='Choose the directory to convert', widget='DirChooser')
parser.add_argument('Quality', help='Pick the quality to convert to', choices=["Very Fast 1080p30", "Very Fast 720p30"], default="Very Fast 1080p30")
options = parser.add_argument_group('Options')
options.add_argument('--RemoveOnFinish', help='Delete the file when converted', action="store_true", default=True, metavar='Remove file after conversion')

@Gooey(progress_regex=r"Encoding: task \d+ of \d+, (\d+\.\d\d) %", hide_progress_msg=True, required_cols=1, default_size=(610, 580),
timing_options={
            'show_time_remaining':True,
            'hide_time_remaining_on_complete':True
        })
def main():
    args = parser.parse_args()
    if(os.path.isdir(args.Directory)):
        for filename in os.listdir(args.Directory):
            if(is_video_file(filename)):
                line = str()
                print(stylize(filename, attr("bold") + attr("underlined")))
                full_path = os.path.join(args.Directory, filename)
                profile = ["HandBrakeCLI","-i",f"{full_path}","-o",f"{os.path.splitext(full_path)[0]}.mp4","-Z",args.Quality]
                cp = subprocess.Popen(profile, stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)

                while True:
                    nl = cp.stdout.read(1)

                    if nl == '' or cp.poll() is not None:
                        break  # Aborted, no characters available, process died.

                    elif nl.hex() == '0d' and len(line) > 30:

                        # regex match for % complete and ETA, assuming the regex is ok.
                        matches = re.match(r"Encoding: task \d+ of \d+, (\d+\.\d\d) %", line)

                        if matches:
                            print(matches.group())

                        line = str()
                    else:
                        line += nl.decode('utf-8')

                error = str(cp.stderr.read())

                if 'Encode done!' in error:
                    print("Done")
                    if args.RemoveOnFinish:
                        os.remove(full_path)
                else:
                    raise Exception(error)

if __name__ == "__main__":
    sys.exit(main())
