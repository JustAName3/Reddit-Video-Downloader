import subprocess
import os

# To use merge_av() FFmpeg must be installed on your system.

raw_ffmpeg_cmd = "ffmpeg -i {video_file} -i {audio_file} -c copy {path}.mp4 -hide_banner"     # This command will be used to merge audio and video into mp4 container


def merge_av(video, audio, output_name: str, path):
    """
    Formats raw_ffmpeg_cmd and runs it. Command merges audio and video file, file will be saved in path.

    Arguments:
        -video:             Path to video file
        -audio:             Path to audio file
        -output_name:       Title of .mp4 file
        -path:              Path where .mp4 will be stored

    Returns subprocess.CompletedProcess
    """
    path = os.path.join(path, output_name)
    ffmpeg_cmd = raw_ffmpeg_cmd.format(video_file= video, audio_file= audio, path= path)

    cmd =subprocess.run(ffmpeg_cmd, capture_output= True, text= True)

    return