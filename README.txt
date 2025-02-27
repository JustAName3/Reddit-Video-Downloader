Still not finished, but usable.

This is a simple python app for downloading Reddit videos and gifs.

- Install requirements and FFmpeg.
- Run the gui.py file.
- Paste in URL, click "Check" button if you want to put in the title and default path automatically.
- Click "Download". The video should be saved in the given path (default on Windows: C:\Users\user\Videos).

Most Videos are hosted on packaged-media.redd.it, if not they will be downloaded from v.redd.it. Audio and Video
on v.redd.it are separate. They will be combined using the FFmpeg command line tool. To use this function FFmpeg
needs to be installed on your system.

All the main functions for getting the source of the video and actually saving it are in the functions.py file.


For now everything should work, but I need to do further testing. I will make improvements soon. Feel free to submit
feedback, feature requests and issues on GitHub.
This was made on windows. Please use responsible.

