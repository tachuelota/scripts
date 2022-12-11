#!/usr/bin/env python3

import subprocess
import re
import os
import sys

from clint.textui.progress import Bar

from gooey import Gooey, GooeyParser

def is_video_file(file_name):
    video_extensions = ['.avi', '.mov', '.flv', '.wmv', '.mkv']
    file_extension = os.path.splitext(file_name)[1]
    
    if file_extension in video_extensions:
        return True
    return False

parser = GooeyParser()

parser.add_argument('Directory', widget='DirChooser')

@Gooey(progress_regex=r"Encoding: task \d+ of \d+, (\d+\.\d\d) %", hide_progress_msg=True)
def main():
    args = parser.parse_args()
    if(os.path.isdir(args.Directory)):
        for filename in os.listdir(args.Directory):
            if(is_video_file(filename)):
                line = ""
                print(filename)
                full_path = os.path.join(args.Directory, filename)
                profile = ["HandBrakeCLI","-i",f"{full_path}","-o",f"{os.path.splitext(full_path)[0]}.mp4","-Z","Very Fast 1080p30"]
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

                        line = ""
                    else:
                        line += nl.decode('utf-8')

                error = cp.stderr.read()

                if 'Encode done!' in str(error):
                    print("Done")
                else:
                    print(str(error))
                #os.remove(full_path)

if __name__ == "__main__":
    sys.exit(main())
