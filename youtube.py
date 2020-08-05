import os
from pytube import YouTube
from youtube_search import YoutubeSearch
from moviepy.editor import *

def search(text):
    # Search on youtube and pick first result
    result = YoutubeSearch(text, max_results=1).to_dict()

    #Return the link
    return 'https://www.youtube.com' + result[0].get('url_suffix')

def download_mp4(link):
    # Get the video object
    yt = YouTube(link)

    # Select the quality and type of video
    stream = yt.streams.filter().first()

    # Download the video
    stream.download()

    path = str(stream.default_filename)

    # Wait for download
    while not os.path.isfile(path):
        pass

    return path

def convert_mp4_to_mp3(path):
    # Select path for video and audio files
    path_mp3 = path[:-1]
    path_mp3 += "3"

    # Load and convert the video
    video = VideoFileClip(path)
    video.audio.write_audiofile(path_mp3)

    # Delete the video
    del video.reader
    del video
    os.remove(path)

    return path_mp3