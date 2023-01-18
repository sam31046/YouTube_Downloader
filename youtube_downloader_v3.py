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


def Youtube_download_progress(vid, chunk, bytes_remaining):
    total_size = vid.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size / 1024) / 1024
    totalsz = round(totalsz, 1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion, 2)
    # Print status
    # '\r' means to replace the text printed previously
    """
    This is an example of single line. As for multiple lines, have to set cursors.
    Example:
    import time
    for ii in range(100):
        print(f"\rPercent: {ii + 1} %", end=" " * 20)
        time.sleep(1)
    """
    print(f'Download Progress: {percentage_of_completion}%')
    print(f'Total Size: {totalsz} MB')
    print(f'Downloaded: {dwnd} MB')
    print(f'Remaining:{remain} MB\n')


def Youtube_download_progress_v2(vid, chunk, bytes_remaining):
    total_size = vid.filesize
    bytes_downloaded = total_size - bytes_remaining
    print('\r' + 'Progress: {%s%s}%.2f%%;' % (
        '█' * int(bytes_downloaded * 100 / total_size),
        ' ' * (100 - int(bytes_downloaded * 100 / total_size)),
        float(bytes_downloaded / total_size * 100)), end='')


def Youtube_download_complete(vid, file_handle):
    print('Downloaded Successfully!')
    print('File at: ', location)


# Download single video
def Youtube_video_download(url='', location=''):
    yt_video = YouTube(url, on_progress_callback=Youtube_download_progress_v2,
                       on_complete_callback=Youtube_download_complete)
    """
    # Video thumbnail url
    print(yt_video.thumbnail_url)
    # Check all supported format
    print(yt_video.streams)
    """
    # Video title
    print(f'Downloading: {yt_video.title}')
    # Find mp4 type and the highest resolution
    # Example:
    # yt_video.streams.filter().get_by_resolution('360p').download(output_path,filename)
    video = yt_video.streams.filter(file_extension='mp4').get_highest_resolution()
    print('Filter = \n', video)

    # Download and display location
    video_file = video.download(location)
    print(video_file)
    return yt_video


# Filter: By title keywords or by entire playlist
def Youtube_filter_keyword_search(playlist, keyword):
    video_titles = []
    video_urls = []
    for video, url in zip(playlist.videos, playlist.video_urls):
        if (keyword in str.lower(video.title)) or (keyword == ''):
            print(video.title)  # List all titles in the playlist
            video_titles.append(str(video_titles))
            video_urls.append(url)
    return video_titles, video_urls


def Youtube_playlist_download(playlist_url='', location=''):
    playlist = Playlist(playlist_url)
    # Playlist title
    print(playlist.title)
    start_download = 'n'
    keyword = ''
    titles = ''
    urls = ''
    while start_download == 'n':
        titles, urls = Youtube_filter_keyword_search(playlist, keyword)
        keyword = str.lower(input("Please enter title keyword: "))
        print("Enter 'y' to start downloading.")
        if (keyword == 'y') or (keyword == 'yes'):
            start_download = 'y'
    # Download videos after filtering
    for title, url in zip(titles, urls):
        try:
            Youtube_video_download(url, location)
        except:
            print(f'Video: \n\n{title} cannot download, step to the next video.\n\n')
        else:
            print(f'Video: \n\n{title} Downloaded Successfully!\n\n')


def Youtube_mp3_download(url='', location=''):
    yt_video = YouTube(url, on_progress_callback=Youtube_download_progress_v2,
                       on_complete_callback=Youtube_download_complete)
    # title
    print(f'Downloading: {yt_video.title}')
    # pyTube does not support mp3 download. We have to convert.
    # https://stackoverflow.com/questions/47420304/download-video-in-mp3-format-using-pytube
    # Ref: https://hackmd.io/@brad84622/Hk_71R7-v
    audio = yt_video.streams.filter(only_audio=True).first()
    print('Filter = \n', audio)

    # Download and display location
    audio_file = audio.download(location)
    # save the file
    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'
    os.rename(audio_file, new_file)
    print(audio_file)


if __name__ == '__main__':
    import os
    from pytube import YouTube, Playlist

    link = ''  # A YouTube Video url link
    location = ''  # Download video to path
    playlist_link = ''  # A YouTube playlist url link
    print("Welcome to YouTube Downloader!")
    print("Enter 'q' to exit...")
    while True:
        # Input download mode
        download_mode = str(input("Please enter a 'number' to select a download mode:\n"
                                  "1. Download a video with a video url.\n"
                                  "2. Download several videos with a playlist url.\n"
                                  "3. Download mp3 file with a video url.\n"))
        if str.lower(download_mode) == 'q' or str.lower(download_mode) == 'quit':
            break

        # Input path
        location = input("Please enter the path you want to save the videos(Default path: Same as program file.):\n")
        if str.lower(location) == 'q' or str.lower(location) == 'quit':
            break  # Quit program

        # Input url
        link = input("Please enter your url:\n")
        if str.lower(link) == 'q' or str.lower(link) == 'quit':
            break
        # Execute
        elif download_mode == '1':
            Youtube_video_download(link, location)
            break
        elif download_mode == '2':
            Youtube_playlist_download(link, location)
            break
        elif download_mode == '3':
            Youtube_mp3_download(link, location)
            break
        else:
            print("Please enter correct number.\n")
    print("Program Closed.")
