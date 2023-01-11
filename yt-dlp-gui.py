#!/usr/bin/env python3

import yt_dlp
import sys
import re
from gooey import Gooey, GooeyParser

parser = GooeyParser(description="Download videos or playlists as mp3")

parser.add_argument('Directory', help='Choose the directory to download to', widget='DirChooser', default='download')
parser.add_argument('URL', help='URL to download')

@Gooey(default_size=(610, 590), required_cols=1, progress_regex=r"[download]: (\d+\.\d\d)%.*")
def download():
    args = parser.parse_args()
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        "outtmpl": f"{args.Directory}/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(args.URL)

if __name__ == "__main__":
    sys.exit(download())
