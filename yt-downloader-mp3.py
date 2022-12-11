import yt_dlp

url = input("URL to download: ")

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    "outtmpl": "download/%(title)s.%(ext)s"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(url)