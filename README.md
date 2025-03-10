# Reddit video Downloader 

This is a simple Python script with a gui to download videos and gifs that are hosted on Reddit. This does not work for videos/gifs hosted on third party services like imgur.com.
***
Most videos are hosted on and downloaded from packaged-media.redd.it. If not they will be downloaded from v.redd.it. 

Videos on v.redd.it are not contained in a mp4 container file and need to be merged into one to have audio and video. To do this the [FFmpeg](https://www.ffmpeg.org/) command line tool is used (see: [src/ffmpeg_cmd.py](https://github.com/JustAName3/Reddit-Video-Downloader/blob/master/src/ffmpeg_cmd.py)). [FFmpeg](https://www.ffmpeg.org/) must be installed on your system in order for this to work. 


## Setup
1. Download or `git clone` the repository 

2. Install the requirements listed in requirements.txt

    `pip install -r requirements.txt`

3. Install FFmpeg on your system. If you don't know how, google "FFmpeg install guide".

If you install the requirements in a venv you need to add a shebang pointing to the python interpreter of your venv in the main.py file.

## GUI

![Image not found](gui.png)

1. Enter URL to Reddit post here.
2. If you press the "check" button the information will be preloaded. This is optional. 
3. Status code of the https response will be displayed here.
4. Name of the .mp4/.gif file that will be saved. If you press "check" the title of the Reddit post will be inserted.
5. Enter path to where the video should be saved in. When no path is given the default path will be inserted (C:\Users\user\Videos, works only on windows).
6. Press to download. Be sure to put in a title for the file or press "check" before.  
***  

Please use responsible. Feel free to open issues on GitHub if you encounter errors.