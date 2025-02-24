import requests
import random
import json
import os

# Random user agents --> inspired by https://github.com/elmoiv/redvid/blob/master/redvid/requestmaker.py
userAgents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.62",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
              "Mozilla/5.0 (Windows; Windows NT 10.4; Win64; x64) AppleWebKit/601.6 (KHTML, like Gecko) Chrome/50.0.2268.286 Safari/603.4 Edge/16.29908",
              "Mozilla/5.0 (Windows; Windows NT 10.3; Win64; x64; en-US) Gecko/20100101 Firefox/57.1",
              "Mozilla/5.0 (Linux; U; Android 7.1; Pixel XL Build/NRD90M) AppleWebKit/600.13 (KHTML, like Gecko)  Chrome/47.0.1115.223 Mobile Safari/602.5",
              "Mozilla/5.0 (Linux i543 ; en-US) AppleWebKit/600.22 (KHTML, like Gecko) Chrome/54.0.1542.183 Safari/601",
              "Mozilla/5.0 (iPhone; CPU iPhone OS 7_6_2; like Mac OS X) AppleWebKit/533.49 (KHTML, like Gecko)  Chrome/52.0.1782.144 Mobile Safari/533.4"]


def get(url):
    """
    Sends an HTTPS GET request to given url, returns response when status code is 200
    """
    params = {"User-Agent": random.choice(userAgents)}
    response = requests.get(url, headers=params)

    if response.status_code == 200:
        print("Data received")
        return response
    else:
        print("Error", response.status_code)


def parse_packaged_media_redd_it(reddit_response: requests.Response):
    """
    Parses the given HTML response for the source of media on packaged-media.redd.it

    Returns list with all video source URLs: str, last item = highest video quality
    """
    splitted: list = reddit_response.text.split("\n")
    sources: list = None

    for line in splitted:
        if "packaged-media-json" in line:
            sources = line.split("{")
            break

    if sources is None:
        print("Source != packaged-media.redd.it")
        raise TypeError

    temp = sources.copy()
    for i in temp:
        if "https://packaged-media.redd.it" not in i:
            sources.remove(i)

    # Cleans the links to the video source
    for index in range(len(sources)):
        sources[index - 1] = sources[index - 1].replace("&quot;url&quot;:&quot;", "")
        sources[index - 1] = sources[index - 1].replace("&quot;,&quot;dimensions&quot;:", "")
        sources[index - 1] = sources[index - 1].replace("amp;", "")

    print("Extracted video sources")
    return sources


def parse_i_redd_it(reddit_response: requests.Response):
    """
    Parses the given HTML response for the source of media on i.redd.it, usually gifs

    Returns source URL: str
    """
    source = reddit_response.text.split("\n")

    for line in source:
        if "content-href" in line:
            source = line
            break

    source = source.split('"')
    for i in source:
        if "https://i.redd.it" in i:
            source = i
            break

    print("Extracted video source")
    return source


def parse_v_redd_it(post_info: dict):
    """
    Returns media source URL.
    post_info: dict has to have the base url and width of a video --> output from get_info()
    """
    audio_path = f"{post_info["base_url"]}/HLS_AUDIO_128.aac"
    video_path = f"{post_info["base_url"]}/HLS_{post_info["width"]}.ts"

    return video_path, audio_path


def get_info(url):
    """
    Saves useful information about a post from its .json

    Returns dict
    """
    response = get(url= url +".json")

    raw_info = json.loads(response.text)

    info: dict = {
        "title":                    raw_info[0]["data"]["children"][0]["data"]["title"],
        "is_reddit_media_domain":   raw_info[0]["data"]["children"][0]["data"]["is_reddit_media_domain"],
        "domain":                   raw_info[0]["data"]["children"][0]["data"]["domain"],
        "hls_url":                  raw_info[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["hls_url"],
        "height":                   raw_info[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["height"],
        "width":                    raw_info[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["width"],
        "has_audio":                raw_info[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["has_audio"],
        "is_gif":                   raw_info[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["is_gif"]
    }

    base_url = info["hls_url"].split("/")
    del base_url[-1]
    base_url = "/".join(base_url)
    info["base_url"] = base_url

    return info


def save_video_from_source_url(url, path, file_name, file_type=".mp4"):
    """
    Makes an HTTPS GET request to url and saves the video into a file

    Returns None
    """
    response = get(url)
    path = os.path.join(path, file_name, file_type)

    with open(path, "wb") as file:
        file.write(response.content)

