# -*- coding: utf-8 -*-
import sys
import time
import os
from functools import wraps
from pytube import YouTube


def getUrlFromTxt():
    with open('url_list.txt', 'r') as urls_f:
        urls = []
        for url in urls_f.readlines():
            if not url == '\n':
             urls.append(url.strip())
    return urls


# urls = ('https://www.youtube.com/watch?v=Tq6rCWPdXoQ', 'https://www.youtube.com/watch?v=9bZkp7q19f0','https://www.youtube.com/watch?v=To3YL92HZyc')
urls = getUrlFromTxt()


def timethis(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, getHumanTime(end-start))
        return result
    return wrapper


def getHumanTime(sec):
    if sec >= 3600:  # Converts to Hours
        return '{0:d} hour(s)'.format(int(sec / 3600))
    elif sec >= 60:  # Converts to Minutes
        return '{0:d} minute(s)'.format(int(sec / 60))
    else:            # No Conversion
        return '{0:d} second(s)'.format(int(sec))


@timethis
def download_video(url, local_dir):
    try:
        yt = YouTube(url)
        yt_stream = yt.streams
    except Exception as e:
        print('Error {0}'.format(str(e)).encode('utf-8'))
        print('Something wrong with the url or video, Pls check!')
        return -1

    try:
        video = yt_stream.filter(progressive=True).order_by('resolution').desc().first()
    except Exception :
        video = yt_stream.filter(progressive=True).order_by('resolution').desc().first()

    try:
        video.download(local_dir)
        # print(" successfully downloaded", yt.filename)
        print(" The video has been successfully downloaded")
        return 1
    #except OSError:
    except OSError as e:
        print("The video already exist in this {0}! Skipping video...".format(local_dir))
        print(e)
        return 0


local_dir = os.path.join(os.getcwd(), "video")
print("local_dir=", local_dir)
# make local_dir if dir specified doesn't exist
try:
    os.makedirs(local_dir, exist_ok=True)
except OSError as e:
    print(e)
    exit(1)


start = time.time()
file_count = 0
for url in urls:
    url_start = time.time()
    print("\nDownloading for url:{0}".format(url))
    ret = download_video(url, local_dir)
    if (ret > 0):
        file_count += ret
    print("")
end = time.time()
elapsed = end - start

if file_count == 0:
    print("No video has been downloaded into {0}!".format(local_dir))
else:
    print("Total {0} file(s) have been downloaded into  {1}!".format(file_count, local_dir))
print("Elapsed time {0}.".format(getHumanTime(elapsed)))
exit(0)
