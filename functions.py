import requests
import random
import json

# Random user agents --> inspired by https://github.com/elmoiv/redvid/blob/master/redvid/requestmaker.py
userAgents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.62",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"]


# Makes a get request to the given url and returns the response if status == 200
def get(url):
    params = {"User-Agent": random.choice(userAgents)}
    response = requests.get(url, headers=params)

    if response.status_code == 200:
        print("Data received")
        return response
    else:
        print("Error", response.status_code)


# Parses the response and gets the video sources for all qualities for videos hosted on v.redd.it
def parse_v_redd_it(reddit_response: requests.Response):
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


# Parses the response and gets the source for the video hosted on i.redd.it --> Used for gifs
def parse_i_redd_it(reddit_response: requests.Response):
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


# Gets the .json of the url and returns necessary information
def get_info(url):
    response = get(url= url +".json")

    raw_info = json.loads(response.text)

    info: dict = {
        "title":                    raw_info[0]["data"]["children"][0]["data"]["title"],
        "is_reddit_media_domain":   raw_info[0]["data"]["children"][0]["data"]["is_reddit_media_domain"],
        "domain":                   raw_info[0]["data"]["children"][0]["data"]["domain"],
        "url_overridden_by_dest":   raw_info[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]        # Video source for non reddit-hosted videos/gifs
    }

    return info
