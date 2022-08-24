# -*- coding: UTF-8 -*-
__author__ = "Jhong,Dong-You"
"""
Ref:
https://steam.oxxostudio.tw/category/python/example/youtube-download.html
https://officeguide.cc/python-pytube-youtube-download-tool-tutorial-examples/

At cmd or terminal:
# Install pytube library
pip install pytube

# Download single YouTube video
pytube video_link

# Download all YouTube videos in a playlist
pytube playlist_link

# Download only audio part of YouTube video:
# Command:'-a' or '--audio', format:'mp4' or other
pytube -a mp4 video_link
pytube --audio mp4 video_link

# Search supported format of YouTube video
pytube -l your_link
>> Loading video...
>> <Stream: itag="17" mime_type="video/3gpp" res="144p" fps="12fps"
>> vcodec="mp4v.20.3" acodec="mp4a.40.2" progressive="True" type="video">
>> ...

# Download specific format of YouTube video
# itag is the identifier of the format row
pytube --itag 17 zh-TW your_link
"""

from pytube import YouTube
from pytube import Playlist

link = 'your_link'
loca = 'your_path'
playlist_link = ''
single_video_url_in_playlist = ''


def download_progress(stream, chunk, remains):
    total = stream.filesize  # Get file total size
    percent = (total - remains) / total * 100  # Calculate percent
    print(f'Downloading... {percent:05.2f}', end='\r')  # Print status
    # '\r' means to replace the text printed previously


def download_complete(callback_thing_one, callback_thing_two):
    print('Downloaded Successfully!')
    print('File at: ', loca)


def youtube_download(url='', location=''):
    yt_video = YouTube(url, on_progress_callback=download_progress
                       , on_complete_callback=download_complete)

    # Video title
    print(yt_video.title)
    # Video thumbnail url
    print(yt_video.thumbnail_url)
    # Check all supported format
    print(yt_video.streams)

    # Find mp4 type and the highest resolution
    # Example:
    # yt_video.streams.filter().get_by_resolution('360p').download(output_path,filename)
    video = yt_video.streams.filter(file_extension='mp4').get_highest_resolution()
    print('Filter = \n', video)

    # Download
    video_file = video.download(location)
    print(video_file)


def youtube_playlist_download(playlist_url='', location=''):
    playlist = Playlist(playlist_url)

    # Can be a video link in a list
    if single_video_url_in_playlist != '':
        single_in_playlist = Playlist(single_video_url_in_playlist)
        print('Single video in the list')
        playlist = single_in_playlist

    # Playlist title
    print(playlist.title)

    # Download videos with loop
    for video in playlist.videos:
        video.streams.first().download(location)


if __name__ == '__main__':
    youtube_download(link, loca)

    # youtube_playlist_download(playlist_link, loca)
