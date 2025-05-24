import os
import sys 
import log
import logging
import pathlib
import functions
import exceptions
import ffmpeg_cmd

# Some functions I just copied out of gui.py and modified them. This does the trick

logger = logging.getLogger("cli")
logger.debug(f"sys.argv: {sys.argv}")

# Default location for saving videos
default_path = pathlib.Path.home() / "Videos"

temp_path = pathlib.Path(__file__).parent.parent / "temp"

raw_args = sys.argv[1:]     # All args passed to the script
url = raw_args [0]          # Url must be given as first argument, optionals follow


def parse_source(domain: str, response, info: dict):
    """
    Calls the functions.py parsing functions
    Returns str -> "v", "i" or "p" depending on video source URL and the source(s).
    """
    if domain == "v.redd.it":
        src = functions.parse_packaged_media_redd_it(response)
        if src is None:
            src = functions.parse_v_redd_it(info)
            return "v", src
        else:
            return "p", src
    elif domain == "i.redd.it":
        src = functions.parse_i_redd_it(response)
        return "i", src


def check_url(url):
    if "reddit.com" not in url:
        return False
    else:
        return True


def download(url = url, args: list = raw_args[1:], path = default_path):
    logger.debug(f"Args passed to func: {args}, url: {url}, path: {path}")

    if not check_url(url):
        logger.warning(f"URL {url} is not a URL to Reddit")
        return

    info: dict = functions.get_info(url)
    
    # Checking for optional args
    if len(args) > 0:
        for arg in args:
            flag = arg[:2] # Separating the flag from data

            if flag == "-t":
                new_title = arg[2:]

                if new_title == "" or new_title == " ":
                    logger.warning("No new title given")
                    return
                else:
                    info["title"] = new_title
                    logger.info(f"Changing title to '{new_title}'")

            elif flag == "-p":
                new_path = pathlib.Path(arg[2:])

                if new_path.exists():
                    path = new_path
                    logger.info(f"Using new path: {path}")
                else:
                    logger.warning(f"Specified path ({new_path}) does not exists")
                    return
    else:
        logger.info("No optional arguments given")
            
    # Making request to Reddit to get the source of the video
    res = functions.get(url= url)
    logger.info(f"Status code: {res.status_code}")

    src_domain, src_url = parse_source(domain= info["domain"], response= res, info= info)

    # Downloading and saving video
    if src_domain == "i":
        try:
            functions.download(url= src_url,
                               path= path,
                               file_name= info["title"],
                               file_type= ".gif")
        except exceptions.ServerError:
            logger.exception("")
            return
    elif src_domain == "p":
        try:
            functions.download(url= src_url[-1],
                               path= path,
                               file_name= info["title"])
        except exceptions.ServerError:
            logger.exception("")
            return
    elif src_domain == "v":
        try:
            functions.download(url= src_url[0],
                               path= temp_path,
                               file_name= "Vid",
                               file_type= ".ts")
            functions.download(url= src_url[-1],
                               path= temp_path,
                               file_name= "Aud",
                               file_type= ".aac")
        except exceptions.ServerError:
            logger.exception("")
            return

        try:
            logger.info("calling ffmpeg_cmd.merge_av")
            cmd_stdout = ffmpeg_cmd.merge_av(video= str(temp_path / "Vid.ts"),
                                             audio= str(temp_path / "Aud.aac"),
                                             output_name= info["title"],
                                             path= path)
                
            logger.info("Merged video and audio with FFmpeg")
            logger.debug(f"FFmpeg args: {cmd_stdout.args}")
        except exceptions.FFmpegError:
            logger.exception("")
            return
        finally:
            if (temp_path / "Aud.aac").exists():
                os.remove(path= temp_path / "Aud.aac")
                    
            if (temp_path / "Vid.ts").exists():
                os.remove(path = temp_path / "Vid.ts")



if __name__ == "__main__":

    download(url)

    print("Finished")