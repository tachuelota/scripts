#!/usr/bin/env python3

import subprocess
import re
import os
import sys

from gooey import Gooey, GooeyParser

def is_video_file(file_name):
    video_extensions = ['.avi', '.mov', '.flv', '.wmv', '.mkv']
    file_extension = os.path.splitext(file_name)[1]
    
    if file_extension in video_extensions:
        return True
    return False

parser = GooeyParser()

parser.add_argument('Directory', widget='DirChooser')

@Gooey(progress_regex=r'.*(\d+\.\d+)\s%.*ETA\s(\d+)h(\d+)m(\d+)s')
def main():
    args = parser.parse_args()
    if(os.path.isdir(args.Directory)):
        for filename in os.listdir(args.Directory):
            if(is_video_file(filename)):
                full_path = os.path.join(args.Directory, filename)
                profile = ["HandBrakeCLI","-i",full_path,"-o",f"{os.path.splitext(full_path)[0]} (Converted).mp4","-Z","Very Fast 1080p30"]
                cp = subprocess.Popen(profile, stderr=subprocess.PIPE, strout=subprocess.PIPE, close_fds=True)

                line = ""

                while True:    
                    nl = cp.stdout.read(1)
                    if nl == '' and cp.poll() is not None:
                        break  # Aborted, no characters available, process died.
                    if nl == "\n":
                        line = ""
                    elif nl == "\r":
                        # regex match for % complete and ETA, assuming the regex is ok.
                        matches = re.match( r'.*(\d+\.\d+)\s%.*ETA\s(\d+)h(\d+)m(\d+)s', line.decode('utf-8') )

                        if matches:
                            pass
                            #print( matches.group() )
                            # do something
                        line = ""
                    else:
                        line += nl

                error = cp.stderr.read()
                success = "Encode done!" in error

if __name__ == "__main__":
    sys.exit(main())